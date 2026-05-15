# 🛠️ Hướng Dẫn Cài Đặt (Setup Guide)

Làm theo các bước sau để thiết lập dự án AI Agent Pro trên máy của bạn.

## 1. Yêu cầu hệ thống
- **Python 3.10+**
- **Node.js 18+**
- **Docker & Docker Compose** (Để chạy Redis, ChromaDB, Postgres)

## 2. Cài đặt hạ tầng (Infrastructure)
Khởi chạy các dịch vụ lưu trữ dữ liệu và bộ nhớ:
```bash
cd my-ai-agent-pro
docker-compose up -d
```

## 3. Cài đặt Python Core
```bash
pip install -r requirements.txt
```

## 4. Cấu hình biến môi trường
Tạo file `.env` tại root dự án (nếu chưa có) và điền các API Keys:
```env
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 5. Tự động hóa với Scripts (`scripts/`)

Dự án cung cấp các công cụ tự động hóa để bạn vận hành dễ dàng hơn:

- **Setup môi trường nhanh:**
  ```powershell
  .\scripts\setup_env.ps1
  ```
- **Nạp kiến thức cho Agent (RAG):**
  Bỏ tài liệu vào `data/raw/` và chạy:
  ```bash
  python scripts/build_embeddings.py
  ```
- **Dọn dẹp hệ thống (Logs/Cache):**
  ```bash
  python scripts/cleanup.py
  ```
- **Kiểm tra kết nối AI:**
  ```bash
  python scripts/test_connection.py
  ```
