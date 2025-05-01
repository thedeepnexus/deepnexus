from generator.prompt_builder_all import build_prompt as build_prompt_all

def build_prompt_all(query, law_docs, exam_docs):
    # law_docs / exam_docs: list of reranked document strings
    law_str = "\n\n".join(law_docs)
    exam_str = "\n\n".join(exam_docs)

    system_msg = "당신은 공인중개사 시험 문제 출제 전문가입니다."
    guidance = "아래는 관련 법령과 기출문제입니다:\n"

    prompt = f"""{system_msg}\n\n{guidance}
[법령 정보]
{law_str}

[기출문제 정보]
{exam_str}

[질문]
{query}

[지시사항]
- 정확하고 명확하게 답변하세요."""

    return prompt
