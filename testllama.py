import os
import requests

api_key = "f81a951e134359094e5f9f7ea316fa8155b31c5ce8853e1b31b300b59aa680af"
api_url = "https://api.together.xyz/v1/chat/completions"
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": model_name,
    "messages": [{"role": "user", "content": "Was ist ein Domainmodell in PDDL?"}],
    "max_tokens": 100,
    "temperature": 0.7
}

response = requests.post(api_url, headers=headers, json=payload)
print(response.json())



