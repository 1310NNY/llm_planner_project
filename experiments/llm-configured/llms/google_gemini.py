import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
assert api_key is not None, "GEMINI_API_KEY not set in environment."

genai.configure(api_key=api_key)

class GoogleGemini:
    def __init__(self, model="gemini-1.5-pro-latest", temperature=0.2, max_tokens=2048, top_p=1.0):
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt):
        if isinstance(prompt, list):
            prompt = "\n".join(m["content"] for m in prompt if m["role"] == "user")

        start_time = time.time()
        response = self.model.generate_content(prompt)
        duration = time.time() - start_time

        return {
            "response": response.text,
            "api_time": duration
        }
