import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
assert api_key is not None, "OPENAI_API_KEY not set in environment."

class OpenAIGPT:
    def __init__(self, model="gpt-4", temperature=0.2, max_tokens=None, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):
        if isinstance(prompt, str):
            messages = [
                {"role": "system", "content": "You are a PDDL expert."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = prompt  # Already formatted messages (e.g., chain-of-thought)

        start_time = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )
        duration = time.time() - start_time

        content = response.choices[0].message.content

        return {
            "response": content,
            "api_time": duration
        }