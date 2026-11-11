# Technical Report — ShopSense

## Objective
Build a hybrid shopping assistant that answers product and store-policy questions without inventing SKU, price, stock or specifications.

## Design decisions
- Pandas validates and loads the supplied CSV.
- SQLite provides structured catalog persistence.
- PyPDF extracts policy text while preserving page numbers.
- Sentence Transformers creates semantic embeddings; TF-IDF is the offline fallback.
- Product requests are filtered by exact constraints before semantic ranking.
- Policy questions retrieve PDF chunks and include page citations.
- Deterministic answer templates reduce unsupported claims; missing evidence triggers abstention.

## Limitations
Small synthetic dataset; English-oriented constraint parser; baseline does not call a generative LLM; Chroma persistence adapter is included but not yet connected to default flow.

## Improvements
1. Connect persistent Chroma collections and implement incremental re-indexing.
2. Add an LLM synthesis layer with strict structured output and citation entailment checks, retaining deterministic hard filters.
