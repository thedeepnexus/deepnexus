import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# 1. 데이터 경로 설정
source_paths = [
    r"data/real_estate_agent/raw/past_papers/brokerage_law.jsonl",
    r"data/real_estate_agent/raw/past_papers/civil_law.jsonl",
    r"data/real_estate_agent/raw/past_papers/disclosure_taxation.jsonl",
    r"data/real_estate_agent/raw/past_papers/introduction.jsonl",
    r"data/real_estate_agent/raw/past_papers/public_law.jsonl",
]

INDEX_PATH = "data/index/index.faiss"
DOCS_PATH = "data/index/docs.npy"

# 2. 임베딩 모델 로드
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def init_faiss():
    questions = []

    # 3. JSONL 파일 읽기
    for path in source_paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                question_text = data.get("question", "")
                if question_text:  # 질문이 비어있지 않으면 추가
                    questions.append(question_text)

    print(f"✅ 총 {len(questions)}개 질문 로딩 완료")

    # 4. 임베딩 생성
    embeddings = embedding_model.encode(
        questions, 
        batch_size=32, 
        show_progress_bar=True
    )
    embeddings = np.array(embeddings).astype('float32')

    # 5. FAISS 인덱스 생성
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 거리 기반 인덱스
    index.add(embeddings)

    # 6. 저장
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    np.save(DOCS_PATH, questions)

    print(f"✅ FAISS 인덱스와 문서 저장 완료!")

if __name__ == "__main__":
    init_faiss()
