from utils.cache import cache_response
from type.state_schema import RAGState

def save_response(state: RAGState) -> RAGState:
    query = state.query
    top_k = getattr(state, "top_k", 5)
    response = state.final_response

    cache_response(query, top_k, response)
    return state  # 변경 없음
