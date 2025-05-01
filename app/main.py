# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from graph.async_rag_graph import get_async_rag_pipeline
from state.schema import RAGState
from utils.async_cache import init_db
from contextlib import asynccontextmanager

graph = get_async_rag_pipeline()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/rag")
async def rag(query: str, request: Request):
    input_data = RAGState(query=query)

    async def event_stream():
        async for update in graph.astream(input_data, stream_mode="updates"):
            for node, result in update.items():
                if result.get("final_response"):
                    yield f"data: [{node}] {result['final_response']}\n\n"
                if await request.is_disconnected():
                    return

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ✅ 여기에 실행 구문 추가
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)