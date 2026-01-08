-- FlexiMart Data Warehouse Sample Data
-- Database: fleximart_dw

USE fleximart_dw;

-- ============================================================================
-- Populate dim_date (January-February 2024, 30 dates)
-- ============================================================================
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, FALSE),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, FALSE),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, FALSE),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, TRUE),
(20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, FALSE),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, FALSE),
(20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, FALSE),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, FALSE),
(20240116, '2024-01-16', 'Tuesday', 16, 1, 'January', 'Q1', 2024, FALSE),
(20240117, '2024-01-17', 'Wednesday', 17, 1, 'January', 'Q1', 2024, FALSE),
(20240118, '2024-01-18', 'Thursday', 18, 1, 'January', 'Q1', 2024, FALSE),
(20240119, '2024-01-19', 'Friday', 19, 1, 'January', 'Q1', 2024, FALSE),
(20240120, '2024-01-20', 'Saturday', 20, 1, 'January', 'Q1', 2024, TRUE),
(20240121, '2024-01-21', 'Sunday', 21, 1, 'January', 'Q1', 2024, TRUE),
(20240122, '2024-01-22', 'Monday', 22, 1, 'January', 'Q1', 2024, FALSE),
(20240123, '2024-01-23', 'Tuesday', 23, 1, 'January', 'Q1', 2024, FALSE),
(20240124, '2024-01-24', 'Wednesday', 24, 1, 'January', 'Q1', 2024, FALSE),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January', 'Q1', 2024, FALSE),
(20240126, '2024-01-26', 'Friday', 26, 1, 'January', 'Q1', 2024, FALSE),
(20240127, '2024-01-27', 'Saturday', 27, 1, 'January', 'Q1', 2024, TRUE),
(20240128, '2024-01-28', 'Sunday', 28, 1, 'January', 'Q1', 2024, TRUE),
(20240129, '2024-01-29', 'Monday', 29, 1, 'January', 'Q1', 2024, FALSE),
(20240130, '2024-01-30', 'Tuesday', 30, 1, 'January', 'Q1', 2024, FALSE),
(20240131, '2024-01-31', 'Wednesday', 31, 1, 'January', 'Q1', 2024, FALSE),
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, FALSE),
(20240202, '2024-02-02', 'Friday', 2, 2, 'February', 'Q1', 2024, FALSE),
(20240203, '2024-02-03', 'Saturday', 3, 2, 'February', 'Q1', 2024, TRUE);

-- ============================================================================
-- Populate dim_product (15 products across 3 categories)
-- ============================================================================
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001', 'Samsung Galaxy S21', 'Electronics', 'Smartphones', 45999.00),
('P002', 'Nike Running Shoes', 'Fashion', 'Footwear', 3499.00),
('P003', 'Apple MacBook Pro', 'Electronics', 'Laptops', 189999.00),
('P004', 'Levi''s Jeans', 'Fashion', 'Clothing', 2999.00),
('P005', 'Sony Headphones', 'Electronics', 'Audio', 1999.00),
('P006', 'Organic Almonds', 'Groceries', 'Dry Fruits', 899.00),
('P007', 'HP Laptop', 'Electronics', 'Laptops', 52999.00),
('P008', 'Adidas T-Shirt', 'Fashion', 'Clothing', 1299.00),
('P009', 'Basmati Rice 5kg', 'Groceries', 'Grains', 650.00),
('P010', 'OnePlus Nord', 'Electronics', 'Smartphones', 26999.00),
('P011', 'Puma Sneakers', 'Fashion', 'Footwear', 4599.00),
('P012', 'Dell Monitor 24inch', 'Electronics', 'Monitors', 12999.00),
('P013', 'Woodland Shoes', 'Fashion', 'Footwear', 5499.00),
('P014', 'iPhone 13', 'Electronics', 'Smartphones', 69999.00),
('P015', 'Organic Honey 500g', 'Groceries', 'Organic', 450.00);

