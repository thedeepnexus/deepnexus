# rag_pipeline_graph/graph.py
from langgraph.graph import StateGraph, START, END
from nodes.check_cache import async_check_cache
from nodes.search_docs import async_search_documents
from nodes.rerank import async_rerank_documents
from nodes.build_prompt import async_build_prompt
from nodes.call_llm import async_call_llm
from nodes.cache_save import async_save_response
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from type.state_schema import RAGState

from langgraph.graph import StateGraph
from nodes import *  # 노드들을 비동기로 구현
import asyncio

async def get_async_rag_pipeline():
    workflow = StateGraph(RAGState)
    
    # 비동기 노드 등록
    workflow.add_node("CheckCache", async_check_cache)
    workflow.add_node("SearchDocs", async_search_documents)
    workflow.add_node("Rerank", async_rerank_documents)
    workflow.add_node("BuildPrompt", async_build_prompt)
    workflow.add_node("CallLLM", async_call_llm)
    workflow.add_node("SaveResponse", async_save_response)
    
    # 흐름 구성 (기존과 동일)
    workflow.set_entry_point("CheckCache")
    workflow.add_conditional_edges(
        "CheckCache",
        lambda state: "Return" if state.cached_response else "SearchDocs",
        {"Return": END, "SearchDocs": "SearchDocs"}
    )
    # ... 나머지 엣지 추가
    
    return workflow.compile()

async def async_main():
    graph = await get_async_rag_pipeline()
    input_data = RAGState(query="공인중개사법령상 중개사무소의 개설등록에 관한 설명")
    final_state = await graph.ainvoke(input_data)
    print("\n🧠 최종 응답:", final_state.get("final_response", "[응답 없음]"))

if __name__ == "__main__":
    asyncio.run(async_main())
