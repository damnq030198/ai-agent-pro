# 📜 Project Rules & Standards

## Code Quality
- **Clean Code:** Tuân thủ nguyên tắc SOLID và DRY.
- **Naming:** CamelCase cho class, snake_case cho biến/hàm (Python). camelCase cho Node.js.
- **Documentation:** Luôn có docstrings cho các class và method quan trọng.

## AI Workflow
- **Spec First:** Không viết code khi chưa có file SPEC.md được phê duyệt.
- **Task Breakdown:** Chia nhỏ công việc thành các task không quá 100 dòng code.
- **Testing:** Unit test là bắt buộc cho các core logic.

## Security
- **API Keys:** Tuyệt đối không commit API keys. Sử dụng `.env`.
- **Validation:** Luôn validate input từ người dùng trước khi đưa vào LLM.
