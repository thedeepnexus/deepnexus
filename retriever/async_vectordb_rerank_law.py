# retriever/vectordb_rerank_law_async.py

import asyncio
from retriever.vectordb_rerank_law import search_documents as sync_search_documents

async def search_documents(query: str, top_k: int = 5):
    # 기존 동기 함수 비동기 thread로 실행
    return await asyncio.to_thread(sync_search_documents, query, top_k)
