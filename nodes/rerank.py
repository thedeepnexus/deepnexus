from retriever.reranker import rerank_documents as rerank_fn
from state.schema import RAGState  # Optional: for type hint

def rerank_documents(state: RAGState) -> RAGState:
    query = state.query
    law = state.retrieved_docs["law"]
    exam = state.retrieved_docs["exam"]

    law_reranked = rerank_fn(query, [doc for doc, _, _ in law], top_k=5)
    exam_reranked = rerank_fn(query, [doc for doc, _, _ in exam], top_k=5)

    return state.model_copy(update={
        "reranked_docs": {
            "law": law_reranked,
            "exam": exam_reranked
        }
    })
