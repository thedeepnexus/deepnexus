import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from retriever.reranker import rerank_documents

# 1. 임베딩 모델 로드
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 2. 벡터DB (FAISS Index) 초기화
INDEX_PATH = "data/index/index.faiss"
DOCS_PATH = "data/index/docs.npy"

if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
    index = faiss.read_index(INDEX_PATH)
    documents = np.load(DOCS_PATH, allow_pickle=True)
else:
    index = None
    documents = None
    print("No FAISS index or docs found. Please build the index first.")

# 3. 검색 함수
def search_documents(query: str, top_k: int = 5):
    if index is None or documents is None:
        raise ValueError("Index or documents not loaded. Build the FAISS index first.")
    
    # 1. FAISS rough 검색
    query_embedding = embedding_model.encode([query], convert_to_tensor=True).cpu().detach().numpy()
    distances, indices = index.search(query_embedding, top_k)
    results = [documents[idx] for idx in indices[0] if idx != -1]

    # 2. Reranking 적용
    reranked_results = rerank_documents(query, results, top_k=top_k)

    return reranked_results


