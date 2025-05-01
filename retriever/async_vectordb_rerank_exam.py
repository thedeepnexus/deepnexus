# retriever/async_vectordb_rerank_exam.py

import asyncio
from retriever.vectordb_rerank_exam import search_documents as sync_search_documents

async def search_documents(query: str, top_k: int = 5):
    return await asyncio.to_thread(sync_search_documents, query, top_k)
