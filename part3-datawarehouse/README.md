# Part 3: Data Warehouse and Analytics

## Overview

This part implements a star schema data warehouse for FlexiMart to enable analytical reporting and business intelligence. The warehouse uses a dimensional modeling approach optimized for OLAP (Online Analytical Processing) queries.

## Files

- `star_schema_design.md` - Complete star schema documentation with design decisions
- `warehouse_schema.sql` - SQL script to create the data warehouse schema
- `warehouse_data.sql` - Sample data for all dimension and fact tables
- `analytics_queries.sql` - OLAP queries for business analytics
- `README.md` - This file

## Schema Structure

### Fact Table
- **fact_sales**: Transaction-level sales data with measures (quantity, price, amount)

### Dimension Tables
- **dim_date**: Time dimension for temporal analysis
- **dim_product**: Product dimension with category information
- **dim_customer**: Customer dimension with geographic and segmentation data

## Setup Instructions

### 1. Create Database

```bash
mysql -u root -p < warehouse_schema.sql
```

### 2. Load Sample Data

```bash
mysql -u root -p fleximart_dw < warehouse_data.sql
```

### 3. Run Analytics Queries

```bash
mysql -u root -p fleximart_dw < analytics_queries.sql
```

Or run queries individually in MySQL client:

```sql
USE fleximart_dw;
-- Copy and paste queries from analytics_queries.sql
```

## Analytics Queries

### Query 1: Monthly Sales Drill-Down
Demonstrates time-based analysis with drill-down capability from year → quarter → month. Shows total orders, quantity, and sales for each time period.

### Query 2: Top 10 Products by Revenue
Identifies best-performing products with revenue contribution percentage. Uses window functions to calculate percentage of total revenue.

### Query 3: Customer Segmentation
Segments customers into High/Medium/Low value categories based on total spending. Provides counts and revenue statistics for each segment.

## Key Features

- **Star Schema Design**: Optimized for analytical queries with denormalized dimensions
- **Surrogate Keys**: Integer keys for better join performance
- **Time Dimension**: Enables flexible time-based analysis and drill-downs
- **OLAP Queries**: Demonstrates aggregation, window functions, and CTEs

## Data Volume

- **dim_date**: 30 dates (January-February 2024)
- **dim_product**: 15 products across 3 categories
- **dim_customer**: 12 customers across 4 cities
- **fact_sales**: 40 sales transactions
