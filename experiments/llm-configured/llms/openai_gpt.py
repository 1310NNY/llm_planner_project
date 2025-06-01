import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
assert api_key is not None, "OPENAI_API_KEY not set in environment."

class OpenAIGPT:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):
        if isinstance(prompt, str):
            messages = [
                {"role": "system", "content": "You are a PDDL expert."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = prompt  # Already formatted CoT-style messages

        start_time = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )
        duration = time.time() - start_time

        content = response.choices[0].message.content
        usage = response.usage

        return {
            "response": content,
            "api_time": duration,
            "tokens_total": usage.total_tokens if usage else None,
            "prompt_length_chars": len(messages[0]["content"]) if isinstance(prompt, str) else None,
            "completion_length_chars": len(content)
        }