import requests

url = "https://dasomaru-docker-api.hf.space/"

response = requests.get(url)

if response.status_code == 200:
    print("🧠 응답:", response.json())
else:
    print("❌ 요청 실패:", response.status_code, response.text)
