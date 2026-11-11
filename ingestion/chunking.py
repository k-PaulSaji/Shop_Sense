def chunk_pages(pages, chunk_words=110, overlap=20):
    chunks=[]
    for page in pages:
        words=page["text"].split()
        start=0
        while start < len(words):
            piece=" ".join(words[start:start+chunk_words])
            if piece:
                chunks.append({"text":piece,"page":page["page"],"source":page["source"],"kind":"policy"})
            start += max(1, chunk_words-overlap)
    return chunks
