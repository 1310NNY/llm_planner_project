import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")
assert api_key, "TOGETHER_API_KEY not set in .env"

class TogetherLLaMA3:
    def __init__(self, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=0.7, max_tokens=1024, top_p=1.0):
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self._warm_up()

    def _warm_up(self):
        print(f"🔄 LLaMA 3 warm-up gestartet für {self.model} ...")
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 1,
        }
        try:
            res = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if res.status_code == 200:
                print("✅ LLaMA 3 erfolgreich aufgewärmt.")
            else:
                print(f"⚠️ Warm-up Antwort: {res.status_code} – {res.text}")
        except Exception as e:
            print(f"❌ Fehler beim Warm-up: {e}")

    def generate(self, prompt):
        if isinstance(prompt, list):
            prompt = "\n".join(m["content"] for m in prompt if m["role"] == "user")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }

        start_time = time.time()
        res = requests.post(self.api_url, headers=self.headers, json=payload)
        duration = time.time() - start_time

        if res.status_code != 200:
            raise Exception(f"Together API Error: {res.status_code} - {res.text}")

        content = res.json()["choices"][0]["message"]["content"]

        return {
            "response": content.strip(),
            "api_time": duration
        }
