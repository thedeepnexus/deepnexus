# rag_pipeline_graph/graph.py
from langgraph.graph import StateGraph, START, END
from nodes.check_cache import check_cache
from nodes.search_docs import search_documents
from nodes.rerank import rerank_documents
from nodes.build_prompt import build_prompt
from nodes.call_llm import call_llm
from nodes.cache_save import save_response
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from type.state_schema import RAGState

# class RAGState(BaseModel):
#     query: str
#     top_k: int = 5
#     cached_response: Optional[str] = None
#     retrieved_docs: List[Dict[str, Any]] = []
#     reranked_docs: List[Dict[str, Any]] = []
#     prompt: str = ""
#     final_response: str = ""

def get_rag_pipeline_graph():
    workflow = StateGraph(RAGState)

    # 노드 등록
    workflow.add_node("CheckCache", check_cache)
    workflow.add_node("SearchDocs", search_documents)
    workflow.add_node("Rerank", rerank_documents)
    workflow.add_node("BuildPrompt", build_prompt)
    workflow.add_node("CallLLM", call_llm)
    workflow.add_node("SaveResponse", save_response)

    # 흐름 구성
    workflow.set_entry_point("CheckCache")
    workflow.add_conditional_edges(
        "CheckCache",
        lambda state: "Return" if state.cached_response else "SearchDocs",
        {"Return": END, "SearchDocs": "SearchDocs"}
    )

    workflow.add_edge("SearchDocs", "Rerank")
    workflow.add_edge("Rerank", "BuildPrompt")
    workflow.add_edge("BuildPrompt", "CallLLM")
    workflow.add_edge("CallLLM", "SaveResponse")
    workflow.add_edge("SaveResponse", END)

    return workflow.compile()

if __name__ == "__main__":
    graph = get_rag_pipeline_graph()

    input_data = RAGState(
        query="공인중개사법령상 중개사무소의 개설등록에 관한 설명",
        top_k=5
    )

    final_state = graph.invoke(input_data)
    # print("\n🧠 최종 응답:", final_state.final_response)
    # print("\n🧠 최종 응답:", final_state["final_response"])
    print("\n🧠 최종 응답:", final_state.get("final_response", "[응답 없음]"))

