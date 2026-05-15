import json
import re
from typing import Any, Dict, Optional

class ResponseParser:
    """
    Cleans and formats LLM outputs into structured data or clean markdown.
    """

    @staticmethod
    def to_json(text: str) -> Dict[str, Any]:
        """
        Extracts and parses JSON from potentially messy LLM response.
        """
        try:
            # 1. Try direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            # 2. Try to find the JSON block using regex
            match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Failed to parse JSON from: {text[:100]}...")

    @staticmethod
    def clean_markdown(text: str) -> str:
        """Removes common AI prefixes like 'Here is the answer:'."""
        # Simple cleanup logic
        prefixes = ["Here is the answer:", "Based on the context:", "According to the documents:"]
        cleaned = text
        for p in prefixes:
            if cleaned.startswith(p):
                cleaned = cleaned[len(p):].strip()
        return cleaned
