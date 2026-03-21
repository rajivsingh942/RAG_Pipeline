"""LLM Providers"""
from .base import BaseLLM, LLMResponse
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .openrouter_provider import OpenRouterProvider


def get_llm(provider: str, api_key: str, model: str) -> BaseLLM:
    """Factory function to get LLM provider"""
    providers = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "openrouter": OpenRouterProvider,
    }
    
    if provider not in providers:
        raise ValueError(f"Unknown LLM provider: {provider}")
    
    return providers[provider](api_key, model)


__all__ = [
    "BaseLLM",
    "LLMResponse",
    "OpenAIProvider",
    "GeminiProvider",
    "OpenRouterProvider",
    "get_llm",
]
