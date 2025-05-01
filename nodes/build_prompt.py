from utils.prompt import build_prompt_all
from type.state_schema import RAGState  # optional for type hint

def build_prompt(state: RAGState) -> RAGState:
    query = state.query
    law_docs = state.reranked_docs["law"]
    exam_docs = state.reranked_docs["exam"]

    prompt = build_prompt_all(query, law_docs, exam_docs)
    return state.model_copy(update={"prompt": prompt})
