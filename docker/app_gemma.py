import gradio as gr
import spaces
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
# from retriever.vectordb_rerank import search_documents  # 🧠 RAG 검색기 불러오기
from services.rag_pipeline import rag_pipeline

model_name = "dasomaru/gemma-3-4bit-it-demo"


# 1. 모델/토크나이저 1회 로딩
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
# 🚀 model은 CPU로만 먼저 올림 (GPU 아직 없음)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # 4bit model이니까
    device_map="auto",  # ✅ 중요: 자동으로 GPU 할당
    trust_remote_code=True,
)

# 2. 캐시 관리
search_cache = {}

@spaces.GPU(duration=300)
def generate_response(query: str):
    tokenizer = AutoTokenizer.from_pretrained(
        "dasomaru/gemma-3-4bit-it-demo",
        trust_remote_code=True,
        )
    model = AutoModelForCausalLM.from_pretrained(
        "dasomaru/gemma-3-4bit-it-demo",
        torch_dtype=torch.float16,  # 4bit model이니까
        device_map="auto",  # ✅ 중요: 자동으로 GPU 할당
        trust_remote_code=True,

        )
    model.to("cuda")    

    if query in search_cache:
        print(f"⚡ 캐시 사용: '{query}'")
        return search_cache[query]

    # 🔥 rag_pipeline을 호출해서 검색 + 생성
    # 검색
    top_k = 5
    results = rag_pipeline(query, top_k=top_k)

    # 결과가 list일 경우 합치기
    if isinstance(results, list):
        results = "\n\n".join(results)

    search_cache[query] = results
    # return results

    inputs = tokenizer(results, return_tensors="pt").to(model.device)  # ✅ model.device
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        do_sample=True,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

    
# 3. Gradio 인터페이스
demo = gr.Interface(
    fn=generate_response,
    # inputs=gr.Textbox(lines=2, placeholder="질문을 입력하세요"),
    inputs="text",
    outputs="text",
    title="Law RAG Assistant",
    description="법령 기반 RAG 파이프라인 테스트",
)

# demo.launch(server_name="0.0.0.0", server_port=7860)  # 🚀 API 배포 준비 가능
# demo.launch()
demo.launch(debug=True)
