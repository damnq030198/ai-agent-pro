import os
import yaml
from typing import Dict, Any
from src.core.base_llm import BaseLLM

class ModelFactory:
    """
    Factory to initialize the appropriate LLM client based on configuration.
    """
    
    @staticmethod
    def load_config(config_path: str = "config/model_config.yaml") -> Dict[str, Any]:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def get_model(model_id: str = None) -> BaseLLM:
        config_data = ModelFactory.load_config()
        
        # Use default model if none specified
        if not model_id:
            model_id = config_data.get("default_model")
            
        model_config = config_data.get("models", {}).get(model_id)
        if not model_config:
            raise ValueError(f"Model configuration for '{model_id}' not found.")
            
        provider = model_config.get("provider")
        
        if provider == "anthropic":
            from src.core.claude_client import ClaudeClient
            return ClaudeClient(model_config)
        elif provider == "openai":
            from src.core.openai_client import OpenAIClient
            return OpenAIClient(model_config)
        elif provider == "google":
            from src.core.gemini_client import GeminiClient
            return GeminiClient(model_config)
        else:
            raise NotImplementedError(f"Provider '{provider}' is not supported yet.")
