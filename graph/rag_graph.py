# graph/rag_graph.py

from langgraph.graph import StateGraph, START, END
from nodes.async_check_cache import async_check_cache
from nodes.async_search_documents import async_search_documents
from nodes.async_rerank_documents import async_rerank_documents
from nodes.async_build_prompt import async_build_prompt
from nodes.async_call_llm import async_call_llm
from nodes.async_save_response import async_save_response
from state.schema import RAGState

def get_async_rag_pipeline():
    workflow = StateGraph(RAGState)

    # 노드 등록 (모두 async 함수)
    workflow.add_node("CheckCache", async_check_cache)
    workflow.add_node("SearchDocs", async_search_documents)
    workflow.add_node("Rerank", async_rerank_documents)
    workflow.add_node("BuildPrompt", async_build_prompt)
    workflow.add_node("CallLLM", async_call_llm)
    workflow.add_node("SaveResponse", async_save_response)

    # 시작 노드
    workflow.set_entry_point("CheckCache")

    # 조건 분기: 캐시 여부
    workflow.add_conditional_edges(
        "CheckCache",
        lambda state: "Return" if state.cached_response else "SearchDocs",
        {"Return": END, "SearchDocs": "SearchDocs"}
    )

    # 일반 흐름
    workflow.add_edge("SearchDocs", "Rerank")
    workflow.add_edge("Rerank", "BuildPrompt")
    workflow.add_edge("BuildPrompt", "CallLLM")
    workflow.add_edge("CallLLM", "SaveResponse")
    workflow.add_edge("SaveResponse", END)

    return workflow.compile()
