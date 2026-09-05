-- PRIMEOR SOLUTIONS
-- Level 2: DATA ANALYSIS (SQL)
-- E-Commerce Dataset
-- Recommended DBMS: MySQL 8+

CREATE DATABASE IF NOT EXISTS ecommerce_analysis;
USE ecommerce_analysis;

-- 1. Create table
CREATE TABLE IF NOT EXISTS ecommerce_data (
    order_id VARCHAR(50),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_name VARCHAR(150),
    segment VARCHAR(50),
    state VARCHAR(100),
    country VARCHAR(100),
    market VARCHAR(50),
    region VARCHAR(100),
    product_id VARCHAR(50),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    product_name VARCHAR(255),
    sales DECIMAL(14,2),
    quantity INT,
    discount DECIMAL(6,3),
    profit DECIMAL(14,4),
    shipping_cost DECIMAL(14,2),
    order_priority VARCHAR(50),
    year INT
);

-- Import the cleaned Excel/CSV data into ecommerce_data.
-- In MySQL Workbench, use Table Data Import Wizard for the Excel/CSV file.

-- 2. Top 10 profitable products
SELECT product_name, SUM(profit) AS total_profit
FROM ecommerce_data
GROUP BY product_name
ORDER BY total_profit DESC
LIMIT 10;

-- 3. Top 10 customers by sales
SELECT customer_name, SUM(sales) AS total_sales
FROM ecommerce_data
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;

-- 4. Region-wise total sales
SELECT region, SUM(sales) AS total_sales
FROM ecommerce_data
GROUP BY region
ORDER BY total_sales DESC;

-- 5. Category-wise average profit
SELECT category,
       ROUND(AVG(profit), 2) AS average_profit,
       ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_data
GROUP BY category
ORDER BY average_profit DESC;

-- 6. Highest discount category
SELECT category,
       ROUND(AVG(discount) * 100, 2) AS average_discount_percent
FROM ecommerce_data
GROUP BY category
ORDER BY average_discount_percent DESC
LIMIT 1;

-- 7. Orders with negative profit
SELECT order_id, product_name, category, sales, discount, profit
FROM ecommerce_data
WHERE profit < 0
ORDER BY profit ASC;

-- Count of negative-profit records
SELECT COUNT(*) AS negative_profit_records
FROM ecommerce_data
WHERE profit < 0;

-- 8. Monthly sales trend
SELECT YEAR(order_date) AS order_year,
       MONTH(order_date) AS order_month,
       ROUND(SUM(sales), 2) AS total_sales
FROM ecommerce_data
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY order_year, order_month;

-- 9. Market-wise revenue analysis
SELECT market,
       ROUND(SUM(sales), 2) AS total_revenue,
       ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_data
GROUP BY market
ORDER BY total_revenue DESC;

-- 10. Top-performing sub-categories
SELECT sub_category,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_data
GROUP BY sub_category
ORDER BY total_profit DESC;

-- 11. Ship mode usage analysis
SELECT ship_mode,
       COUNT(*) AS order_lines,
       COUNT(DISTINCT order_id) AS unique_orders
FROM ecommerce_data
GROUP BY ship_mode
ORDER BY unique_orders DESC;

-- ---------- Advanced Level 2 analysis ----------

-- 12. Profit margin by category
SELECT category,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2) AS profit_margin_percent
FROM ecommerce_data
GROUP BY category
ORDER BY profit_margin_percent DESC;

-- 13. Top 10 products by profit margin
SELECT product_name,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2) AS profit_margin_percent
FROM ecommerce_data
GROUP BY product_name
HAVING SUM(sales) > 0
ORDER BY profit_margin_percent DESC
LIMIT 10;

-- 14. Year-wise sales and profit
SELECT year,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_data
GROUP BY year
ORDER BY year;

-- 15. Segment-wise performance
SELECT segment,
       COUNT(DISTINCT order_id) AS total_orders,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_data
GROUP BY segment
ORDER BY total_sales DESC;

-- 16. High-discount, loss-making records
SELECT product_name, category, discount, sales, profit
FROM ecommerce_data
WHERE discount >= 0.50
  AND profit < 0
ORDER BY profit ASC;

-- 17. Region + category performance
SELECT region, category,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_data
GROUP BY region, category
ORDER BY total_profit DESC;

-- 18. Average order value
SELECT ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2)
       AS average_order_value
FROM ecommerce_data;

-- 19. Customer purchase frequency
SELECT customer_name,
       COUNT(DISTINCT order_id) AS number_of_orders,
       ROUND(SUM(sales), 2) AS total_sales
FROM ecommerce_data
GROUP BY customer_name
ORDER BY number_of_orders DESC;

-- 20. Most profitable region
SELECT region, ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_data
GROUP BY region
ORDER BY total_profit DESC
LIMIT 1;
