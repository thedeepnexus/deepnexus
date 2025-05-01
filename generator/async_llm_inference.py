# generator/async_llm_inference.py

from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="dasomaru/gemma-3-4bit-it-demo",
    tokenizer="dasomaru/gemma-3-4bit-it-demo",
    device=0,
    max_new_tokens=1024,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1
)

async def async_generate_answer(prompt: str) -> str:
    print(f"🔵 Prompt Length: {len(prompt)} characters")
    outputs = await generator(
        prompt,
        do_sample=True,
        top_k=50,
        num_return_sequences=1
    )
    return outputs[0]["generated_text"].strip()
