from .openai_gpt import OpenAIGPT

def get_llm_model(name: str, temperature: float = 0.2, top_p: float = 1.0, max_tokens: int = 2048):
    if name == "gpt-4":
        return OpenAIGPT(model="gpt-4", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "gpt-3.5":
        return OpenAIGPT(model="gpt-3.5-turbo", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    else:
        raise ValueError(f"Unknown LLM model: {name}")
