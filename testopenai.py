from openai import OpenAI
from config import OPENAI_API_KEY

# Client initialisieren (neu!)
client = OpenAI(api_key=OPENAI_API_KEY)

# Anfrage an GPT-4 senden
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Gib mir ein motivierendes Zitat für meine Bachelorarbeit."}
    ],
)

print(response.choices[0].message.content)
