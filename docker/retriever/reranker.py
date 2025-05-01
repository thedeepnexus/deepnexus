from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 1. Reranker 모델 로딩
reranker_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-base")
reranker_model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-base")

def rerank_documents(query: str, docs: list, top_k: int = 5) -> list:
    """
    검색된 문서 리스트를 Query와 비교해서 relevance 순서로 재정렬한다.
    """
    pairs = [(query, doc) for doc in docs]
    
    inputs = reranker_tokenizer.batch_encode_plus(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512
    )
    
    with torch.no_grad():
        scores = reranker_model(**inputs).logits.squeeze(-1)  # (batch_size,)
    
    scores = scores.tolist()
    
    # 점수 높은 순서대로 정렬
    sorted_docs = [doc for _, doc in sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)]
    
    return sorted_docs[:top_k]
