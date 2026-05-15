# 🤖 AI Agent Pro System

Hệ thống AI Agent cá nhân được xây dựng theo tiêu chuẩn **Generative AI "Chuẩn PRO"** kết hợp với bộ kỹ năng **Agent Skills**.

## 🏗️ Kiến Trúc Hệ Thống (Hybrid)

Hệ thống sử dụng mô hình kết hợp:

- **AI Core (Python):** Chịu trách nhiệm về LLM, RAG (Retrieval-Augmented Generation) và xử lý ngôn ngữ tự nhiên.
- **Orchestrator (Node.js):** Chịu trách nhiệm điều phối, quản lý hàng đợi task (BullMQ) và cung cấp API/Interface.

### Cấu Trúc Thư Mục

```text
my-ai-agent-pro/
├── 📁 .claude/                # 🤖 AI Agent Workflow (từ Class-AI-Agent)
│   ├── 📁 agents/             # Định nghĩa vai trò (Spec, Plan, Build...)
│   ├── 📁 skills/             # Copy/Link từ agent-skills/skills
│   └── 📁 rules/              # Luật BẮT BUỘC cho Agent
├── 📁 config/                 # ⚙️ Cấu hình (từ AI.md)
│   ├── model_config.yaml      # Provider, Temperature, Max tokens
│   └── logging_config.yaml
├── 📁 data/                   # 💾 Dữ liệu & Memory
│   ├── cache/                 # Lưu response tránh tốn phí API
│   ├── vectordb/              # Long-term memory (Chroma/FAISS)
│   └── raw/                   # Tài liệu đầu vào để RAG
├── 📁 src/                    # 🧠 Mã nguồn chính (Tinh hoa từ AI.md)
│   ├── 📁 core/               # LLM Clients (GPT, Claude, Factory Pattern)
│   ├── 📁 prompts/            # Quản lý Prompt tập trung (Templates, Chains)
│   ├── 📁 rag/                # Retrieval (Embedder, Retriever, Indexer)
│   ├── 📁 processing/         # Tiền xử lý (Chunking, Tokenizer)
│   ├── 📁 inference/          # Orchestrator (Điều phối Agent + RAG)
│   └── 📁 tools/              # Công cụ bổ trợ (Browser-use, File system)
├── 📁 scripts/                # 🛠️ Tự động hóa
│   ├── build_embeddings.py    # Index dữ liệu vào VectorDB
│   └── cleanup.py             # Xóa cache/file tạm
├── docker-compose.yml         # Container hóa (App + DB + Redis)
└── README.md

```

## 🚀 Tính Năng Nổi Bật

1.  **Multi-LLM Support:** Hỗ trợ Claude 3.5, GPT-4o và các Local LLM thông qua Factory Pattern.
2.  **Long-term Memory:** Sử dụng **ChromaDB** để lưu trữ và truy xuất kiến thức từ tài liệu cá nhân.
3.  **Autonomous Workflow:** Tích hợp 20+ kỹ năng từ `agent-skills` (Spec, Plan, Build, Test...).
4.  **Browser Automation:** Tích hợp `browser-use` để Agent tự động tương tác với web.
5.  **Production Ready:** Hỗ trợ Docker, logging tập trung và cơ chế caching để tiết kiệm chi phí.

## 🛠️ Hướng Dẫn Cài Đặt

### Tiền đề

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### Các bước thực hiện

1.  **Khởi tạo hạ tầng:**
    ```bash
    docker-compose up -d
    ```
2.  **Cài đặt Python Core:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Cài đặt Node.js Orchestrator:**
    ```bash
    npm install
    ```
4.  **Cấu hình biến môi trường:**
    Copy `.env` và điền các API Key (ANTHROPIC_API_KEY, OPENAI_API_KEY).

## 📝 Lộ Trình Phát Triển

- [x] Khởi tạo cấu trúc dự án
- [ ] Xây dựng Core AI & Factory Pattern
- [ ] Thiết lập RAG với ChromaDB
- [ ] Hoàn thiện Orchestrator & API
- [ ] Tích hợp UI (Next.js) & Monitoring

---

_Made with ❤️ for Advanced Agentic Coding._
