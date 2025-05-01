# nodes/async_rerank_documents.py

import asyncio
from retriever.async_reranker import async_rerank_documents as sync_rerank_fn
from state.schema import RAGState

async def async_rerank_documents(state: RAGState) -> RAGState:
    query = state.query
    law = state.retrieved_docs["law"]
    exam = state.retrieved_docs["exam"]

    law_docs = [doc for doc, _, _ in law]
    exam_docs = [doc for doc, _, _ in exam]

    # 비동기로 동기 함수 병렬 실행
    law_reranked, exam_reranked = await asyncio.gather(
        asyncio.to_thread(sync_rerank_fn, query, law_docs, 5),
        asyncio.to_thread(sync_rerank_fn, query, exam_docs, 5)
    )

    return state.model_copy(update={
        "reranked_docs": {
            "law": law_reranked,
            "exam": exam_reranked
        }
    })
