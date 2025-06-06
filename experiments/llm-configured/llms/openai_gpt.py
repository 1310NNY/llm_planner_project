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
        start_time = time.time()

        # Prompt-Formatierung
        if isinstance(prompt, str):
            messages = [
                {"role": "system", "content": "You are a PDDL expert."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = prompt  # Already formatted (e.g., CoT)

        # 🔄 Responses API für o4-mini
        if self.model == "o4-mini":
            input_str = ""
            for msg in messages:
                if msg["role"] == "system":
                    input_str += f"[System]: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    input_str += f"[User]: {msg['content']}\n\n"
                elif msg["role"] == "assistant":
                    input_str += f"[Assistant]: {msg['content']}\n\n"

            response = self.client.responses.create(
                model=self.model,
                input=input_str.strip(),
                reasoning={"effort": "medium"}
            )
            content = response.output

        # 🔄 ChatCompletion für GPT-4, GPT-3.5, GPT-4o
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens
            )
            content = response.choices[0].message.content

        # 🔧 Formatierung fixen (\n → echte Zeilenumbrüche)
        if isinstance(content, str):
            content = content.replace("\\n", "\n").strip()
        else:
            content = str(content)

        duration = time.time() - start_time
        return {
            "response": content,
            "api_time": duration
        }