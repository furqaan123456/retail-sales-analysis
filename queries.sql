-- Retail Sales Analysis: PostgreSQL / SQLite-friendly queries
-- Table: retail_sales(order_id, order_date, customer_id, region, category, product, quantity, discount, sales, profit)

-- 1. Headline KPIs
SELECT SUM(sales) AS total_sales, SUM(profit) AS total_profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margin_pct,
       COUNT(DISTINCT order_id) AS orders, COUNT(DISTINCT customer_id) AS customers
FROM retail_sales;

-- 2. Best-selling products
SELECT product, SUM(sales) AS sales, SUM(profit) AS profit, SUM(quantity) AS units
FROM retail_sales GROUP BY product ORDER BY sales DESC LIMIT 10;

-- 3. Regional performance
SELECT region, SUM(sales) AS sales, SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margin_pct
FROM retail_sales GROUP BY region ORDER BY sales DESC;

-- 4. Monthly sales trend with month-over-month growth
WITH m AS (
  SELECT SUBSTR(order_date, 1, 7) AS month, SUM(sales) AS sales
  FROM retail_sales GROUP BY 1)
SELECT month, sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month), 1) AS mom_pct
FROM m ORDER BY month;

-- 5. Does discounting hurt profit?
SELECT discount, COUNT(*) AS orders, SUM(profit) AS profit
FROM retail_sales GROUP BY discount ORDER BY discount;

-- 6. Top 10 customers by lifetime value
SELECT customer_id, COUNT(*) AS orders, SUM(sales) AS sales
FROM retail_sales GROUP BY customer_id ORDER BY sales DESC LIMIT 10;
