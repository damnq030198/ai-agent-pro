import os
import google.generativeai as genai
from typing import Optional, Dict, Any
from src.core.base_llm import BaseLLM
from dotenv import load_dotenv

load_dotenv()

class GeminiClient(BaseLLM):
    """
    Client for Google Gemini API.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        params = self._get_params(**kwargs)
        
        # Check Cache
        cached_response = self.cache.get_response(self.model_name, prompt, params)
        if cached_response:
            return cached_response

        # Call Gemini
        try:
            # Gemini handles system prompt differently (in model initialization)
            # For simplicity here we prepend it
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            generation_config = {
                "temperature": params["temperature"],
                "max_output_tokens": params["max_tokens"],
            }

            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            result_text = response.text

            # Store Cache
            self.cache.set_response(self.model_name, prompt, params, result_text)
            return result_text
        except Exception as e:
            raise RuntimeError(f"Error calling Gemini API: {str(e)}")

    def generate_json(self, prompt: str, schema: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Gemini JSON generation"""
        json_prompt = f"{prompt}\nReturn result in valid JSON format."
        response_text = self.generate(json_prompt, **kwargs)
        
        import json
        # Simple extraction
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        return json.loads(response_text[start:end])
