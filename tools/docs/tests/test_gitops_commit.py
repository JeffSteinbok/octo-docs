"""Tests for tools/docs/gitops/commit_changes.py"""

import subprocess
from unittest.mock import MagicMock, patch, call

import pytest

import sys
from pathlib import Path

_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TOOLS_ROOT))

from docs.gitops.commit_changes import commit_changes
from docs.gitops.exceptions import GitCommandError


def _mock_run(returncode=0, stdout="", stderr=""):
    """Create a mock CompletedProcess."""
    m = MagicMock(spec=subprocess.CompletedProcess)
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


class TestCommitChangesNoOp:
    """When there are no staged changes, commit_changes returns False."""

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_no_changes_returns_false(self, mock_run):
        # git add succeeds, git diff --cached --quiet returns 0 (clean)
        mock_run.side_effect = [
            _mock_run(0),  # git add
            _mock_run(0),  # git diff --cached --quiet (no changes)
        ]
        assert commit_changes("./docs") is False

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_no_changes_with_author(self, mock_run):
        mock_run.side_effect = [
            _mock_run(0),  # git config user.name
            _mock_run(0),  # git config user.email
            _mock_run(0),  # git add
            _mock_run(0),  # git diff --cached --quiet
        ]
        assert commit_changes("./docs", "bot", "bot@test.com") is False


class TestCommitChangesSuccess:
    """When there are staged changes, commit_changes commits and returns True."""

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_changes_committed(self, mock_run):
        mock_run.side_effect = [
            _mock_run(0),  # git add
            _mock_run(1),  # git diff --cached --quiet (has changes)
            _mock_run(0),  # git commit
        ]
        assert commit_changes("./docs") is True

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_author_config_applied(self, mock_run):
        mock_run.side_effect = [
            _mock_run(0),  # git config user.name
            _mock_run(0),  # git config user.email
            _mock_run(0),  # git add
            _mock_run(1),  # git diff --cached --quiet
            _mock_run(0),  # git commit
        ]
        commit_changes("./docs", "Bot", "bot@example.com")
        # Verify git config was called with the author info
        assert mock_run.call_args_list[0] == call(
            ["git", "config", "user.name", "Bot"],
            check=True, capture_output=True, text=True,
        )


class TestCommitChangesErrors:
    """Git failures raise GitCommandError."""

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_git_add_failure_raises(self, mock_run):
        mock_run.return_value = _mock_run(1, stderr="fatal: not a git repo")
        with pytest.raises(GitCommandError, match="git add"):
            commit_changes("./docs")

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_git_commit_failure_raises(self, mock_run):
        mock_run.side_effect = [
            _mock_run(0),  # git add
            _mock_run(1),  # git diff --cached --quiet (has changes)
            _mock_run(1, stderr="error: commit failed"),  # git commit
        ]
        with pytest.raises(GitCommandError, match="git commit"):
            commit_changes("./docs")

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_git_diff_error_code_raises(self, mock_run):
        """returncode > 1 from git diff indicates an actual error, not just changes."""
        mock_run.side_effect = [
            _mock_run(0),  # git add
            _mock_run(128, stderr="fatal: bad revision"),  # git diff error
        ]
        with pytest.raises(GitCommandError, match="git diff"):
            commit_changes("./docs")

    @patch("docs.gitops.commit_changes.subprocess.run")
    def test_git_config_failure_raises(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "git config", stderr="error")
        with pytest.raises(GitCommandError, match="git config"):
            commit_changes("./docs", author_name="bot")
