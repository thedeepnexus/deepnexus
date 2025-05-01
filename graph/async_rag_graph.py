from langgraph.graph import StateGraph, END
from state.schema import RAGState
from nodes.async_check_cache import async_check_cache
from nodes.async_search_documents import async_search_documents
from nodes.async_rerank_documents import async_rerank_documents
from nodes.async_build_prompt import async_build_prompt
from nodes.async_call_llm import async_call_llm
from nodes.async_save_response import async_save_response

def get_async_rag_pipeline():
    graph = StateGraph(RAGState)

    graph.add_node("CheckCache", async_check_cache)
    graph.add_node("SearchDocs", async_search_documents)
    graph.add_node("Rerank", async_rerank_documents)
    graph.add_node("BuildPrompt", async_build_prompt)
    graph.add_node("CallLLM", async_call_llm)
    graph.add_node("SaveResponse", async_save_response)

    graph.set_entry_point("CheckCache")
    graph.add_conditional_edges(
        "CheckCache",
        lambda state: "Return" if state.cached_response else "SearchDocs",
        {"Return": END, "SearchDocs": "SearchDocs"}
    )
    graph.add_edge("SearchDocs", "Rerank")
    graph.add_edge("Rerank", "BuildPrompt")
    graph.add_edge("BuildPrompt", "CallLLM")
    graph.add_edge("CallLLM", "SaveResponse")
    graph.add_edge("SaveResponse", END)

    return graph.compile()
