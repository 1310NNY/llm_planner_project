import os
import time
import anthropic
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
assert api_key is not None, "ANTHROPIC_API_KEY not set in environment."

class AnthropicClaude:
    def __init__(self, model="claude-3-opus-20240229", temperature=0.2, max_tokens=1024, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens or 1024  # fallback falls None
        self.top_p = top_p
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt):
        if isinstance(prompt, str):
            messages = [
                {"role": "user", "content": prompt}
            ]
        else:
            messages = prompt  # Already formatted messages (list of dicts)

        start_time = time.time()
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )
        duration = time.time() - start_time

        content = response.content[0].text if hasattr(response, "content") else response

        return {
            "response": content.strip(),
            "api_time": duration
        }
