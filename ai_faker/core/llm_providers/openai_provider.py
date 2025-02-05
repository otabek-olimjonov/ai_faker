import openai
from typing import Dict, Optional
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", max_retries: int = 3):
        """
        Initialize OpenAI provider
        
        Args:
            api_key (str): OpenAI API key
            model (str): Model name (default: "gpt-4o-mini")
            max_retries (int): Maximum number of retries for rate-limited requests
        """
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """
        Generate completion using OpenAI
        
        Args:
            prompt (str): The prompt text
            **kwargs: Additional arguments
                - system_prompt (str): System prompt/context
                - temperature (float): Temperature for generation
                - max_tokens (int): Maximum tokens to generate
        """
        try:
            # Prepare messages
            messages = []
            system_prompt = kwargs.get('system_prompt', '')
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise ValueError(f"Error generating completion with OpenAI: {str(e)}")
    
    def validate_configuration(self) -> bool:
        """
        Validate the OpenAI configuration
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        try:
            # Try a simple completion to validate
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=1
            )
            return True
        except Exception as e:
            print(f"\n⚠️  OpenAI configuration error: {str(e)}")
            return False