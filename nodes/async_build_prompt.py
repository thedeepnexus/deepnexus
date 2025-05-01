# nodes/async_build_prompt.py

from utils.async_prompt import async_build_prompt_all
from state.schema import RAGState

async def async_build_prompt(state: RAGState) -> RAGState:
    query = state.query
    law_docs = state.reranked_docs["law"]
    exam_docs = state.reranked_docs["exam"]

    prompt = await async_build_prompt_all(query, law_docs, exam_docs)
    return state.model_copy(update={"prompt": prompt})
