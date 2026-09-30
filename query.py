import requests


url = "http://localhost:30000/v1/chat/completions";

load = {"model": "/models/Qwen3.5-2B", "messages": [{"role": "user", "content": "Explain how to deploy a model on my laptop GPU using SGLang server on docker, and query a prompt on the server using a python script."}], "temperature": 0.6, "max_tokens": 20000}

response = requests.post(url, json=load)

response.raise_for_status()

data = response.json()

print(data["choices"][0]["message"]["content"])
