# types/state_schema.py
from typing import TypedDict
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# class RAGState(TypedDict, total=False):
#     query: str
#     top_k: int
#     cached_response: str
#     retrieved_docs: dict
#     reranked_docs: dict
#     prompt: str
#     final_response: str


class RAGState(BaseModel):
    query: str
    top_k: int = 5
    cached_response: Optional[str] = None
    retrieved_docs: List[Dict[str, Any]] = []
    reranked_docs: List[Dict[str, Any]] = []
    prompt: str = ""
    final_response: str = ""
