import os
import sys
from mcp.server.fastmcp import FastMCP

# Thêm thư mục gốc vào path để import được các module khác
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.tools.github_tools import GitHubTools

# Khởi tạo Git MCP Server
mcp = FastMCP("Git & GitHub Server")

@mcp.tool()
def get_github_pr_details(repo_name: str, pr_number: int) -> str:
    """Fetch details and diff of a GitHub Pull Request for review."""
    return GitHubTools.get_pr_details(repo_name, pr_number)

@mcp.tool()
def post_github_pr_comment(repo_name: str, pr_number: int, comment: str) -> str:
    """Post a review comment or summary to a GitHub Pull Request."""
    return GitHubTools.post_pr_comment(repo_name, pr_number, comment)

if __name__ == "__main__":
    mcp.run()
