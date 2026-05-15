import os
from typing import Optional, Dict, Any
from openai import OpenAI
from src.core.base_llm import BaseLLM
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient(BaseLLM):
    """
    Client for OpenAI (GPT-4, etc.)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        params = self._get_params(**kwargs)
        
        # Check Cache
        cached_response = self.cache.get_response(self.model_name, prompt, params)
        if cached_response:
            return cached_response

        # Call OpenAI
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=params["temperature"],
                max_tokens=params["max_tokens"]
            )
            
            result_text = response.choices[0].message.content

            # Store Cache
            self.cache.set_response(self.model_name, prompt, params, result_text)
            return result_text
        except Exception as e:
            raise RuntimeError(f"Error calling OpenAI API: {str(e)}")

    def generate_json(self, prompt: str, schema: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Using OpenAI's JSON mode"""
        params = self._get_params(**kwargs)
        
        messages = [{"role": "user", "content": f"{prompt}\nReturn JSON."}]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            response_format={ "type": "json_object" },
            temperature=params["temperature"]
        )
        import json
        return json.loads(response.choices[0].message.content)
