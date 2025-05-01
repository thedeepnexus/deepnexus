from utils.cache import get_cached_response

def check_cache(state):
    query = state.query
    top_k = getattr(state, "top_k", 5)
    cached = get_cached_response(query, top_k)

    if cached:
        return state.copy(update={
            "cached_response": cached,
            "final_response": cached
        })
    
    return state
