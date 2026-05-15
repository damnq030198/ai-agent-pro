import sys
import os
import json
import argparse

# Thêm root vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference.inference_engine import InferenceEngine
from src.rag.retriever import Retriever
from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--model", type=str, default=None)
    args = parser.parse_args()

    try:
        # 1. Khởi tạo Engine
        embedder = Embedder()
        vector_store = VectorStore()
        retriever = Retriever(embedder, vector_store)
        engine = InferenceEngine(retriever, model_id=args.model)

        # 2. Thực thi query
        result = engine.query_with_rag(args.query)

        # 3. Trả về JSON để Node.js parse
        output = {
            "query": args.query,
            "response": result,
            "model": engine.llm.model_name
        }
        print(json.dumps(output))

    except Exception as e:
        error_output = {"error": str(e)}
        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == "__main__":
    main()
