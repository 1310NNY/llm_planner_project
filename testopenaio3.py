import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="o3-mini",
    messages=[{"role": "user", "content": "Sag mir etwas über KI-Planung."}],
    max_completion_tokens=100
)

print(response.choices[0].message.content)

