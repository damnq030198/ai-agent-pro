import os
import sys
import json
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.factory import ModelFactory

app = FastAPI(title="AI Agent Pro - Inference Server")

class QueryRequest(BaseModel):
    query: str
    model_id: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: float = 0.7

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate")
async def generate(request: QueryRequest):
    """Non-streaming generation"""
    llm = ModelFactory.get_model(request.model_id)
    response = llm.generate(request.query, system_prompt=request.system_prompt, temperature=request.temperature)
    return {"response": response}

@app.post("/stream")
async def stream(request: QueryRequest):
    """Streaming generation via SSE"""
    llm = ModelFactory.get_model(request.model_id)
    
    async def event_generator():
        try:
            # stream_generate is a generator
            for chunk in llm.stream_generate(request.query, system_prompt=request.system_prompt, temperature=request.temperature):
                # Format as SSE
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    port = int(os.getenv("INFERENCE_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
