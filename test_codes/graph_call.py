

from graph.rag_graph import get_rag_pipeline_graph
from type.state_schema import RAGState


# if __name__ == "__main__":
graph = get_rag_pipeline_graph()

input_data = RAGState(
    query="공인중개사법령상 중개사무소의 개설등록에 관한 설명",
    top_k=5
)

final_state = graph.invoke(input_data)
# print("\n🧠 최종 응답:", final_state.final_response)
# print("\n🧠 최종 응답:", final_state["final_response"])
print("\n🧠 최종 응답:", final_state.get("final_response", "[응답 없음]")) 