import sqlite3
def fetch_products(path):
    with sqlite3.connect(path) as conn:
        return conn.execute("SELECT * FROM products").fetchall()
