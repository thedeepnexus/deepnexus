# vectordb_relank_law.py
import faiss
import numpy as np
import os
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from retriever.reranker import rerank_documents
from constants.embedding_models import embedding_models
# chroma vector config v2
 
# law_db config v2
CHROMA_PATH = os.path.abspath("data/index/exam_db")
COLLECTION_NAME = "exam_all"
EMBEDDING_MODEL_NAME = embedding_models[1]  # 사용하고자 하는 모델 선택

# 1. 임베딩 모델 로드 v2
# embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# 2. 임베딩 함수 설정
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)

# 3. Chroma 클라이언트 및 컬렉션 로드
client = PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)

# 4. 검색 함수
def search_documents(query: str, top_k: int = 5):
    print(f"\n🔍 검색어: '{query}'")
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # 문서 리스트만 추출
    docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]

    # Rerank 문서
    reranked_docs = rerank_documents(query, docs, top_k=top_k)

    reranked_data = []
    for doc in reranked_docs:
        idx = docs.index(doc)
        reranked_data.append((doc, metadatas[idx], distances[idx]))

    # for i, (doc, meta, dist) in enumerate(reranked_data):
    #     print(f"\n📄 결과 {i+1} (유사도: {1 - dist:.2f})")
    #     print(f"문서: {doc[:150]}...")
    #     print("메타데이터:")
    #     print(meta)

    return reranked_data  # 필요하면 리턴

    # for i, (doc, meta, dist) in enumerate(zip(
    #     results['documents'][0],
    #     results['metadatas'][0],
    #     results['distances'][0]
    # )):
    #     print(f"\n📄 결과 {i+1} (유사도: {1 - dist:.2f})")
    #     print(f"문서: {doc[:150]}...")
    #     print("메타데이터:")
    #     print(meta)