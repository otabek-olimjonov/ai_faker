import google.generativeai as genai
from typing import Dict, Optional
import os
import time
from .base import BaseLLMProvider

# Suppress Gemini warnings
os.environ['ABSL_LOGGING_MIN_LEVEL'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-pro", max_retries: int = 3, retry_delay: float = 2.0):
        """
        Initialize Gemini provider
        
        Args:
            api_key (str): Google API key
            model (str): Model name (default: "gemini-pro")
            max_retries (int): Maximum number of retries for rate-limited requests
            retry_delay (float): Initial delay between retries in seconds
        """
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        try:
            self.gemini_model = genai.GenerativeModel(self.model)
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini model: {str(e)}")
    
    def _handle_rate_limit(self, attempt: int) -> None:
        """Handle rate limit with exponential backoff"""
        if attempt < self.max_retries:
            wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
            print(f"\n⏳ Rate limit reached. Waiting {wait_time:.1f}s before retry {attempt + 1}/{self.max_retries}...")
            time.sleep(wait_time)
        else:
            raise ValueError("Maximum retry attempts reached. Please check your API quota or try again later.")

    def generate_completion(self, prompt: str, **kwargs) -> str:
        """
        Generate completion using Gemini with retry logic
        
        Args:
            prompt (str): The prompt text
            **kwargs: Additional arguments
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Combine system prompt and user prompt if provided
                system_prompt = kwargs.get('system_prompt', '')
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                # Configure generation parameters
                generation_config = genai.types.GenerationConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 150),
                    top_p=kwargs.get('top_p', 0.95),
                    top_k=kwargs.get('top_k', 40)
                )
                
                # Generate response
                response = self.gemini_model.generate_content(
                    full_prompt,
                    generation_config=generation_config,
                    stream=False
                )
                
                # Check if the response was blocked
                if response.prompt_feedback.block_reason:
                    raise ValueError(f"Response was blocked: {response.prompt_feedback.block_reason}")
                
                return response.text.strip()
                
            except Exception as e:
                last_error = e
                error_message = str(e).lower()
                
                # Check for rate limit errors
                if "quota" in error_message or "rate limit" in error_message or "429" in error_message:
                    self._handle_rate_limit(attempt)
                    continue
                
                # For other errors, raise immediately
                raise ValueError(f"Error generating completion with Gemini: {str(e)}")
        
        # If we've exhausted all retries
        raise ValueError(f"Failed after {self.max_retries} attempts. Last error: {str(last_error)}")
    
    def validate_configuration(self) -> bool:
        """Validate the Gemini configuration"""
        try:
            test_response = self.gemini_model.generate_content(
                "Test",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1
                )
            )
            return not bool(test_response.prompt_feedback.block_reason)
        except Exception as e:
            error_message = str(e).lower()
            if "quota" in error_message or "rate limit" in error_message or "429" in error_message:
                print("\n⚠️  API quota exceeded during validation. You may need to wait or check your quota limits.")
            return False