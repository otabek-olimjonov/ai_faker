from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion from the LLM provider"""
        pass
    
    @abstractmethod
    def validate_configuration(self) -> bool:
        """Validate the provider configuration"""
        pass