-- ============================================================================
-- Populate dim_customer (12 customers across 4 cities)
-- ============================================================================
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001', 'Rahul Sharma', 'Bangalore', 'Karnataka', 'High Value'),
('C002', 'Priya Patel', 'Mumbai', 'Maharashtra', 'High Value'),
('C003', 'Amit Kumar', 'Delhi', 'Delhi', 'Medium Value'),
('C004', 'Sneha Reddy', 'Hyderabad', 'Telangana', 'Medium Value'),
('C005', 'Vikram Singh', 'Chennai', 'Tamil Nadu', 'High Value'),
('C006', 'Anjali Mehta', 'Bangalore', 'Karnataka', 'Medium Value'),
('C007', 'Ravi Verma', 'Pune', 'Maharashtra', 'Low Value'),
('C008', 'Pooja Iyer', 'Bangalore', 'Karnataka', 'Medium Value'),
('C009', 'Karthik Nair', 'Kochi', 'Kerala', 'Low Value'),
('C010', 'Deepa Gupta', 'Delhi', 'Delhi', 'High Value'),
('C011', 'Arjun Rao', 'Hyderabad', 'Telangana', 'High Value'),
('C012', 'Lakshmi Krishnan', 'Chennai', 'Tamil Nadu', 'Medium Value');

-- ============================================================================
-- Populate fact_sales (40 sales transactions)
-- ============================================================================
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- January 2024 Sales
(20240115, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240116, 4, 2, 2, 2999.00, 0.00, 5998.00),
(20240117, 7, 3, 1, 52999.00, 0.00, 52999.00),
(20240118, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240119, 9, 5, 3, 650.00, 0.00, 1950.00),
(20240120, 12, 6, 1, 12999.00, 0.00, 12999.00),
(20240121, 5, 7, 2, 1999.00, 0.00, 3998.00),
(20240122, 8, 8, 1, 1299.00, 0.00, 1299.00),
(20240123, 3, 9, 1, 189999.00, 5000.00, 184999.00),
(20240124, 2, 3, 1, 3499.00, 0.00, 3499.00),
(20240125, 6, 8, 5, 899.00, 0.00, 4495.00),
(20240126, 15, 9, 2, 450.00, 0.00, 900.00),
(20240127, 4, 10, 1, 2999.00, 0.00, 2999.00),
(20240128, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240129, 7, 4, 1, 52999.00, 0.00, 52999.00),
(20240130, 10, 5, 1, 26999.00, 0.00, 26999.00),
(20240131, 11, 6, 1, 4599.00, 0.00, 4599.00),
-- February 2024 Sales
(20240201, 14, 2, 1, 69999.00, 0.00, 69999.00),
(20240202, 3, 12, 1, 189999.00, 0.00, 189999.00),
(20240203, 15, 3, 3, 450.00, 0.00, 1350.00),
(20240115, 13, 4, 2, 5499.00, 0.00, 10998.00),
(20240116, 8, 5, 3, 1299.00, 0.00, 3897.00),
(20240117, 12, 7, 1, 12999.00, 0.00, 12999.00),
(20240118, 11, 8, 2, 4599.00, 0.00, 9198.00),
(20240119, 9, 9, 10, 650.00, 0.00, 6500.00),
(20240120, 10, 10, 1, 26999.00, 0.00, 26999.00),
(20240121, 4, 11, 2, 2999.00, 0.00, 5998.00),
(20240122, 2, 3, 1, 3499.00, 0.00, 3499.00),
(20240123, 5, 4, 4, 899.00, 0.00, 3596.00),
(20240124, 9, 5, 5, 650.00, 0.00, 3250.00),
(20240125, 4, 3, 1, 2999.00, 0.00, 2999.00),
(20240126, 11, 6, 1, 4599.00, 0.00, 4599.00),
(20240127, 5, 7, 2, 1999.00, 0.00, 3998.00),
(20240128, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240129, 7, 2, 1, 52999.00, 0.00, 52999.00),
(20240130, 4, 3, 2, 2999.00, 0.00, 5998.00),
(20240131, 14, 6, 1, 69999.00, 0.00, 69999.00),
(20240201, 12, 11, 1, 12999.00, 0.00, 12999.00),
(20240202, 12, 12, 1, 12999.00, 0.00, 12999.00),
(20240203, 5, 3, 2, 1999.00, 0.00, 3998.00);
