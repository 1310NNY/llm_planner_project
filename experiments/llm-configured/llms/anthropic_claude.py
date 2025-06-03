import os
import time
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
assert api_key, "ANTHROPIC_API_KEY not set in .env"

class AnthropicClaude:
    def __init__(self, model="claude-3-opus-20240229", temperature=0.2, max_tokens=2048, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt):
        if isinstance(prompt, list):
            prompt = "\n".join(m["content"] for m in prompt if m["role"] == "user")

        start_time = time.time()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system="You are a helpful assistant who writes valid PDDL.",
            messages=[{"role": "user", "content": prompt}]
        )
        duration = time.time() - start_time

        return {
            "response": response.content[0].text,
            "api_time": duration
        }
