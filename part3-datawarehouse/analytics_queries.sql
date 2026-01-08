-- FlexiMart Data Warehouse Analytics Queries
-- Database: fleximart_dw

USE fleximart_dw;

-- ============================================================================
-- Query 1: Monthly Sales Drill-Down Analysis
-- ============================================================================
-- Business Scenario: "The CEO wants to see sales performance broken down by 
-- time periods. Start with yearly total, then quarterly, then monthly sales 
-- for 2024."
-- Demonstrates: Drill-down from Year to Quarter to Month

SELECT 
    d.year,
    d.quarter,
    d.month_name,
    COUNT(DISTINCT fs.sale_key) AS total_orders,
    -- Note: sale_key represents individual line items/transactions
    -- In a star schema with transaction-level grain, each sale_key is a unique transaction
    SUM(fs.quantity_sold) AS total_quantity,
    SUM(fs.total_amount) AS total_sales
FROM 
    fact_sales fs
    INNER JOIN dim_date d ON fs.date_key = d.date_key
WHERE 
    d.year = 2024
GROUP BY 
    d.year, d.quarter, d.month, d.month_name
ORDER BY 
    d.year, d.quarter, d.month;

-- ============================================================================
-- Query 2: Product Performance Analysis
-- ============================================================================
-- Business Scenario: "The product manager needs to identify top-performing 
-- products. Show the top 10 products by revenue, along with their category, 
-- total units sold, and revenue contribution percentage."
-- Includes: Revenue percentage calculation

WITH product_revenue AS (
    SELECT 
        p.product_name,
        p.category,
        SUM(fs.quantity_sold) AS units_sold,
        SUM(fs.total_amount) AS revenue
    FROM 
        fact_sales fs
        INNER JOIN dim_product p ON fs.product_key = p.product_key
    GROUP BY 
        p.product_key, p.product_name, p.category
),
total_revenue AS (
    SELECT SUM(revenue) AS grand_total
    FROM product_revenue
)
SELECT 
    pr.product_name,
    pr.category,
    pr.units_sold,
    pr.revenue,
    ROUND((pr.revenue / tr.grand_total * 100), 2) AS revenue_percentage
FROM 
    product_revenue pr
    CROSS JOIN total_revenue tr
ORDER BY 
    pr.revenue DESC
LIMIT 10;

-- ============================================================================
-- Query 3: Customer Segmentation Analysis
-- ============================================================================
-- Business Scenario: "Marketing wants to target high-value customers. 
-- Segment customers into 'High Value' (>₹50,000 spent), 'Medium Value' 
-- (₹20,000-₹50,000), and 'Low Value' (<₹20,000). Show count of customers 
-- and total revenue in each segment."
-- Segments: High/Medium/Low value customers

WITH customer_spending AS (
    SELECT 
        c.customer_key,
        c.customer_name,
        SUM(fs.total_amount) AS total_spent
    FROM 
        fact_sales fs
        INNER JOIN dim_customer c ON fs.customer_key = c.customer_key
    GROUP BY 
        c.customer_key, c.customer_name
),
customer_segments AS (
    SELECT 
        customer_key,
        customer_name,
        total_spent,
        CASE 
            WHEN total_spent > 50000 THEN 'High Value'
            WHEN total_spent >= 20000 AND total_spent <= 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS customer_segment
    FROM 
        customer_spending
)
SELECT 
    cs.customer_segment,
    COUNT(DISTINCT cs.customer_key) AS customer_count,
    SUM(cs.total_spent) AS total_revenue,
    ROUND(AVG(cs.total_spent), 2) AS avg_revenue
FROM 
    customer_segments cs
GROUP BY 
    cs.customer_segment
ORDER BY 
    CASE cs.customer_segment
        WHEN 'High Value' THEN 1
        WHEN 'Medium Value' THEN 2
        WHEN 'Low Value' THEN 3
    END;
