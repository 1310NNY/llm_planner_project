import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
assert api_key is not None, "DEEPSEEK_API_KEY not set in environment."

class DeepSeekReasoner:
    def __init__(self, model="deepseek-reasoner", temperature=0.2, max_tokens=2048, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def generate(self, prompt):
        start_time = time.time()

        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        elif isinstance(prompt, list):
            messages = prompt
        else:
            raise ValueError("Prompt must be a string or a list of messages.")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens
        )

        duration = time.time() - start_time
        return {
            "response": response.choices[0].message.content.strip(),
            "api_time": duration
        }
