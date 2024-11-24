import git
from typing import List

class GitHandler:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.repo_path = repo_path

    def get_changed_files(self) -> List[str]:
        """Get list of changed files in current branch compared to base"""
        # Get the diff between current branch and origin/main
        diff = self.repo.head.commit.diff('origin/main')
        
        # Filter for .sql files
        return [d.a_path for d in diff if d.a_path.endswith('.sql')]

    def get_old_content(self, file_path: str) -> str:
        """Get file content from base branch"""
        try:
            return self.repo.git.show(f'origin/main:{file_path}')
        except git.exc.GitCommandError:
            return ""

    def get_new_content(self, file_path: str) -> str:
        """Get current file content"""
        try:
            with open(f"{self.repo_path}/{file_path}", 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""