# from retriever.vectordb import search_documents
from retriever.vectordb_rerank import search_documents
from retriever.vectordb_rerank_law import search_documents as search_law
from retriever.vectordb_rerank_exam import search_documents as search_exam

from generator.prompt_builder import build_prompt
from generator.prompt_builder_all import build_prompt as build_prompt_all

from generator.llm_inference import generate_answer as generate_answer
from generator.llm_inference_all import generate_answer as generate_answer_all

# 2. 캐시 관리
search_cache = {}

def rag_pipeline(query: str, top_k: int = 5) -> str:
    """
    1. 사용자 질문으로 관련 문서를 검색
    2. 검색된 문서와 함께 프롬프트 구성
    3. 프롬프트로부터 답변 생성
    """
    # 캐시 확인
    if query in search_cache:
        print(f"⚡ 캐시 사용: '{query}'")
        return search_cache[query]
    
    # 1. 검색
    # context_docs = search_documents(query, top_k=top_k)
    # print("context_docs: ", context_docs)
    # print("==============================================\n\n")

    context_exam_docs = search_exam(query, top_k=top_k)
    print("context_exam_docs: ", context_exam_docs)
    print("==============================================\n\n")

    constext_law_docs = search_law(query, top_k=top_k)
    print("context_law_docs: ", constext_law_docs)
    print("==============================================\n\n")

    # 2. 프롬프트 조립
    prompt = build_prompt_all(query, constext_law_docs, context_exam_docs)
    print("prompt: ", prompt)    
    print("==============================================\n\n")

    # 3. 모델 추론
    output = generate_answer(prompt)
    # return output

    if isinstance(context_exam_docs, list):
        context_exam_docs = "\n\n".join(context_exam_docs)

    search_cache[query] = output
    return output

# 예시 쿼리
if __name__ == "__main__":
    query = "중개업자가 사무소를 옮겼을 때 필요한 조치"
    top_k = 5
    result = rag_pipeline(query, top_k)
    print(result)