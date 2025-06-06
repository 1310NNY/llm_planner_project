import os
import time
import anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
assert api_key is not None, "ANTHROPIC_API_KEY not set in environment."


class AnthropicClaude:
    def __init__(self, model="claude-3-7-sonnet-20250219", temperature=0.2, max_tokens=None, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens or 1024
        self.top_p = top_p
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt):
        start_time = time.time()

        # 📌 Fall 1: Zero-shot (Prompt als einfacher String)
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
            system_prompt = ""

        # 📌 Fall 2: Chain-of-Thought (Prompt ist Liste mit Rollen)
        elif isinstance(prompt, list):
            system_prompt = None
            messages_fixed = []

            for msg in prompt:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                elif msg["role"] in ("user", "assistant"):
                    messages_fixed.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                # andere Rollen ignorieren

            messages = messages_fixed
        else:
            raise ValueError("Prompt must be either a string or a list of messages.")

        # 🧠 API-Aufruf
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            system=system_prompt,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens
        )

        duration = time.time() - start_time

        return {
            "response": response.content[0].text.strip(),
            "api_time": duration
        }