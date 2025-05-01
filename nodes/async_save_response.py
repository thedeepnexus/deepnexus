# nodes/async_save_cache.py

from utils.async_cache import async_cache_response
from state.schema import RAGState

async def async_save_response(state: RAGState) -> RAGState:
    query = state.query
    top_k = getattr(state, "top_k", 5)
    response = state.final_response

    await async_cache_response(query, top_k, response)
    return state
