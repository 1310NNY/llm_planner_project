import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def reorder_with_llm(domain_text, heuristic="EFF1"):
    prompt = f"""
You are a PDDL expert. Reorder the actions (operators) based on the heuristic {heuristic}.
Return only the updated domain.
---
{domain_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful AI."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response["choices"][0]["message"]["content"]
