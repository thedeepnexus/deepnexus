import faiss
import numpy as np

INDEX_PATH = "data/index/index.faiss"
DOCS_PATH = "data/index/docs.npy"

# 인덱스 로딩
index = faiss.read_index(INDEX_PATH)
print(f"✅ FAISS Index Loaded! Size: {index.ntotal} vectors")

# 문서 로딩
documents = np.load(DOCS_PATH, allow_pickle=True)
print(f"✅ Documents Loaded! Count: {len(documents)} items")

# 일부 확인
print("▶️ Example document:", documents[0])

from retriever.vectordb import search_documents

query = "중개업자가 사무소를 옮겼을 때 필요한 조치"
top_k = 3

results = search_documents(query, top_k=top_k)

print("검색 결과:")
for idx, doc in enumerate(results, 1):
    print(f"{idx}. {doc}")
