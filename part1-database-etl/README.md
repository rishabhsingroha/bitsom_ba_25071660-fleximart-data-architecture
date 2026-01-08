# Part 1: Database Design and ETL Pipeline

## Overview

This part implements a complete ETL (Extract, Transform, Load) pipeline to process raw CSV data files and load them into a MySQL/PostgreSQL relational database. The pipeline handles data quality issues and transforms the data according to the specified database schema.

## Files

- `etl_pipeline.py` - Main ETL script that extracts, transforms, and loads data
- `schema_documentation.md` - Complete database schema documentation
- `business_queries.sql` - SQL queries for business intelligence
- `data_quality_report.txt` - Generated report showing data quality metrics
- `requirements.txt` - Python dependencies

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

**For MySQL:**
```bash
mysql -u root -p -e "CREATE DATABASE fleximart;"
```

**For PostgreSQL:**
```bash
createdb fleximart
```

### 3. Configure Database Connection

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=fleximart
DB_USER=root
DB_PASSWORD=your_password
```

### 4. Run ETL Pipeline

```bash
python etl_pipeline.py
```

The script will:
1. Read CSV files from `../data/` directory
2. Clean and transform the data
3. Load data into the database
4. Generate a data quality report

## Data Quality Issues Handled

### Customers Data
- Duplicate records (removed based on email)
- Missing emails (dropped - required field)
- Inconsistent phone formats (standardized to +91-XXXXXXXXXX)
- Date format inconsistencies (converted to YYYY-MM-DD)

### Products Data
- Missing prices (dropped - required field)
- Inconsistent category names (standardized: "Electronics", "electronics", "ELECTRONICS" → "Electronics")
- Null stock values (filled with 0)

### Sales Data
- Date format inconsistencies (standardized to YYYY-MM-DD)
- Missing customer/product IDs (filtered out)
- Duplicate transactions (removed based on sale_id)

## Database Schema

The database consists of four tables:
- `customers` - Customer information
- `products` - Product catalog
- `orders` - Order headers
- `order_items` - Order line items

See `schema_documentation.md` for detailed documentation.

## Business Queries

Run the business queries:

```bash
mysql -u root -p fleximart < business_queries.sql
```

Or for PostgreSQL:
```bash
psql -U postgres -d fleximart -f business_queries.sql
```

The queries answer:
1. Customer purchase history (customers with 2+ orders and >₹5,000 spent)
2. Product sales analysis by category (categories with >₹10,000 revenue)
3. Monthly sales trends with cumulative revenue for 2024

## Output

After running the ETL pipeline, you'll get:
- Data loaded into the database tables
- `data_quality_report.txt` with statistics on data processing
- `etl_pipeline.log` with detailed execution logs

## Testing

To verify the ETL pipeline works correctly:

1. **Check Database Connection**: Ensure MySQL/PostgreSQL is running and credentials in `.env` are correct
2. **Verify Data Files**: Ensure all CSV files exist in `../data/` directory
3. **Run Pipeline**: Execute `python etl_pipeline.py` and check for errors
4. **Verify Data Load**: Query the database to confirm records were inserted:
   ```sql
   SELECT COUNT(*) FROM customers;
   SELECT COUNT(*) FROM products;
   SELECT COUNT(*) FROM orders;
   SELECT COUNT(*) FROM order_items;
   ```
5. **Check Data Quality Report**: Review `data_quality_report.txt` for processing statistics
