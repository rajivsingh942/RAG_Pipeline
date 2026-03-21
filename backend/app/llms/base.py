"""
Base LLM interface for multi-LLM support
"""
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None


class BaseLLM(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    async def generate_with_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Generate response with streaming"""
        pass
    
    @abstractmethod
    def calculate_cost(self, tokens_used: int, is_input: bool = False) -> float:
        """Calculate API cost"""
        pass
