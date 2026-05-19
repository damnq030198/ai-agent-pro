import os
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GitHubTools:
    _github_client = None

    @classmethod
    def _get_client(cls):
        if cls._github_client is None:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise ValueError("GITHUB_TOKEN not found in environment variables. Please add it to your .env file.")
            cls._github_client = Github(token)
        return cls._github_client

    @classmethod
    def get_pr_details(cls, repo_name: str, pr_number: int) -> str:
        """
        Fetches the details and diff of a specific Pull Request.
        :param repo_name: Full repository name (e.g., 'owner/repo').
        :param pr_number: Pull request number.
        """
        try:
            g = cls._get_client()
            repo = g.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            files = pr.get_files()
            summary = [
                f"PR #{pr_number}: {pr.title}", 
                f"Author: {pr.user.login}", 
                f"State: {pr.state}", 
                f"Description: {pr.body}",
                "\nFiles changed:"
            ]
            
            detailed_diff = []
            for file in files:
                summary.append(f"- {file.filename} ({file.status}: +{file.additions}, -{file.deletions})")
                if file.patch:
                    detailed_diff.append(f"--- FILE: {file.filename} ---\n{file.patch}\n")
                else:
                    detailed_diff.append(f"--- FILE: {file.filename} ---\n(No patch available, possibly a large file or binary)\n")
            
            return "\n".join(summary) + "\n\nDetailed Changes:\n" + "\n".join(detailed_diff)
        except Exception as e:
            return f"Error fetching PR details: {str(e)}"

    @classmethod
    def post_pr_comment(cls, repo_name: str, pr_number: int, body: str) -> str:
        """
        Posts a comment to a Pull Request.
        :param repo_name: Full repository name (e.g., 'owner/repo').
        :param pr_number: Pull request number.
        :param body: The content of the comment (your review).
        """
        try:
            g = cls._get_client()
            repo = g.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(body)
            return f"Successfully posted review comment to PR #{pr_number}"
        except Exception as e:
            return f"Error posting comment: {str(e)}"
