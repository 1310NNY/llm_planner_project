import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")
assert api_key, "❌ TOGETHER_API_KEY nicht gesetzt."

class TogetherMixtral:
    def __init__(self, model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7, top_p=1.0, max_tokens=1024):
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self._warm_up()

    def _warm_up(self):
        print(f"🔄 Mixtral warm-up gestartet für {self.model} ...")
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 1,
        }
        try:
            res = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if res.status_code == 200:
                print("✅ Mixtral erfolgreich aufgewärmt.")
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
            raise Exception(f"Mixtral API Error: {res.status_code} - {res.text}")

        content = res.json()["choices"][0]["message"]["content"]

        return {
            "response": content.strip(),
            "api_time": duration
        }
