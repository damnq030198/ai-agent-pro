import os
from typing import Optional, Dict, Any
from anthropic import Anthropic
from src.core.base_llm import BaseLLM
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient(BaseLLM):
    """
    Client for Anthropic Claude API.
    Integrated with Redis Caching and factory pattern.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")
        
        self.client = Anthropic(api_key=self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generates a text response using Claude. Checks cache first.
        """
        # Get dynamic parameters
        params = self._get_params(**kwargs)
        
        # 1. Check Cache
        cached_response = self.cache.get_response(self.model_name, prompt, params)
        if cached_response:
            return cached_response

        # 2. Call API if not in cache
        try:
            message_params = {
                "model": self.model_name,
                "max_tokens": params["max_tokens"],
                "temperature": params["temperature"],
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            if system_prompt:
                message_params["system"] = system_prompt

            response = self.client.messages.create(**message_params)
            result_text = response.content[0].text
            
            # Log usage metadata
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
            self._log_usage(usage)

            # 3. Store in Cache
            self.cache.set_response(self.model_name, prompt, params, result_text)
            
            return result_text

        except Exception as e:
            # You can integrate logging here
            raise RuntimeError(f"Error calling Claude API: {str(e)}")

    def generate_json(self, prompt: str, schema: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        Generates a JSON response. 
        Note: For Claude, we inject instructions to ensure JSON output.
        """
        json_prompt = f"{prompt}\n\nPlease respond ONLY with a valid JSON object."
        if schema:
            json_prompt += f" Follow this schema: {schema}"
            
        response_text = self.generate(json_prompt, **kwargs)
        
        import json
        try:
            # Simple parsing - in production we'd use more robust regex or repair tools
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback: find the first { and last }
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(response_text[start:end])
            raise ValueError(f"Could not parse JSON from Claude response: {response_text}")
