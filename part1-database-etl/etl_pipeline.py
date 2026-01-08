"""
FlexiMart ETL Pipeline
Extracts, Transforms, and Loads data from CSV files into MySQL database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import logging
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'fleximart'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Data quality tracking
data_quality_stats = {
    'customers': {
        'total_read': 0,
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'records_loaded': 0
    },
    'products': {
        'total_read': 0,
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'records_loaded': 0
    },
    'sales': {
        'total_read': 0,
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'records_loaded': 0
    }
}


def standardize_phone(phone):
    """
    Standardize phone number format to: +91-9876543210
    Handles various formats: (555) 123-4567, 555.123.4567, 555-123-4567, etc.
    """
    if pd.isna(phone) or phone == '':
        return None
    
    # Remove all non-digit characters except +
    phone_clean = re.sub(r'[^\d+]', '', str(phone))
    
    # If starts with +, keep it; otherwise add +91-
    if phone_clean.startswith('+'):
        # Format: +91-9876543210
        if len(phone_clean) > 3:
            return phone_clean[:3] + '-' + phone_clean[3:]
        return phone_clean
    else:
        # Add +91- prefix if not present
        if len(phone_clean) >= 10:
            return '+91-' + phone_clean[-10:]
        return '+91-' + phone_clean if phone_clean else None


def standardize_category(category):
    """
    Standardize category names: "electronics", "Electronics", "ELECTRONICS" → "Electronics"
    """
    if pd.isna(category) or category == '':
        return None
    
    # Capitalize first letter, lowercase rest
    return str(category).capitalize()


def parse_date(date_str):
    """
    Convert various date formats to YYYY-MM-DD
    Handles: 2024-01-15, 15/01/2024, 02-03-2024, 2024/02/04
    """
    if pd.isna(date_str) or date_str == '':
        return None
    
    date_str = str(date_str).strip()
    
    # Try different date formats
    formats = [
        '%Y-%m-%d',      # 2024-01-15
        '%d/%m/%Y',      # 15/01/2024
        '%d-%m-%Y',      # 02-03-2024
        '%Y/%m/%d',      # 2024/02/04
        '%m-%d-%Y',      # 01-15-2024
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    logging.warning(f"Could not parse date: {date_str}")
    return None


def split_name(full_name):
    """
    Split customer_name into first_name and last_name
    """
    if pd.isna(full_name) or full_name == '':
        return None, None
    
    parts = str(full_name).strip().split(maxsplit=1)
    if len(parts) == 1:
        return parts[0], ''
    return parts[0], parts[1]


def extract_customers(df):
    """
    Extract and transform customer data
    """
    logging.info("Extracting customers data...")
    data_quality_stats['customers']['total_read'] = len(df)
    
    # Remove duplicates based on email (unique identifier)
    initial_count = len(df)
    df = df.drop_duplicates(subset=['email'], keep='first')
    duplicates = initial_count - len(df)
    data_quality_stats['customers']['duplicates_removed'] = duplicates
    logging.info(f"Removed {duplicates} duplicate customers")
    
    # Handle missing emails - drop records with missing emails (required field)
    missing_emails = df['email'].isna().sum() + (df['email'] == '').sum()
    df = df[df['email'].notna() & (df['email'] != '')]
    data_quality_stats['customers']['missing_values_handled'] += missing_emails
    logging.info(f"Dropped {missing_emails} records with missing emails")
    
    # Standardize phone numbers
    df['phone'] = df['phone'].apply(standardize_phone)
    
    # Parse registration dates
    df['registration_date'] = df['registration_date'].apply(parse_date)
    
    # Split customer_name into first_name and last_name
    name_parts = df['customer_name'].apply(split_name)
    df['first_name'] = [parts[0] for parts in name_parts]
    df['last_name'] = [parts[1] if parts[1] else '' for parts in name_parts]
    
    # Select and rename columns for database
    customers_clean = df[[
        'first_name', 'last_name', 'email', 'phone', 'city', 'registration_date'
    ]].copy()
    
    # Handle missing values in optional fields
    customers_clean['phone'] = customers_clean['phone'].fillna('')
    customers_clean['city'] = customers_clean['city'].fillna('Unknown')
    
    return customers_clean


def extract_products(df):
    """
    Extract and transform product data
    """
    logging.info("Extracting products data...")
    data_quality_stats['products']['total_read'] = len(df)
    
    # Remove duplicates based on product_id
    initial_count = len(df)
    df = df.drop_duplicates(subset=['product_id'], keep='first')
    duplicates = initial_count - len(df)
    data_quality_stats['products']['duplicates_removed'] = duplicates
    logging.info(f"Removed {duplicates} duplicate products")
    
    # Standardize category names
    df['category'] = df['category'].apply(standardize_category)
    
    # Handle missing prices - drop records with missing prices (required field)
    missing_prices = df['price'].isna().sum() + (df['price'] == '').sum()
    df = df[df['price'].notna() & (df['price'] != '')]
    data_quality_stats['products']['missing_values_handled'] += missing_prices
    logging.info(f"Dropped {missing_prices} records with missing prices")
    
    # Convert price to numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df[df['price'].notna()]
    
    # Handle missing stock_quantity - fill with 0 (default value)
    missing_stock = df['stock_quantity'].isna().sum() + (df['stock_quantity'] == '').sum()
    df['stock_quantity'] = df['stock_quantity'].fillna(0)
    df['stock_quantity'] = pd.to_numeric(df['stock_quantity'], errors='coerce').fillna(0).astype(int)
    data_quality_stats['products']['missing_values_handled'] += missing_stock
    logging.info(f"Filled {missing_stock} missing stock quantities with 0")
    
    # Select columns for database
    products_clean = df[[
        'product_name', 'category', 'price', 'stock_quantity'
    ]].copy()
    
    return products_clean


def extract_sales(df, customer_id_map, product_id_map):
    """
    Extract and transform sales data
    Note: Sales data needs to be transformed into orders and order_items
    """
    logging.info("Extracting sales data...")
    data_quality_stats['sales']['total_read'] = len(df)
    
    # Remove duplicates based on transaction_id
    initial_count = len(df)
    df = df.drop_duplicates(subset=['transaction_id'], keep='first')
    duplicates = initial_count - len(df)
    data_quality_stats['sales']['duplicates_removed'] = duplicates
    logging.info(f"Removed {duplicates} duplicate transactions")
    
    # Parse transaction dates
    df['transaction_date'] = df['transaction_date'].apply(parse_date)
    
    # Remove records with invalid dates
    missing_dates = df['transaction_date'].isna().sum()
    df = df[df['transaction_date'].notna()]
    data_quality_stats['sales']['missing_values_handled'] += missing_dates
    logging.info(f"Dropped {missing_dates} records with invalid dates")
    
    # Filter out records with missing customer_id or product_id
    missing_customers = df['customer_id'].isna().sum() + (df['customer_id'] == '').sum()
    missing_products = df['product_id'].isna().sum() + (df['product_id'] == '').sum()
    df = df[df['customer_id'].notna() & (df['customer_id'] != '') & 
            df['product_id'].notna() & (df['product_id'] != '')]
    data_quality_stats['sales']['missing_values_handled'] += (missing_customers + missing_products)
    logging.info(f"Dropped {missing_customers} records with missing customer_id")
    logging.info(f"Dropped {missing_products} records with missing product_id")
    
    # Map original customer_id and product_id to database IDs
    df['db_customer_id'] = df['customer_id'].map(customer_id_map)
    df['db_product_id'] = df['product_id'].map(product_id_map)
    
    # Filter out records that couldn't be mapped
    unmapped_customers = df['db_customer_id'].isna().sum()
    unmapped_products = df['db_product_id'].isna().sum()
    df = df[df['db_customer_id'].notna() & df['db_product_id'].notna()]
    data_quality_stats['sales']['missing_values_handled'] += (unmapped_customers + unmapped_products)
    logging.info(f"Dropped {unmapped_customers} records with unmapped customer_id")
    logging.info(f"Dropped {unmapped_products} records with unmapped product_id")
    
    # Convert numeric fields
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    
    # Calculate subtotal
    df['subtotal'] = df['quantity'] * df['unit_price']
    
    # Remove records with invalid numeric values
    df = df[df['unit_price'].notna()]
    
    return df


def create_database_schema(connection):
    """
    Create database tables if they don't exist
    """
    cursor = connection.cursor()
    
    try:
        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                city VARCHAR(50),
                registration_date DATE
            )
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock_quantity INT DEFAULT 0
            )
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT NOT NULL,
                order_date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """)
        
        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        
        connection.commit()
        logging.info("Database schema created successfully")
        
    except Error as e:
        logging.error(f"Error creating schema: {e}")
        raise
    finally:
        cursor.close()


