def build_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문과 검색된 문서들을 조합해 LLM 입력용 프롬프트를 만든다.
    """
    context_text = "\n".join([f"- {doc}" for doc in context_docs])

    prompt = f"""당신은 공인중개사 시험 문제 출제 전문가입니다.

다음은 기출 문제 및 관련 법령 정보입니다:
{context_text}

이 정보를 참고하여 사용자의 요청에 답변해 주세요.

[질문]
{query}

[답변]
"""
    return prompt
