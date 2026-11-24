import sqlite3
import pandas as pd
from pathlib import Path

Path("output").mkdir(exist_ok=True)
conn = sqlite3.connect("retail.db")

queries = {
    "overall_kpis": """
        SELECT COUNT(DISTINCT order_id) AS total_orders,
               COUNT(DISTINCT customer_id) AS total_customers,
               ROUND(SUM(revenue_eur), 2) AS total_revenue,
               ROUND(SUM(revenue_eur) / COUNT(DISTINCT order_id), 2) AS average_order_value
        FROM orders;
    """,
    "top_customers": """
        SELECT c.customer_id, c.customer_name, c.city,
               COUNT(o.order_id) AS total_orders,
               ROUND(SUM(o.revenue_eur), 2) AS total_revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name, c.city
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "customer_type": """
        WITH customer_orders AS (
            SELECT customer_id,
                   COUNT(DISTINCT order_id) AS order_count,
                   SUM(revenue_eur) AS customer_revenue
            FROM orders
            GROUP BY customer_id
        )
        SELECT CASE WHEN order_count = 1 THEN 'One-time customer' ELSE 'Repeat customer' END AS customer_type,
               COUNT(*) AS customer_count,
               ROUND(SUM(customer_revenue), 2) AS total_revenue,
               ROUND(SUM(customer_revenue) * 100.0 / (SELECT SUM(revenue_eur) FROM orders), 2) AS revenue_share_pct
        FROM customer_orders
        GROUP BY customer_type;
    """,
    "category_performance": """
        SELECT p.product_category,
               COUNT(o.order_id) AS total_orders,
               SUM(o.quantity) AS units_sold,
               ROUND(SUM(o.revenue_eur), 2) AS total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_category
        ORDER BY total_revenue DESC;
    """,
    "monthly_performance": """
        SELECT strftime('%Y-%m', order_date) AS order_month,
               COUNT(DISTINCT order_id) AS total_orders,
               COUNT(DISTINCT customer_id) AS active_customers,
               ROUND(SUM(revenue_eur), 2) AS total_revenue
        FROM orders
        GROUP BY order_month
        ORDER BY order_month;
    """
}

results = []
for name, query in queries.items():
    df = pd.read_sql_query(query, conn)
    df.insert(0, "analysis", name)
    results.append(df)

pd.concat(results, ignore_index=True).to_csv("output/sql_results.csv", index=False)
conn.close()
print("Saved SQL analysis results to output/sql_results.csv.")
