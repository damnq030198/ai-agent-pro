import os
import google.generativeai as genai
from typing import Optional, Dict, Any, List
from src.core.base_llm import BaseLLM
from src.tools.system_tools import TOOLS_DEFINITION, TOOLS_REGISTRY
from dotenv import load_dotenv

load_dotenv()

class GeminiClient(BaseLLM):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=TOOLS_DEFINITION
        )
        self.chat = self.model.start_chat(history=[])

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        # Simplified for now: just call stream and join
        full_text = ""
        for chunk in self.stream_generate(prompt, system_prompt, **kwargs):
            full_text += chunk
        return full_text

    def stream_generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs):
        params = self._get_params(**kwargs)
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        generation_config = {
            "temperature": params["temperature"],
            "max_output_tokens": params["max_tokens"],
        }

        try:
            response = self.chat.send_message(
                full_prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                # Handle Tool Calls
                if chunk.candidates[0].content.parts:
                    for part in chunk.candidates[0].content.parts:
                        if part.function_call:
                            fn_name = part.function_call.name
                            fn_args = dict(part.function_call.args)
                            
                            # Thông báo cho Frontend về tool call (Vibe layer)
                            yield f"__TOOL_CALL__:{json.dumps({'name': fn_name, 'args': fn_args})}"
                            
                            # Thực thi tool
                            if fn_name in TOOLS_REGISTRY:
                                result = TOOLS_REGISTRY[fn_name](**fn_args)
                                # Gửi kết quả về chat để LLM tiếp tục
                                # Lưu ý: Đây là stream, nên việc gửi kết quả về có thể cần một vòng lặp mới
                                # Trong thực tế, Gemini tự handle chat history nếu dùng self.chat
                                # Chúng ta sẽ yield kết quả để frontend biết
                                yield f"__TOOL_RESULT__:{json.dumps({'name': fn_name, 'result': result})}"
                        
                        if part.text:
                            yield part.text
        except Exception as e:
            raise RuntimeError(f"Error streaming from Gemini API: {str(e)}")

    def generate_json(self, prompt: str, schema: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        # ... (giữ nguyên hoặc cập nhật sau)
        return super().generate_json(prompt, schema, **kwargs)

import json
