"""Custom exceptions for gitops operations."""


class GitOpsError(Exception):
    """Base exception for all gitops failures."""


class GitCommandError(GitOpsError):
    """Raised when a local git command fails."""

    def __init__(self, command: str, stderr: str = ""):
        self.command = command
        self.stderr = stderr
        detail = f": {stderr}" if stderr else ""
        super().__init__(f"git command failed ({command}){detail}")


class GitHubAPIError(GitOpsError):
    """Raised when a GitHub API request fails."""

    def __init__(self, action: str, status_code: int = 0, detail: str = ""):
        self.action = action
        self.status_code = status_code
        self.detail = detail
        parts = [f"GitHub API error during {action}"]
        if status_code:
            parts.append(f"HTTP {status_code}")
        if detail:
            parts.append(detail)
        super().__init__(" — ".join(parts))


class GitOpsConfigError(GitOpsError):
    """Raised when required configuration is missing or invalid."""
