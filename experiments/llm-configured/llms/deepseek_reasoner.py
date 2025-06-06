import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
assert api_key, "DEEPSEEK_API_KEY not set in .env"

class DeepseekReasoner:
    def __init__(self, model="deepseek-reasoner", temperature=0.7, max_tokens=2048, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.api_url = "https://api.deepseek.com/v1"

    def generate(self, prompt):
        if isinstance(prompt, list):
            prompt = "\n".join(m["content"] for m in prompt if m["role"] == "user")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant who writes valid PDDL."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }

        start_time = time.time()
        response = requests.post(self.api_url, headers=headers, json=payload)
        duration = time.time() - start_time

        if response.status_code != 200:
            raise Exception(f"DeepSeek API Error: {response.status_code} - {response.text}")

        result = response.json()

        return {
            "response": result["choices"][0]["message"]["content"],
            "api_time": duration
        }
