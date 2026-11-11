"""Optional Chroma persistence adapter.
The baseline engine can run without Chroma; this module is provided for
persistent-vector-store extension and uses the same document metadata shape.
"""
def build_chroma_collection(documents, persist_directory):
    import chromadb
    client=chromadb.PersistentClient(path=str(persist_directory))
    # Rebuild from the supplied source of truth so changed or removed catalog
    # rows cannot survive as stale retrieval results.
    try:
        client.delete_collection("shopsense")
    except Exception:
        pass
    collection=client.create_collection("shopsense")
    if documents:
        collection.add(
            ids=[f"doc-{i}" for i in range(len(documents))],
            documents=[d["text"] for d in documents],
            metadatas=[{k:(v if isinstance(v,(str,int,float,bool)) else str(v)) for k,v in d.items() if k!="text"} for d in documents]
        )
    return collection
