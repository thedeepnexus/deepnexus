from transformers import pipeline

# 1. 모델 로드 (최초 1번만 로드됨)
generator = pipeline(
    "text-generation",
    model="dasomaru/gemma-3-4bit-it-demo",  # 네가 업로드한 모델 이름
    tokenizer="dasomaru/gemma-3-4bit-it-demo",
    device=0,  # CUDA:0 사용 (GPU). CPU만 있으면 device=-1
    max_new_tokens=1024,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1
)

# 2. 답변 생성 함수
def generate_answer(prompt: str) -> str:
    """
    입력받은 프롬프트로부터 모델이 답변을 생성한다.
    """
    print(f"🔵 Prompt Length: {len(prompt)} characters")  # 추가!
    outputs = generator(
        prompt,
        do_sample=True,
        top_k=50,
        num_return_sequences=1
    )
    return outputs[0]["generated_text"].strip()

# 3. 예시 프롬프트
if __name__ == "__main__":
    example_prompt = "What is the capital of France?"
    answer = generate_answer(example_prompt)
    print(f"Answer: {answer}")
