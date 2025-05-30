from .openai_gpt import OpenAIGPT

def get_llm_model(name: str):
    if name == "gpt-4":
        return OpenAIGPT(model="gpt-4")
    elif name == "gpt-3.5":
        return OpenAIGPT(model="gpt-3.5-turbo")
    else:
        raise ValueError(f"Unknown LLM model: {name}")