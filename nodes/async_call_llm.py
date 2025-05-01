# nodes/async_call_llm.py

from generator.async_llm_inference import async_generate_answer
from state.schema import RAGState

async def async_call_llm(state: RAGState) -> RAGState:
    prompt = state.prompt
    stream = await async_generate_answer(prompt)
    return state.model_copy(update={
        "final_response": stream,
        "stream": True,
        "status": "success"
    })
