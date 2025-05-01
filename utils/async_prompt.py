# utils/async_prompt.py

import asyncio
from generator.async_prompt_builder_all import build_prompt as sync_build_prompt_all

async def async_build_prompt_all(query, law_docs, exam_docs):
    return await asyncio.to_thread(sync_build_prompt_all, query, law_docs, exam_docs)
