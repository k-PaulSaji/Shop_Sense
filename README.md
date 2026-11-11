# ShopSense

ShopSense is a Streamlit product discovery and store policy assistant. Product answers are generated from the supplied CSV and policy answers are generated from extractable text in the supplied PDF. Product price, stock, RAM, and screen-size requirements are applied as hard filters before semantic ranking.

## Requirements

- Windows 10/11
- Python 3.10 or 3.11 (64-bit)
- Internet access to install packages

The default search backend uses scikit-learn TF-IDF and runs locally without model downloads or API keys. ChromaDB is an optional persistent vector-store adapter; it is not needed to run the Streamlit app.

## Windows setup

Open PowerShell in the project directory (`D:\ShopSense`, or the directory where you cloned it):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No `.env` file or API key is required. Start the application from the project root:

```powershell
python -m streamlit run app.py
```

Then open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Run evaluation and tests

From the project root, with the virtual environment active:

```powershell
python -m evaluation.evaluate
python -m pytest -q
```

The evaluation command reads `data/G2_test_queries.jsonl`, runs the included additional evaluation cases, and writes `evaluation/results.json`.

## Data and behavior

- `data/G2_catalog.csv` is the source of product names, SKUs, category, specifications, INR prices, and stock flags.
- `data/G2_store_policy.pdf` is extracted page by page and split into overlapping chunks with page citations.
- `data/G2_test_queries.jsonl` contains the supplied query expectations.
- Product filters are strict: products over budget, out of stock when availability is requested, or lacking a requested RAM/screen-size value are excluded.
- The system abstains when it cannot find supporting policy text. It does not call an LLM.
- Stock and policy details reflect the supplied synthetic files and are not live store data.

The catalog and PDF remain the source data; the application does not rewrite them. The app caches its in-memory engine for the Streamlit session to avoid reloading and re-embedding the data on every interaction.

## Optional ChromaDB adapter

`retrieval/vector_store.py` provides a persistent ChromaDB collection builder for integrations that need it. It replaces the collection contents from the supplied documents to prevent stale catalog rows. The default application uses TF-IDF retrieval and does not create or depend on a Chroma database.

## Project layout

```text
app.py                 Streamlit interface
config.py              Project-relative data paths
data/                  Catalog, policy PDF, supplied queries
ingestion/              CSV validation and PDF extraction/chunking
retrieval/              TF-IDF semantic search, filters, Chroma adapter
generation/             Evidence-grounded response templates and citations
evaluation/             Evaluation runner and results
tests/                  Pytest suite
database/               SQLite helpers
requirements.txt        Python dependencies
```
