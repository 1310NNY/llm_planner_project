import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HF_API_KEY")
assert api_key, "HF_API_KEY not set in .env"

class MistralChat:
    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.1", temperature=0.7, max_tokens=1024, top_p=1.0):
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self._warmed_up = False
        self._warm_up_model()

    def _warm_up_model(self):
        """Dummy-Anfrage an Hugging Face API, um das Modell zu starten (Verzögerung vermeiden)."""
        if self._warmed_up:
            return

        payload = {
            "inputs": "Hello",
            "parameters": {
                "max_new_tokens": 1
            }
        }

        try:
            print(f"🔄 Mistral warm-up gestartet für {self.model} ...")
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                print("✅ Mistral Modell erfolgreich aufgewärmt.")
                self._warmed_up = True
            else:
                print(f"⚠️ Warm-up Antwort: {response.status_code} – {response.text}")
        except Exception as e:
            print(f"❌ Warm-up Fehler: {e}")

    def generate(self, prompt):
        if isinstance(prompt, list):
            prompt = "\n".join(m["content"] for m in prompt if m["role"] == "user")

        payload = {
            "inputs": f"<s>[INST] {prompt} [/INST]",
            "parameters": {
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens,
                "top_p": self.top_p
            }
        }

        start_time = time.time()
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        duration = time.time() - start_time

        if response.status_code != 200:
            raise Exception(f"Mistral API Error: {response.status_code} - {response.text}")

        content = response.json()[0]["generated_text"].split("[/INST]")[-1].strip()

        return {
            "response": content,
            "api_time": duration
        }