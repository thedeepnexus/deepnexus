# state/schema.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class RAGState(BaseModel):
    query: str = Field(..., description="사용자 입력 쿼리")
    top_k: int = Field(default=5, description="검색할 문서 수")

    cached_response: Optional[str] = Field(default=None, description="캐시된 응답")
    retrieved_docs: List[Dict[str, Any]] = Field(default_factory=list, description="검색된 원문 문서")
    reranked_docs: List[Dict[str, Any]] = Field(default_factory=list, description="재정렬된 문서")
    
    prompt: str = Field(default="", description="LLM에 전달할 프롬프트")
    final_response: str = Field(default="", description="최종 생성된 응답")
