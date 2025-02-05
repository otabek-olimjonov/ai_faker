from typing import Dict, Optional, Type
from .llm_providers.base import BaseLLMProvider
from ..models.column_info import ColumnInfo
from ..prompts.templates import BATCH_DATA_GENERATION_PROMPT

class LLMInterface:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider
        if not self.provider.validate_configuration():
            raise ValueError("Invalid LLM provider configuration")
    
    def get_batch_generation_prompt(self, schema_info: str, count: int) -> str:
        """Create a prompt for batch data generation"""
        return BATCH_DATA_GENERATION_PROMPT.format(
            count=count,
            schema_info=schema_info
        )
    
    def generate_value_suggestion(self, prompt: str) -> str:
        """Generate values using the configured LLM provider"""
        try:
            return self.provider.generate_completion(
                prompt,
                temperature=0.7,
                max_tokens=2000  # Increased for batch generation
            )
        except Exception as e:
            raise ValueError(f"Error generating value: {str(e)}")