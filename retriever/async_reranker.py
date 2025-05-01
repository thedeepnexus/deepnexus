# retriever/async_reranker.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import asyncio

# 🚀 비동기용 Reranker 모델 로딩
async_reranker_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-base")
async_reranker_model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-base")

async def async_rerank_documents(query: str, docs: list, top_k: int = 5) -> list:
    """
    검색된 문서 리스트를 Query와 비교해서 relevance 순서로 비동기 재정렬한다.
    """
    pairs = [(query, doc) for doc in docs]

    def _sync_rerank():
        inputs = async_reranker_tokenizer.batch_encode_plus(
            pairs,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        )

        with torch.no_grad():
            scores = async_reranker_model(**inputs).logits.squeeze(-1)

        scores_list = scores.tolist()
        sorted_docs = [
            doc for _, doc in sorted(zip(scores_list, docs), key=lambda x: x[0], reverse=True)
        ]
        return sorted_docs[:top_k]

    return await asyncio.to_thread(_sync_rerank)
