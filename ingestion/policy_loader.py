from pypdf import PdfReader
from pathlib import Path
def extract_policy_pages(path):
    if not Path(path).is_file():
        raise FileNotFoundError(f"Policy PDF not found: {path}")
    reader = PdfReader(str(path))
    pages=[]
    for page_no,page in enumerate(reader.pages, start=1):
        text=" ".join((page.extract_text() or "").split())
        if text: pages.append({"text":text,"page":page_no,"source":str(path.name)})
    if not pages:
        raise ValueError(f"Policy PDF contains no extractable text: {path}")
    return pages
