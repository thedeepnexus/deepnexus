from retriever.vectordb_rerank_law import search_documents as search_law
from retriever.vectordb_rerank_exam import search_documents as search_exam

def search_law_docs(query, top_k=5):
    return search_law(query, top_k=top_k)

def search_exam_docs(query, top_k=5):
    return search_exam(query, top_k=top_k)
