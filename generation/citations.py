def catalog_citation(row):
    return f"Catalog source: G2_catalog.csv — SKU {row['sku']}"


def policy_citation(chunk):
    return f"Policy source: {chunk['source']}, page {chunk['page']}"
