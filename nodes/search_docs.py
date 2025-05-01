from retriever.vectordb_rerank_law import search_documents as search_law_docs
from retriever.vectordb_rerank_exam import search_documents as search_exam_docs
from type.state_schema import RAGState

def search_documents(state: RAGState) -> RAGState:
    query = state.query
    top_k = getattr(state, "top_k", 5)

    law_docs = search_law_docs(query, top_k=top_k)
    exam_docs = search_exam_docs(query, top_k=top_k)

    return state.model_copy(update={
        "retrieved_docs": {
            "law": law_docs,
            "exam": exam_docs
        }
    })
