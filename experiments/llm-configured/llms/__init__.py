from .openai_gpt import OpenAIGPT
from .google_gemini import GoogleGemini
# from .anthropic_claude import AnthropicClaude  
from .deepseek_chat import DeepseekChat
from .mistral_chat import MistralChat  # <--- NEU
from .llama3_chat import LLaMA3Chat    # <--- NEU

def get_llm_model(name: str, temperature: float = 0.2, top_p: float = 1.0, max_tokens: int = 2048):
    if name == "gpt-4":
        return OpenAIGPT(model="gpt-4", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "gpt-3.5":
        return OpenAIGPT(model="gpt-3.5-turbo", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "gemini":
        return GoogleGemini(model="gemini-1.5-pro", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    # elif name == "claude":
    #     return AnthropicClaude(model="claude-3-opus-20240229", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "deepseek":
        return DeepseekChat(model="deepseek-chat", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "mistral":
        return MistralChat(model="mistralai/Mistral-7B-Instruct-v0.1", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "llama3":
        return LLaMA3Chat(model="meta-llama/Llama-2-7b-chat-hf", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    else:
        raise ValueError(f"Unknown LLM model: {name}")
