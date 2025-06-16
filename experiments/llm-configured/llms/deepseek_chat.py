import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
assert api_key, "DEEPSEEK_API_KEY nicht gesetzt"

class DeepSeekChat:
    def __init__(self, model="deepseek-chat", temperature=0.2, max_tokens=2048, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def generate(self, prompt):
        start = time.time()
        messages = [{"role": "user", "content": prompt}] \
            if isinstance(prompt, str) else prompt
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
        except Exception as e:
            print("❌ API-Fehler beim Aufruf:", e)
            return {"response": None, "api_time": time.time() - start}

        duration = time.time() - start
        choice = response.choices[0].message
        content = choice.content.strip() if choice.content else ""

        return {"response": content, "api_time": duration}


def test_deepseek_chat():
    try:
        chat = DeepSeekChat(
            model="deepseek-chat",
            temperature=0.2,
            max_tokens=256,
            top_p=1.0
        )
        print("✅ DeepSeekChat initialisiert")
    except AssertionError as e:
        print("❌ Key-Fehler:", e); return
    except Exception as e:
        print("❌ Init-Fehler:", e); return

    prompt = "Nenne die ersten drei Planeten im Sonnensystem."
    result = chat.generate(prompt)

    print(f"\n⏱️ Dauer: {result['api_time']:.2f}s")
    if result['response']:
        print("🧠 Antwort:", result['response'])
    else:
        print("⚠️ Keine Antwort erhalten")

if __name__ == "__main__":
    test_deepseek_chat()
