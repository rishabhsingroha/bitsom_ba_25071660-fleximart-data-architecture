# FlexiMart Data Warehouse Star Schema Design

## Section 1: Schema Overview

### FACT TABLE: fact_sales

**Grain:** One row per product per order line item (transaction-level detail)

**Business Process:** Sales transactions - captures every individual product sale within an order

**Measures (Numeric Facts):**
- `quantity_sold`: Number of units sold for this line item (INT, NOT NULL)
- `unit_price`: Price per unit at the time of sale (DECIMAL(10,2), NOT NULL) - captures historical pricing
- `discount_amount`: Discount applied to this line item (DECIMAL(10,2), DEFAULT 0) - for promotional analysis
- `total_amount`: Final amount for this line item (DECIMAL(10,2), NOT NULL) - calculated as (quantity × unit_price - discount_amount)

**Foreign Keys:**
- `date_key` → `dim_date.date_key` (INT, NOT NULL) - Links to date dimension for time-based analysis
- `product_key` → `dim_product.product_key` (INT, NOT NULL) - Links to product dimension
- `customer_key` → `dim_customer.customer_key` (INT, NOT NULL) - Links to customer dimension

**Surrogate Key:**
- `sale_key`: Primary key (INT, AUTO_INCREMENT) - Unique identifier for each fact record

**Type:** Transaction fact table - captures detailed sales events at the lowest level of granularity

---

### DIMENSION TABLE: dim_date

**Purpose:** Date dimension for time-based analysis and reporting. Enables drill-down from year to quarter to month to day.

**Type:** Conformed dimension - can be shared across multiple fact tables in the data warehouse

**Attributes:**
- `date_key` (PK): Surrogate key (INT, PRIMARY KEY) - Format: YYYYMMDD (e.g., 20240115 for January 15, 2024)
- `full_date`: Actual date value (DATE, NOT NULL) - For date calculations and comparisons
- `day_of_week`: Day name (VARCHAR(10)) - Monday, Tuesday, Wednesday, etc.
- `day_of_month`: Day number (INT) - 1 to 31
- `month`: Month number (INT) - 1 to 12
- `month_name`: Month name (VARCHAR(10)) - January, February, etc.
- `quarter`: Quarter identifier (VARCHAR(2)) - Q1, Q2, Q3, Q4
- `year`: Year (INT) - 2023, 2024, etc.
- `is_weekend`: Boolean flag (BOOLEAN) - TRUE for Saturday/Sunday, FALSE for weekdays

**Usage:** Enables time-based analysis like monthly trends, quarterly comparisons, weekend vs weekday sales patterns

---

### DIMENSION TABLE: dim_product

**Purpose:** Product dimension containing all product attributes for analysis and filtering

**Type:** Slowly Changing Dimension (SCD) Type 1 - current values only (historical changes not tracked)

**Attributes:**
- `product_key` (PK): Surrogate key (INT, AUTO_INCREMENT, PRIMARY KEY)
- `product_id`: Natural key from source system (VARCHAR(20)) - Original product identifier
- `product_name`: Product name (VARCHAR(100)) - Display name
- `category`: Product category (VARCHAR(50)) - Electronics, Fashion, Groceries, etc.
- `subcategory`: Product subcategory (VARCHAR(50)) - Smartphones, Laptops, Jeans, etc.
- `unit_price`: Current unit price (DECIMAL(10,2)) - For reference (actual sale price in fact table)

**Usage:** Enables product-based analysis like top-selling products, category performance, product profitability

---

### DIMENSION TABLE: dim_customer

**Purpose:** Customer dimension for customer segmentation and analysis

**Type:** Slowly Changing Dimension (SCD) Type 1 - current customer attributes only

**Attributes:**
- `customer_key` (PK): Surrogate key (INT, AUTO_INCREMENT, PRIMARY KEY)
- `customer_id`: Natural key from source system (VARCHAR(20)) - Original customer identifier
- `customer_name`: Full customer name (VARCHAR(100)) - For reporting
- `city`: Customer city (VARCHAR(50)) - Geographic analysis
- `state`: Customer state (VARCHAR(50)) - Regional analysis
- `customer_segment`: Customer segmentation (VARCHAR(20)) - High Value, Medium Value, Low Value (can be calculated or assigned)

**Usage:** Enables customer analysis like customer lifetime value, geographic sales distribution, customer segmentation

---

## Section 2: Design Decisions (150 words)

**Granularity Choice:** The fact table uses transaction line-item level granularity (one row per product per order) rather than order-level aggregation. This provides maximum flexibility for analysis—we can always aggregate up to order-level or customer-level, but cannot drill down if we start at a higher level. This granularity enables answering questions like "which specific products were in the order?" and "what was the quantity of each product?"

**Surrogate Keys:** We use surrogate keys (auto-incrementing integers) instead of natural keys (like customer_id, product_id) as primary keys in dimension tables. This provides several benefits: (1) isolates the data warehouse from source system changes, (2) enables handling of slowly changing dimensions, (3) improves join performance with integer keys, and (4) allows for multiple source systems with different natural key formats.

**Drill-Down and Roll-Up Support:** The date dimension's hierarchical structure (year → quarter → month → day) enables natural drill-down operations. Users can start with yearly totals, drill down to quarters, then months, then specific days. The star schema's denormalized structure supports fast roll-up aggregations without complex joins, making it ideal for OLAP operations and business intelligence tools.

---

## Section 3: Sample Data Flow

**Source Transaction:**
```
Order #101
Customer: "Rahul Sharma" (C001)
Product: "Samsung Galaxy S21" (P001)
Quantity: 2
Unit Price: ₹45,999
Transaction Date: 2024-01-15
```

**Becomes in Data Warehouse:**

**fact_sales:**
```sql
{
  sale_key: 1,
  date_key: 20240115,
  product_key: 5,
  customer_key: 12,
  quantity_sold: 2,
  unit_price: 45999.00,
  discount_amount: 0.00,
  total_amount: 91998.00
}
```

**dim_date:**
```sql
{
  date_key: 20240115,
  full_date: '2024-01-15',
  day_of_week: 'Monday',
  day_of_month: 15,
  month: 1,
  month_name: 'January',
  quarter: 'Q1',
  year: 2024,
  is_weekend: FALSE
}
```

**dim_product:**
```sql
{
  product_key: 5,
  product_id: 'P001',
  product_name: 'Samsung Galaxy S21',
  category: 'Electronics',
  subcategory: 'Smartphones',
  unit_price: 45999.00
}
```

**dim_customer:**
```sql
{
  customer_key: 12,
  customer_id: 'C001',
  customer_name: 'Rahul Sharma',
  city: 'Bangalore',
  state: 'Karnataka',
  customer_segment: 'High Value'
}
```

This structure allows analysts to easily join fact_sales with any dimension to answer questions like "What products did Rahul Sharma buy in Q1 2024?" or "What was the total sales in Bangalore in January?"
