import os
import subprocess
import shutil
import datetime
from typing import Dict, Any, List

class SystemTools:
    # Lưu lịch sử các thay đổi để Undo
    _action_history = []
    _backup_dir = ".vibe_backups"

    @classmethod
    def _create_backup(cls, path: str):
        """Tạo bản sao lưu cho file trước khi sửa."""
        if not os.path.exists(path): return None
        
        os.makedirs(cls._backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(cls._backup_dir, f"{os.path.basename(path)}_{timestamp}.bak")
        shutil.copy2(path, backup_path)
        return backup_path

    @classmethod
    def create_file(cls, path: str, content: str) -> str:
        """Tạo một file mới với nội dung cho trước."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            # Lưu lại trạng thái trước đó (nếu file đã tồn tại)
            backup = cls._create_backup(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            cls._action_history.append({"type": "create", "path": path, "backup": backup})
            return f"Successfully created file: {path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"

    @classmethod
    def edit_file(cls, path: str, old_content: str, new_content: str) -> str:
        """Sửa nội dung file bằng cách thay thế chuỗi."""
        try:
            if not os.path.exists(path):
                return f"Error: File {path} does not exist."
            
            backup = cls._create_backup(path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if old_content not in content:
                return f"Error: Original content not found in {path}"
            
            updated_content = content.replace(old_content, new_content)
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            
            cls._action_history.append({"type": "edit", "path": path, "backup": backup})
            return f"Successfully updated file: {path}"
        except Exception as e:
            return f"Error editing file: {str(e)}"

    @classmethod
    def undo_last_action(cls) -> str:
        """Hoàn tác hành động gần nhất."""
        if not cls._action_history:
            return "No actions to undo."
        
        last_action = cls._action_history.pop()
        path = last_action["path"]
        backup = last_action["backup"]

        try:
            if last_action["type"] == "create" and not backup:
                # Nếu là tạo mới hoàn toàn, thì xóa đi
                os.remove(path)
                return f"Undo: Removed created file {path}"
            elif backup:
                # Nếu có bản sao lưu, thì khôi phục lại
                shutil.copy2(backup, path)
                return f"Undo: Restored {path} from backup."
            return "Undo failed: No backup available."
        except Exception as e:
            return f"Undo error: {str(e)}"

    @classmethod
    def list_files_recursive(cls, startpath: str = ".", exclude_dirs: List[str] = None) -> str:
        """Liệt kê toàn bộ cấu trúc thư mục dự án."""
        if exclude_dirs is None:
            exclude_dirs = [".git", "node_modules", "__pycache__", ".next", "venv", ".vibe_backups"]
        
        output = []
        for root, dirs, files in os.walk(startpath):
            # Loại bỏ các thư mục không mong muốn
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            output.append(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                output.append(f"{sub_indent}{f}")
        
        return "\n".join(output)

    @classmethod
    def read_files(cls, file_paths: List[str]) -> str:
        """Đọc nội dung của nhiều file cùng lúc."""
        results = []
        for path in file_paths:
            try:
                if os.path.isfile(path):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    results.append(f"--- FILE: {path} ---\n{content}\n")
                else:
                    results.append(f"--- FILE: {path} --- (Not found or not a file)\n")
            except Exception as e:
                results.append(f"--- FILE: {path} --- (Error: {str(e)})\n")
        
        return "\n".join(results)

    @staticmethod
    def run_command(command: str) -> str:
        """Chạy một lệnh terminal."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            output = result.stdout if result.returncode == 0 else result.stderr
            return f"Command executed (Return code: {result.returncode})\nOutput: {output}"
        except Exception as e:
            return f"Error running command: {str(e)}"

# Registry để map tên tool với hàm xử lý
TOOLS_REGISTRY = {
    "create_file": SystemTools.create_file,
    "edit_file": SystemTools.edit_file,
    "run_command": SystemTools.run_command,
    "undo_last_action": SystemTools.undo_last_action
}

# Khai báo định nghĩa tool cho LLM (Gemini format)
TOOLS_DEFINITION = [
    # ... (giữ nguyên các tool cũ)
    {
        "name": "create_file",
        "description": "Create a new file with specified content.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute or relative path to the file."},
                "content": {"type": "string", "description": "Content to write into the file."}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit an existing file by replacing a block of text.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file."},
                "old_content": {"type": "string", "description": "The exact text to be replaced."},
                "new_content": {"type": "string", "description": "The new text to insert."}
            },
            "required": ["path", "old_content", "new_content"]
        }
    },
    {
        "name": "run_command",
        "description": "Execute a terminal command.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to run."}
            },
            "required": ["command"]
        }
    },
    {
        "name": "undo_last_action",
        "description": "Revert the last file creation or edit action.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]
