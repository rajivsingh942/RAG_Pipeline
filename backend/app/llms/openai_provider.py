"""
OpenAI LLM Provider
"""
import asyncio
from typing import Optional
from openai import AsyncOpenAI
from .base import BaseLLM, LLMResponse


class OpenAIProvider(BaseLLM):
    """OpenAI API provider"""
    
    # Pricing per 1M tokens
    PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    }
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(api_key, model)
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        """Generate response from OpenAI"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        tokens_used = response.usage.total_tokens
        cost = self.calculate_cost(
            response.usage.prompt_tokens, is_input=True
        ) + self.calculate_cost(
            response.usage.completion_tokens, is_input=False
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model,
            tokens_used=tokens_used,
            cost=cost,
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
        
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def calculate_cost(self, tokens_used: int, is_input: bool = False) -> float:
        """Calculate cost for tokens"""
        if self.model not in self.PRICING:
            return 0.0
        
        pricing = self.PRICING[self.model]
        cost_type = "input" if is_input else "output"
        # Cost per token (pricing is per 1M tokens)
        cost_per_token = pricing[cost_type] / 1_000_000
        
        return tokens_used * cost_per_token
