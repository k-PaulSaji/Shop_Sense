import pandas as pd
from pathlib import Path
REQUIRED = {"sku","name","category","spec_1","spec_2","price_inr","in_stock","description"}
def load_catalog(path):
    if not Path(path).is_file():
        raise FileNotFoundError(f"Catalog file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing: raise ValueError(f"Catalog missing columns: {sorted(missing)}")
    if df.empty: raise ValueError("Catalog contains no products")
    if df[list(REQUIRED)].isna().any().any(): raise ValueError("Catalog contains blank required values")
    df["sku"] = df["sku"].astype(str).str.strip()
    if (df["sku"] == "").any(): raise ValueError("Catalog contains an empty SKU")
    for column in ("name", "category", "spec_1", "spec_2", "description"):
        df[column] = df[column].astype(str).str.strip()
    df["price_inr"] = pd.to_numeric(df["price_inr"], errors="raise")
    if (df["price_inr"] < 0).any(): raise ValueError("price_inr cannot be negative")
    df["in_stock"] = pd.to_numeric(df["in_stock"], errors="raise").astype(int)
    if not df["in_stock"].isin([0,1]).all(): raise ValueError("in_stock must be 0 or 1")
    if df["sku"].duplicated().any(): raise ValueError("Duplicate SKU found")
    return df
