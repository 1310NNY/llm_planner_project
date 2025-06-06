from .openai_gpt import OpenAIGPT
from .google_gemini import GoogleGemini
from .anthropic_claude import AnthropicClaude  
from .deepseek_reasoner import DeepseekReasoner
from .together_llama3_chat import TogetherLLaMA3
from .together_mixtral_chat import TogetherMixtral

def get_llm_model(name: str, temperature: float = 0.2, top_p: float = 1.0, max_tokens: int = 2048):
    if name == "gpt-4o":
        return OpenAIGPT(model="gpt-4o", max_tokens=max_tokens)
    elif name == "o4-mini":
        return OpenAIGPT(model="o4-mini", max_tokens=max_tokens)
    elif name == "gemini":
        return GoogleGemini(model="gemini-2.5-pro-exp-03-25", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "claude":
        return AnthropicClaude(model="claude-3-7-sonnet-20250219", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "deepseek":
        return DeepseekReasoner(model="deepseek-chat", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "llama3":
        return TogetherLLaMA3(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    elif name == "mixtral":
        return TogetherMixtral(model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=temperature, top_p=top_p, max_tokens=max_tokens)
    else:
        raise ValueError(f"Unknown LLM model: {name}")
