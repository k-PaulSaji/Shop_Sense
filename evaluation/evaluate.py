import json
from pathlib import Path
from config import CATALOG_PATH,POLICY_PATH,TEST_QUERIES_PATH
from ingestion.catalog_loader import load_catalog
from ingestion.policy_loader import extract_policy_pages
from ingestion.chunking import chunk_pages
from retrieval.embeddings import SemanticEncoder
from retrieval.hybrid_search import HybridSearch
from generation.answer_generator import AnswerGenerator
def build_engine():
    catalog=load_catalog(CATALOG_PATH)
    pages=extract_policy_pages(POLICY_PATH); chunks=chunk_pages(pages)
    docs=[{"text":f"{r['name']} {r['category']} {r['spec_1']} {r['spec_2']} {r['description']}","kind":"catalog","sku":r["sku"]} for _,r in catalog.iterrows()]+chunks
    index=SemanticEncoder([d["text"] for d in docs])
    hybrid=HybridSearch(catalog,index,docs)
    return AnswerGenerator(catalog,chunks,hybrid)
def run():
    engine=build_engine()
    tests=[json.loads(x) for x in open(TEST_QUERIES_PATH,encoding="utf-8") if x.strip()]
    tests += [
      {"question":"Find an in-stock laptop under INR 70000 with at least 16GB RAM","expected":"L102"},
      {"question":"Show a 27-inch monitor below INR 15000","expected":"M204"},
      {"question":"Can I buy the 32-inch 4K monitor now?","expected":"M203"},
      {"question":"What warranty comes with a laptop?","expected":"12-month"},
      {"question":"Is accidental damage covered by laptop warranty?","expected":"excluded"},
      {"question":"Find a mechanical keyboard below INR 4000","expected":"K402"},
      {"question":"Find a mechanical keyboard below INR 3000","expected":"No matching product"}
    ]
    results=[]
    for t in tests:
        actual=engine.answer(t["question"])
        expected=t["expected"]
        if "M203" in expected: passed="M203" in actual["answer"] and "out of stock" in actual["answer"].lower()
        elif expected in ("None","No matching product"): passed="No matching product" in actual["answer"]
        elif expected=="Not returnable unless defective": passed="cannot be returned unless" in actual["answer"].lower()
        else: passed=expected.lower() in actual["answer"].lower()
        results.append({"question":t["question"],"expected":expected,"actual":actual["answer"],"sources":actual["sources"],"passed":passed})
    Path("evaluation").mkdir(exist_ok=True)
    Path("evaluation/results.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Evaluation: {sum(r['passed'] for r in results)}/{len(results)} passed")
    for r in results: print("PASS" if r["passed"] else "CHECK",r["question"],"->",r["expected"])
if __name__=="__main__": run()
