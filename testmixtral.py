import os
import requests

api_key = "f81a951e134359094e5f9f7ea316fa8155b31c5ce8853e1b31b300b59aa680af"


url = "https://api.together.xyz/v1/chat/completions"
model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Was ist ein Domainmodell in PDDL?"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")
try:
    print("Antwort:", response.json()["choices"][0]["message"]["content"])
except Exception:
    print("Fehler oder leere Antwort:", response.text)

