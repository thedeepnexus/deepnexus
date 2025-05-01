def build_prompt(query: str, law_docs: list, exam_docs: list) -> str:
    prompt = (
        "당신은 공인중개사 시험 문제 출제 전문가입니다.\n\n"
        "아래는 관련 법령과 기출문제입니다:\n\n"
        "[법령 정보]\n"
    )

    for doc in law_docs:
        prompt += f"- {doc}\n"

    prompt += "\n[기출문제 정보]\n"

    for doc in exam_docs:
        prompt += f"- {doc}\n"

    prompt += f"\n위 정보를 참고하여 사용자의 요청에 정확하고 명확하게 답변하세요.\n\n"
    prompt += f"[질문]\n{query}\n\n[답변]\n"

    return prompt
