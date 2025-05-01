from generator.llm_inference import generate_answer
from type.state_schema import RAGState

def call_llm(state: RAGState) -> RAGState:
    prompt = state.prompt
    response = generate_answer(prompt)
    return state.model_copy(update={
        "final_response": response,
        "status": "success"
    })
