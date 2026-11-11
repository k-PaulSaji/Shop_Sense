from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CATALOG_PATH = DATA_DIR / "G2_catalog.csv"
POLICY_PATH = DATA_DIR / "G2_store_policy.pdf"
TEST_QUERIES_PATH = DATA_DIR / "G2_test_queries.jsonl"
DATABASE_PATH = BASE_DIR / "database" / "shopsense.db"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
