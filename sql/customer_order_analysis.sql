-- Overall business KPIs
WITH order_summary AS (
    SELECT
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers,
        ROUND(SUM(revenue_eur), 2) AS total_revenue,
        ROUND(SUM(revenue_eur) / COUNT(DISTINCT order_id), 2) AS average_order_value
    FROM orders
)
SELECT * FROM order_summary;

-- Top 10 customers by revenue
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.revenue_eur), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_revenue DESC
LIMIT 10;

-- Repeat customer analysis
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(revenue_eur) AS customer_revenue
    FROM orders
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-time customer'
        ELSE 'Repeat customer'
    END AS customer_type,
    COUNT(*) AS customer_count,
    ROUND(SUM(customer_revenue), 2) AS total_revenue,
    ROUND(SUM(customer_revenue) * 100.0 / (SELECT SUM(revenue_eur) FROM orders), 2) AS revenue_share_pct
FROM customer_orders
GROUP BY customer_type;

-- Revenue by product category
SELECT
    p.product_category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.revenue_eur), 2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_category
ORDER BY total_revenue DESC;

-- Top 10 products by revenue
SELECT
    p.product_name,
    p.product_category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.revenue_eur), 2) AS total_revenue,
    RANK() OVER (ORDER BY SUM(o.revenue_eur) DESC) AS revenue_rank
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.product_category
ORDER BY total_revenue DESC
LIMIT 10;

-- Monthly revenue and orders
SELECT
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND(SUM(revenue_eur), 2) AS total_revenue
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- Customer retention by signup cohort
SELECT
    strftime('%Y-%m', c.signup_date) AS signup_month,
    COUNT(DISTINCT c.customer_id) AS customers_acquired,
    COUNT(DISTINCT CASE WHEN strftime('%Y-%m', o.order_date) > strftime('%Y-%m', c.signup_date) THEN c.customer_id END) AS returning_customers,
    ROUND(COUNT(DISTINCT CASE WHEN strftime('%Y-%m', o.order_date) > strftime('%Y-%m', c.signup_date) THEN c.customer_id END) * 100.0 / COUNT(DISTINCT c.customer_id), 2) AS retention_rate_pct
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY signup_month
ORDER BY signup_month;
