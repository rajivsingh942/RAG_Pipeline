"""
Google Gemini LLM Provider
"""
import google.generativeai as genai
from typing import Optional
from .base import BaseLLM, LLMResponse


class GeminiProvider(BaseLLM):
    """Google Gemini API provider"""
    
    # Pricing per 1M tokens
    PRICING = {
        "gemini-1.5-pro": {"input": 3.5, "output": 10.5},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-pro": {"input": 0.5, "output": 1.5},
    }
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.model_client = genai.GenerativeModel(model)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        """Generate response from Gemini"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = self.model_client.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )
        
        # Estimate tokens (Gemini doesn't always return exact counts)
        tokens_used = len(response.text.split()) + len(prompt.split())
        
        return LLMResponse(
            content=response.text,
            model=self.model,
            tokens_used=tokens_used,
            cost=None,  # Gemini pricing is complex, estimated separately
        )
    
    async def generate_with_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Generate response with streaming"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = self.model_client.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
            stream=True,
        )
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    
    def calculate_cost(self, tokens_used: int, is_input: bool = False) -> float:
        """Calculate cost for tokens"""
        if self.model not in self.PRICING:
            return 0.0
        
        pricing = self.PRICING[self.model]
        cost_type = "input" if is_input else "output"
        cost_per_token = pricing[cost_type] / 1_000_000
        
        return tokens_used * cost_per_token
