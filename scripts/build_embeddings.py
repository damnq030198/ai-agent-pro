import sys
import os
from pathlib import Path

# Thêm root vào path để import các module trong src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.indexer import Indexer
from src.processing.chunking import Chunker

def main():
    print("🧠 Starting Knowledge Indexing Process...")
    
    # 1. Khởi tạo các thành phần
    embedder = Embedder()
    vector_store = VectorStore()
    indexer = Indexer(embedder, vector_store)
    chunker = Chunker(chunk_size=600, chunk_overlap=60) # Cấu hình tối ưu cho RAG

    raw_dir = Path("data/raw")
    if not raw_dir.exists():
        raw_dir.mkdir(parents=True)
        print(f"📁 Created {raw_dir}. Please drop your documents there.")
        return

    # 2. Quét các file trong data/raw
    supported_extensions = ['.txt', '.md', '.py'] # Mở rộng thêm nếu cần
    files_to_process = [f for f in raw_dir.glob("**/*") if f.suffix in supported_extensions]

    if not files_to_process:
        print("⚠️ No documents found in data/raw to index.")
        return

    for file_path in files_to_process:
        print(f"📖 Reading: {file_path.name}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 3. Chia nhỏ văn bản (Chunking)
            chunks = chunker.split_text(content)
            
            # 4. Nạp vào Vector Database
            metadatas = [{"source": file_path.name} for _ in chunks]
            indexer.index_documents(chunks, collection_name="agent_knowledge", metadatas=metadatas)
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")

    print("\n✅ Knowledge Base updated successfully!")

if __name__ == "__main__":
    main()
