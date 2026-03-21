"""
OpenRouter LLM Provider (Multi-model support)
"""
import httpx
from typing import Optional
from .base import BaseLLM, LLMResponse


class OpenRouterProvider(BaseLLM):
    """OpenRouter API provider for fast, open-source models"""
    
    API_BASE = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: str, model: str = "meta-llama/llama-3-8b-instruct"):
        super().__init__(api_key, model)
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://rag-pipeline.local",
                "X-Title": "RAG Pipeline",
            }
        )
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        """Generate response from OpenRouter"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.post(
            f"{self.API_BASE}/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        
        data = response.json()
        tokens_used = data.get("usage", {}).get("total_tokens", 0)
        
        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            model=self.model,
            tokens_used=tokens_used,
            cost=None,  # Pricing varies by model
        )
    
    async def generate_with_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Generate response with streaming"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        async with self.client.stream(
            "POST",
            f"{self.API_BASE}/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            },
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        import json
                        data = json.loads(data_str)
                        if data["choices"][0]["delta"].get("content"):
                            yield data["choices"][0]["delta"]["content"]
                    except:
                        continue
    
    def calculate_cost(self, tokens_used: int, is_input: bool = False) -> float:
        """Calculate cost - varies by model"""
        # OpenRouter pricing varies significantly by model
        # This is a placeholder - actual pricing should be fetched from API
        return 0.0
