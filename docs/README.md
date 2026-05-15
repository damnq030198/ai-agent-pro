# 🤖 AI Agent Pro - Documentation

Dự án này là một hệ thống AI Agent đa năng, kết hợp sức mạnh của nhiều LLM (Claude, GPT, Gemini) với bộ nhớ dài hạn (RAG) và khả năng lập kế hoạch tự động.

## 🏗️ Kiến trúc hệ thống

Dự án tuân thủ nguyên tắc tách biệt hoàn toàn các thành phần:
- **Core:** Giao tiếp với các Provider LLM thông qua Factory Pattern.
- **RAG:** Quản lý tri thức bằng ChromaDB và Embeddings.
- **Prompts:** Quản lý tập trung các mẫu câu lệnh.
- **Processing:** Làm sạch và chia nhỏ dữ liệu đầu vào.
- **Inference:** Điều phối (Orchestration) toàn bộ luồng xử lý.

## 📁 Cấu trúc thư mục chính
- `src/core/`: Kết nối AI (Claude, OpenAI, Gemini).
- `src/rag/`: Hệ thống trí nhớ (ChromaDB).
- `src/prompts/`: Template và Chain of Thought.
- `src/inference/`: Bộ điều phối trung tâm.
- `data/`: Lưu trữ cache, vector database và tài liệu thô.

## 🚀 Quy trình hoạt động của Agent
1. **Tiếp nhận:** User gửi yêu cầu.
2. **Tìm kiếm:** Retriever tìm các đoạn văn bản liên quan trong `data/vectordb`.
3. **Phân tích:** Inference Engine kết hợp yêu cầu và tri thức tìm được vào Prompt.
4. **Xử lý:** LLM xử lý và trả về kết quả thô.
5. **Định dạng:** ResponseParser chuyển kết quả thành Markdown hoặc JSON chuẩn.
