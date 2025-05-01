# nodes/search_documents.py

from retriever.async_vectordb_rerank_law import search_documents as search_law_docs
from retriever.async_vectordb_rerank_exam import search_documents as search_exam_docs
from state.schema import RAGState
import asyncio

async def async_search_documents(state: RAGState) -> RAGState:
    query = state.query
    top_k = getattr(state, "top_k", 5)

    # 병렬 실행
    law_task = asyncio.create_task(search_law_docs(query, top_k=top_k))
    exam_task = asyncio.create_task(search_exam_docs(query, top_k=top_k))

    law_docs, exam_docs = await asyncio.gather(law_task, exam_task)

    return state.model_copy(update={
        "retrieved_docs": {
            "law": law_docs,
            "exam": exam_docs
        }
    })
