import os
import sys
from mcp.server.fastmcp import FastMCP

# Thêm thư mục gốc vào path để import được các module khác
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.tools.system_tools import SystemTools

# Khởi tạo Vibe MCP Server
mcp = FastMCP("Vibe Coding Server")

@mcp.tool()
def list_directory(path: str = ".") -> str:
    """List files and directories in a given path."""
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
def analyze_codebase(path: str = ".") -> str:
    """Analyze the entire project structure recursively to understand the context."""
    return SystemTools.list_files_recursive(path)

@mcp.tool()
def read_files(paths: list[str]) -> str:
    """Read the content of multiple files to understand logic across different modules."""
    return SystemTools.read_files(paths)

@mcp.tool()
def create_new_file(path: str, content: str) -> str:
    """Create a new file with specified content."""
    return SystemTools.create_file(path, content)

@mcp.tool()
def edit_existing_file(path: str, old_content: str, new_content: str) -> str:
    """Edit a file by replacing a specific block of text."""
    return SystemTools.edit_file(path, old_content, new_content)

@mcp.tool()
def run_shell_command(command: str) -> str:
    """Execute a terminal command and return the output."""
    return SystemTools.run_command(command)

@mcp.tool()
def undo_last_vibe_action() -> str:
    """Undo the last file creation or edit action."""
    return SystemTools.undo_last_action()

if __name__ == "__main__":
    mcp.run()
