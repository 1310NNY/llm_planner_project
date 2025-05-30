import os
from openai import OpenAI
from dotenv import load_dotenv

# ✅ .env laden – auch wenn extern noch nicht erfolgt
load_dotenv()

class OpenAIGPT:
    def __init__(self, model="gpt-4"):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY nicht gesetzt. Bitte setze ihn in deiner .env oder Umgebung.")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a PDDL expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
