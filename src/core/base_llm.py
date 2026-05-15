import abc
from typing import Any, Dict, List, Optional

class BaseLLM(abc.ABC):
    """
    Abstract Base Class for all LLM implementations.
    Ensures a consistent interface across different AI providers.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model_name")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1024)
        
        # Initialize Cache Manager
        from src.core.cache_manager import CacheManager
        self.cache = CacheManager(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379))
        )

    def _get_params(self, **kwargs) -> Dict[str, Any]:
        """Helper to collect model parameters for cache key generation."""
        params = {
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        return params

    @abc.abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        pass

    def _log_usage(self, usage_data: Dict[str, int]):
        """
        Logs token usage to a central file and potentially Prometheus.
        usage_data: {"input_tokens": 100, "output_tokens": 50}
        """
        import json
        import datetime
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "model": self.model_name,
            "usage": usage_data
        }
        
        log_path = "data/logs/token_usage.jsonl"
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    @abc.abstractmethod
    def generate_json(self, prompt: str, schema: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate a structured JSON response.
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """Returns basic info about the model instance."""
        return {
            "model_name": self.model_name,
            "provider": self.__class__.__name__,
            "temperature": self.temperature
        }
