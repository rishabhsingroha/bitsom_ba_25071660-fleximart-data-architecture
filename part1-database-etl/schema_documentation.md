# FlexiMart Database Schema Documentation

## Entity-Relationship Description

### ENTITY: customers

**Purpose:** Stores customer information and personal details for FlexiMart e-commerce platform.

**Attributes:**
- `customer_id`: Unique identifier for each customer (Primary Key, Auto-increment Integer)
- `first_name`: Customer's first name (VARCHAR(50), NOT NULL)
- `last_name`: Customer's last name (VARCHAR(50), NOT NULL)
- `email`: Customer's email address (VARCHAR(100), UNIQUE, NOT NULL) - Used for login and communication
- `phone`: Customer's contact phone number (VARCHAR(20), Optional) - Standardized format
- `city`: Customer's city of residence (VARCHAR(50), Optional) - For location-based analytics
- `registration_date`: Date when customer registered with FlexiMart (DATE, Optional) - For customer lifecycle analysis

**Relationships:**
- One customer can place MANY orders (1:M relationship with orders table)
- Connected via `customer_id` foreign key in orders table

**Sample Data:**
| customer_id | first_name | last_name | email | phone | city | registration_date |
|-------------|------------|-----------|-------|-------|------|-------------------|
| 1 | John | Smith | john.smith@email.com | +91-5550101 | New York | 2023-01-15 |
| 2 | Jane | Doe | jane.doe@email.com | +91-5550102 | Los Angeles | 2023-02-20 |

---

### ENTITY: products

**Purpose:** Stores product catalog information including pricing and inventory details.

**Attributes:**
- `product_id`: Unique identifier for each product (Primary Key, Auto-increment Integer)
- `product_name`: Name of the product (VARCHAR(100), NOT NULL) - Display name for customers
- `category`: Product category classification (VARCHAR(50), NOT NULL) - Standardized category names (e.g., "Electronics", "Furniture")
- `price`: Selling price of the product (DECIMAL(10,2), NOT NULL) - Current market price
- `stock_quantity`: Available inventory quantity (INT, DEFAULT 0) - For inventory management

**Relationships:**
- One product can appear in MANY order items (1:M relationship with order_items table)
- Connected via `product_id` foreign key in order_items table

**Sample Data:**
| product_id | product_name | category | price | stock_quantity |
|------------|--------------|----------|-------|----------------|
| 1 | Laptop Pro 15 | Electronics | 1299.99 | 50 |
| 2 | Wireless Mouse | Electronics | 29.99 | 200 |

---

### ENTITY: orders

**Purpose:** Stores order header information for each customer purchase transaction.

**Attributes:**
- `order_id`: Unique identifier for each order (Primary Key, Auto-increment Integer)
- `customer_id`: Reference to the customer who placed the order (INT, NOT NULL, Foreign Key → customers.customer_id)
- `order_date`: Date when the order was placed (DATE, NOT NULL) - For time-based analysis
- `total_amount`: Total value of the order including all items (DECIMAL(10,2), NOT NULL) - Sum of all order items
- `status`: Current status of the order (VARCHAR(20), DEFAULT 'Pending') - Values: Pending, Processing, Shipped, Delivered, Cancelled

**Relationships:**
- One order belongs to ONE customer (M:1 relationship with customers table)
- One order contains MANY order items (1:M relationship with order_items table)
- Connected via `order_id` foreign key in order_items table

**Sample Data:**
| order_id | customer_id | order_date | total_amount | status |
|----------|-------------|------------|--------------|--------|
| 1 | 1 | 2024-01-15 | 1299.99 | Delivered |
| 2 | 2 | 2024-01-16 | 59.98 | Shipped |

---

### ENTITY: order_items

**Purpose:** Stores individual line items within each order, representing products purchased and their quantities.

**Attributes:**
- `order_item_id`: Unique identifier for each order line item (Primary Key, Auto-increment Integer)
- `order_id`: Reference to the parent order (INT, NOT NULL, Foreign Key → orders.order_id)
- `product_id`: Reference to the product being ordered (INT, NOT NULL, Foreign Key → products.product_id)
- `quantity`: Number of units ordered for this product (INT, NOT NULL) - Must be positive
- `unit_price`: Price per unit at the time of order (DECIMAL(10,2), NOT NULL) - Captures historical pricing
- `subtotal`: Total amount for this line item (DECIMAL(10,2), NOT NULL) - Calculated as quantity × unit_price

**Relationships:**
- One order item belongs to ONE order (M:1 relationship with orders table)
- One order item references ONE product (M:1 relationship with products table)

**Sample Data:**
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|---------------|----------|------------|----------|------------|----------|
| 1 | 1 | 1 | 1 | 1299.99 | 1299.99 |
| 2 | 2 | 2 | 2 | 29.99 | 59.98 |

---

## Normalization Explanation

This database design follows **Third Normal Form (3NF)**, which ensures data integrity and eliminates redundancy. Here's why:

### Functional Dependencies Identified:

1. **customers table:**
   - `customer_id` → `first_name`, `last_name`, `email`, `phone`, `city`, `registration_date`
   - `email` → `customer_id` (unique constraint ensures this)

2. **products table:**
   - `product_id` → `product_name`, `category`, `price`, `stock_quantity`

3. **orders table:**
   - `order_id` → `customer_id`, `order_date`, `total_amount`, `status`
   - `customer_id` → (references customers, but doesn't duplicate customer data)

4. **order_items table:**
   - `order_item_id` → `order_id`, `product_id`, `quantity`, `unit_price`, `subtotal`
   - `order_id` + `product_id` → `quantity`, `unit_price`, `subtotal` (composite determines line item)

### 3NF Compliance:

**First Normal Form (1NF):** ✓ All attributes are atomic (no multi-valued or composite attributes)

**Second Normal Form (2NF):** ✓ All non-key attributes are fully functionally dependent on the primary key. In `order_items`, `quantity`, `unit_price`, and `subtotal` depend on the combination of `order_id` and `product_id` (via `order_item_id`).

**Third Normal Form (3NF):** ✓ No transitive dependencies exist. For example:
- In `orders`, `total_amount` is directly dependent on `order_id`, not through `customer_id`
- In `order_items`, `subtotal` is calculated from `quantity` and `unit_price`, but stored for historical accuracy (not a transitive dependency issue)
- Customer information is not duplicated in orders (only `customer_id` foreign key is stored)

### Anomaly Prevention:

**Update Anomalies Avoided:** If a customer's email changes, we only update one record in `customers` table, not multiple order records.

**Insert Anomalies Avoided:** We can add new products without needing existing orders, and add new customers without requiring orders.

**Delete Anomalies Avoided:** Deleting an order doesn't delete customer or product information, only the order and its line items (with proper foreign key constraints).

This normalized design ensures data consistency, reduces storage requirements, and maintains referential integrity through foreign key relationships.
