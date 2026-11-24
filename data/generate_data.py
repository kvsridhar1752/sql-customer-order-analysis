import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(21)
Path("data").mkdir(exist_ok=True)

conn = sqlite3.connect("retail.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT,
    city TEXT,
    signup_date TEXT
);

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    product_category TEXT,
    unit_price_eur REAL
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    product_id TEXT,
    order_date TEXT,
    quantity INTEGER,
    revenue_eur REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

n_customers = 800
customer_ids = [f"CUST{i:04d}" for i in range(1, n_customers + 1)]
cities = ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"]
first_names = ["Anna", "Lukas", "Sofia", "Jonas", "Mia", "Ethan", "Emma", "Noah"]
last_names = ["Meyer", "Schmidt", "Weber", "Fischer", "Wagner", "Becker"]

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "customer_name": [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_customers)],
    "city": np.random.choice(cities, n_customers),
    "signup_date": (pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 365, n_customers), unit="D")).strftime("%Y-%m-%d")
})

products = pd.DataFrame({
    "product_id": [f"P{i:03d}" for i in range(1, 21)],
    "product_name": [f"Product {i}" for i in range(1, 21)],
    "product_category": np.random.choice(["Electronics", "Clothing", "Home", "Beauty", "Sports"], 20),
    "unit_price_eur": np.round(np.random.uniform(8, 250, 20), 2)
})

n_orders = 5000
order_customer = np.random.choice(customer_ids, n_orders, p=np.random.dirichlet(np.ones(n_customers) * 0.4))
order_product = np.random.choice(products["product_id"], n_orders)
order_dates = (pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 365, n_orders), unit="D")).strftime("%Y-%m-%d")
quantity = np.random.choice([1, 2, 3, 4], n_orders, p=[0.55, 0.25, 0.13, 0.07])

product_price = dict(zip(products["product_id"], products["unit_price_eur"]))
revenue = np.round(np.array([product_price[p] for p in order_product]) * quantity, 2)

orders = pd.DataFrame({
    "order_id": [f"ORD{i:06d}" for i in range(1, n_orders + 1)],
    "customer_id": order_customer,
    "product_id": order_product,
    "order_date": order_dates,
    "quantity": quantity,
    "revenue_eur": revenue
})

customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

conn.commit()
conn.close()
print("Created retail.db with 800 customers, 20 products, and 5,000 orders.")
