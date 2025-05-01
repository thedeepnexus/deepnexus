# /main.py

import asyncio
from graph.rag_graph import get_async_rag_pipeline
from state.schema import RAGState
from utils.async_cache import init_db

async def main():
    await init_db()

    graph = get_async_rag_pipeline()
    input_data = RAGState(
        query="공인중개사법령상 중개사무소의 개설등록에 관한 설명",
        top_k=5
    )

    final_state = await graph.ainvoke(input_data)
    print("\n🧠 최종 응답:", final_state.get("final_response", "[응답 없음]"))

if __name__ == "__main__":
    asyncio.run(main())