def load_customers(connection, df, original_df):
    """
    Load customers data into database
    Returns mapping of original customer_id to new database customer_id
    """
    cursor = connection.cursor()
    
    try:
        # Clear existing data (optional - remove if you want to append)
        cursor.execute("DELETE FROM customers")
        
        insert_query = """
            INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        customer_id_map = {}
        records = []
        email_to_original_id = {}
        
        # Create mapping from email to original customer_id
        for _, row in original_df.iterrows():
            if pd.notna(row['email']) and row['email'] != '':
                email_to_original_id[row['email']] = row['customer_id']
        
        for _, row in df.iterrows():
            records.append((
                row['first_name'],
                row['last_name'],
                row['email'],
                row['phone'] if row['phone'] else None,
                row['city'],
                row['registration_date'] if row['registration_date'] else None
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        
        # Get the inserted customer IDs and create mapping using email
        cursor.execute("SELECT customer_id, email FROM customers ORDER BY customer_id")
        db_customers = cursor.fetchall()
        
        # Create mapping from original customer_id to database customer_id
        for db_id, email in db_customers:
            if email in email_to_original_id:
                original_id = email_to_original_id[email]
                customer_id_map[original_id] = db_id
        
        data_quality_stats['customers']['records_loaded'] = cursor.rowcount
        logging.info(f"Loaded {cursor.rowcount} customers into database")
        
        return customer_id_map
        
    except Error as e:
        logging.error(f"Error loading customers: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def load_products(connection, df, original_df):
    """
    Load products data into database
    Returns mapping of original product_id to new database product_id
    """
    cursor = connection.cursor()
    
    try:
        # Clear existing data (optional)
        cursor.execute("DELETE FROM products")
        
        insert_query = """
            INSERT INTO products (product_name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """
        
        product_id_map = {}
        records = []
        name_to_original_id = {}
        
        # Create mapping from product_name to original product_id
        for _, row in original_df.iterrows():
            if pd.notna(row['product_name']) and row['product_name'] != '':
                name_to_original_id[row['product_name']] = row['product_id']
        
        for _, row in df.iterrows():
            records.append((
                row['product_name'],
                row['category'],
                float(row['price']),
                int(row['stock_quantity'])
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        
        # Get the inserted product IDs and create mapping using product_name
        cursor.execute("SELECT product_id, product_name FROM products ORDER BY product_id")
        db_products = cursor.fetchall()
        
        # Create mapping from original product_id to database product_id
        for db_id, name in db_products:
            if name in name_to_original_id:
                original_id = name_to_original_id[name]
                product_id_map[original_id] = db_id
        
        data_quality_stats['products']['records_loaded'] = cursor.rowcount
        logging.info(f"Loaded {cursor.rowcount} products into database")
        
        return product_id_map
        
    except Error as e:
        logging.error(f"Error loading products: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def load_orders(connection, sales_df):
    """
    Load sales data as orders and order_items
    Groups transactions by customer and date to create orders
    """
    cursor = connection.cursor()
    
    try:
        # Clear existing data
        cursor.execute("DELETE FROM order_items")
        cursor.execute("DELETE FROM orders")
        
        # Group transactions by customer_id and transaction_date to create orders
        # Each unique (customer_id, transaction_date) combination becomes one order
        orders_dict = {}
        order_items_list = []
        
        for _, transaction in sales_df.iterrows():
            order_key = (transaction['db_customer_id'], transaction['transaction_date'])
            
            if order_key not in orders_dict:
                # Create new order
                order_total = transaction['subtotal']
                # Get status from transaction, default to 'Completed' if missing
                status = transaction.get('status', 'Completed')
                # Ensure status is valid (max 20 chars per schema)
                if pd.notna(status):
                    status = str(status)[:20]
                else:
                    status = 'Completed'
                
                orders_dict[order_key] = {
                    'customer_id': transaction['db_customer_id'],
                    'order_date': transaction['transaction_date'],
                    'total_amount': order_total,
                    'status': status
                }
            else:
                # Add to existing order total
                orders_dict[order_key]['total_amount'] += transaction['subtotal']
            
            # Add order item
            order_items_list.append({
                'order_key': order_key,
                'product_id': transaction['db_product_id'],
                'quantity': transaction['quantity'],
                'unit_price': transaction['unit_price'],
                'subtotal': transaction['subtotal']
            })
        
        # Insert orders
        order_id_map = {}
        insert_order_query = """
            INSERT INTO orders (customer_id, order_date, total_amount, status)
            VALUES (%s, %s, %s, %s)
        """
        
        for order_key, order_data in orders_dict.items():
            cursor.execute(insert_order_query, (
                order_data['customer_id'],
                order_data['order_date'],
                order_data['total_amount'],
                order_data['status']
            ))
            order_id_map[order_key] = cursor.lastrowid
        
        connection.commit()
        logging.info(f"Created {len(orders_dict)} orders")
        
        # Insert order items
        insert_item_query = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        items_inserted = 0
        for item in order_items_list:
            order_id = order_id_map[item['order_key']]
            cursor.execute(insert_item_query, (
                order_id,
                item['product_id'],
                item['quantity'],
                item['unit_price'],
                item['subtotal']
            ))
            items_inserted += 1
        
        connection.commit()
        data_quality_stats['sales']['records_loaded'] = items_inserted
        logging.info(f"Inserted {items_inserted} order items")
        
    except Error as e:
        logging.error(f"Error loading orders: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def generate_data_quality_report():
    """
    Generate data quality report
    """
    report = []
    report.append("=" * 60)
    report.append("FLEXIMART ETL DATA QUALITY REPORT")
    report.append("=" * 60)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    for table, stats in data_quality_stats.items():
        report.append(f"Table: {table.upper()}")
        report.append("-" * 60)
        report.append(f"  Total records read:        {stats['total_read']}")
        report.append(f"  Duplicates removed:        {stats['duplicates_removed']}")
        report.append(f"  Missing values handled:    {stats['missing_values_handled']}")
        report.append(f"  Records loaded successfully: {stats['records_loaded']}")
        report.append("")
    
    report.append("=" * 60)
    report_text = "\n".join(report)
    
    # Write to file
    with open('data_quality_report.txt', 'w') as f:
        f.write(report_text)
    
    logging.info("Data quality report generated: data_quality_report.txt")
    print(report_text)
    
    return report_text


def main():
    """
    Main ETL pipeline execution
    """
    logging.info("Starting FlexiMart ETL Pipeline")
    
    try:
        # Connect to database
        logging.info("Connecting to database...")
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            logging.info("Connected to MySQL database")
            
            # Create schema
            create_database_schema(connection)
            
            # EXTRACT: Read CSV files
            logging.info("Reading CSV files...")
            # Get the project root directory (parent of part1-database-etl)
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            data_dir = project_root / 'data'
            
            customers_df = pd.read_csv(data_dir / 'customers_raw.csv')
            products_df = pd.read_csv(data_dir / 'products_raw.csv')
            sales_df = pd.read_csv(data_dir / 'sales_raw.csv')
            
            # TRANSFORM: Clean and transform data
            customers_clean = extract_customers(customers_df)
            products_clean = extract_products(products_df)
            
            # LOAD: Insert into database and get ID mappings
            customer_id_map = load_customers(connection, customers_clean, customers_df)
            product_id_map = load_products(connection, products_clean, products_df)
            
            # Transform and load sales data
            sales_clean = extract_sales(sales_df, customer_id_map, product_id_map)
            load_orders(connection, sales_clean)
            
            logging.info("ETL Pipeline completed successfully")
            
    except Error as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()
            logging.info("Database connection closed")
    
    # Generate data quality report
    generate_data_quality_report()


if __name__ == "__main__":
    main()
