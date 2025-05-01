import requests
from services.rag_pipeline import rag_pipeline

query = "중개업자가 사무소를 옮겼을 때 필요한 조치"

# response = requests.post(
#     "http://localhost:8000/api/ask",
#     json={"query": query, "top_k": 5}
# )

query = "중개업자가 사무소를 옮겼을 때 필요한 조치"

response = rag_pipeline(query, top_k=5)

print(response)