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
        self.max_tokens = max_tokens or 1024
        self.top_p = top_p
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):
        if isinstance(prompt, str):
            messages = [
                {"role": "system", "content": "You are a PDDL expert."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = prompt  # e.g. cot-style prompt

        start_time = time.time()

        if self.model == "o4-mini":
            # 🔹 Responses API: Format als String
            input_str = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    input_str += f"[System]: {content}\n\n"
                elif role == "user":
                    input_str += f"[User]: {content}\n\n"
                elif role == "assistant":
                    input_str += f"[Assistant]: {content}\n\n"

            response = self.client.responses.create(
                model=self.model,
                input=input_str.strip(),
                reasoning={"effort": "medium"}
            )
            raw_output = response.output
            content = raw_output if isinstance(raw_output, str) else str(raw_output)

        else:
            # 🔹 Normale ChatCompletion API (gpt-4, 3.5, 4o)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens
            )
            content = response.choices[0].message.content

        duration = time.time() - start_time

        return {
            "response": content.strip() if isinstance(content, str) else str(content),
            "api_time": duration
        }