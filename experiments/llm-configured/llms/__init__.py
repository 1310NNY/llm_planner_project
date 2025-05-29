from .openai_gpt import OpenAIGPT
from .anthropic_claude import AnthropicClaude

def get_llm_model(name: str):
    if name == "gpt-4":
        return OpenAIGPT(model="gpt-4")
    elif name == "claude":
        return AnthropicClaude()
    else:
        raise ValueError(f"Unknown LLM: {name}")