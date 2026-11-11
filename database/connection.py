import sqlite3
from pathlib import Path
def initialize_database(path, dataframe):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(path) as conn:
        dataframe.to_sql("products",conn,if_exists="replace",index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku)")
    return path
