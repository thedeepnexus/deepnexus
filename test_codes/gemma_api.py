from gradio_client import Client

client = Client("dasomaru/docker-api")
result = client.predict(
		n=3,
		api_name="/predict"
)
print(result)