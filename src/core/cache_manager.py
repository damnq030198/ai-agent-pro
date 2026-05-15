import redis
import json
import hashlib
from typing import Optional, Any, Dict

class CacheManager:
    """
    Server-side caching using Redis.
    Handles storing and retrieving LLM responses to save costs and reduce latency.
    """

    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def _generate_key(self, model_name: str, prompt: str, params: Dict[str, Any]) -> str:
        """
        Creates a unique SHA-256 hash for a specific request.
        """
        input_data = f"{model_name}:{prompt}:{json.dumps(params, sort_keys=True)}"
        return f"ai_cache:{hashlib.sha256(input_data.encode()).hexdigest()}"

    def get_response(self, model_name: str, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """
        Retrieves a cached response if exists.
        """
        key = self._generate_key(model_name, prompt, params)
        try:
            return self.client.get(key)
        except redis.RedisError:
            return None

    def set_response(self, model_name: str, prompt: str, params: Dict[str, Any], response: str, ttl: int = 86400):
        """
        Caches a response with an optional Time To Live (default 24h).
        """
        key = self._generate_key(model_name, prompt, params)
        try:
            self.client.setex(key, ttl, response)
        except redis.RedisError:
            pass

    def clear_cache(self):
        """Clears all AI cache keys."""
        keys = self.client.keys("ai_cache:*")
        if keys:
            self.client.delete(*keys)
