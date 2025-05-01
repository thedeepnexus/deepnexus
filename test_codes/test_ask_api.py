import requests

query = "중개업자가 사무소를 옮겼을 때 필요한 조치"

response = requests.post(
    "http://localhost:8000/api/ask",
    json={"query": query, "top_k": 5}
)

if response.status_code == 200:
    output = response.json()["output"]
    print("✅ 결과:")
    print(output)
else:
    print("❌ 실패:", response.text)
