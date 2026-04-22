"""Tests for tools/docs/gitops/open_pr.py"""

import json
import subprocess
from unittest.mock import MagicMock, patch, ANY

import pytest

import sys
from pathlib import Path

_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TOOLS_ROOT))

from docs.gitops.open_pr import (
    _build_pr_body,
    _parse_repo,
    _cleanup_stale_branches,
    open_pr,
    _api_request,
    _REQUEST_TIMEOUT,
)
from docs.gitops.exceptions import GitCommandError, GitHubAPIError, GitOpsConfigError


def _mock_run(returncode=0, stdout="", stderr=""):
    m = MagicMock(spec=subprocess.CompletedProcess)
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


# --- _build_pr_body (pure function) ---

class TestBuildPrBody:
    def test_with_full_manifest(self):
        manifest = {"commit": "abc123", "bundle_version": "5", "generated_at": "2025-01-01"}
        body = _build_pr_body(manifest, ["page-a", "page-b"])
        assert "`abc123`" in body
        assert "`5`" in body
        assert "- `page-a`" in body
        assert "- `page-b`" in body

    def test_empty_manifest_uses_unknown(self):
        body = _build_pr_body({}, [])
        assert "`unknown`" in body
        assert "_none_" in body

    def test_no_pages_shows_none(self):
        body = _build_pr_body({"commit": "abc"}, [])
        assert "_none_" in body


# --- _parse_repo ---

class TestParseRepo:
    def test_valid_repo(self):
        assert _parse_repo("owner/repo") == ("owner", "repo")

    def test_repo_with_extra_slash(self):
        owner, repo = _parse_repo("owner/repo/extra")
        assert owner == "owner"
        assert repo == "repo/extra"

    def test_missing_slash_raises(self):
        with pytest.raises(GitOpsConfigError, match="owner/repo"):
            _parse_repo("noslash")

    def test_empty_owner_raises(self):
        with pytest.raises(GitOpsConfigError):
            _parse_repo("/repo")

    def test_empty_repo_raises(self):
        with pytest.raises(GitOpsConfigError):
            _parse_repo("owner/")

    def test_empty_string_raises(self):
        with pytest.raises(GitOpsConfigError):
            _parse_repo("")

    def test_none_raises(self):
        with pytest.raises(GitOpsConfigError):
            _parse_repo(None)


# --- _api_request timeout ---

class TestApiRequest:
    @patch("urllib.request.urlopen")
    def test_timeout_is_passed(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        _api_request("https://api.github.com/test", "fake-token")
        mock_urlopen.assert_called_once_with(ANY, timeout=_REQUEST_TIMEOUT)


# --- _cleanup_stale_branches ---

class TestCleanupStaleBranches:
    @patch("docs.gitops.open_pr.subprocess.run")
    @patch("docs.gitops.open_pr._api_request")
    def test_skips_current_branch(self, mock_api, mock_run):
        mock_run.return_value = _mock_run(
            0, stdout="abc123\trefs/heads/docs/current-branch\n"
        )
        _cleanup_stale_branches("tok", "owner", "repo", "docs/current-branch")
        mock_api.assert_not_called()

    @patch("docs.gitops.open_pr.subprocess.run")
    @patch("docs.gitops.open_pr._api_request")
    def test_deletes_orphaned_branch(self, mock_api, mock_run):
        mock_run.side_effect = [
            _mock_run(0, stdout="abc\trefs/heads/docs/old-branch\n"),  # ls-remote
            _mock_run(0),  # git push --delete
        ]
        mock_api.return_value = []  # No PR for this branch

        _cleanup_stale_branches("tok", "owner", "repo", "docs/current")
        # Should have called git push --delete
        delete_call = mock_run.call_args_list[1]
        assert "--delete" in delete_call[0][0]
        assert "docs/old-branch" in delete_call[0][0]

    @patch("docs.gitops.open_pr.subprocess.run")
    @patch("docs.gitops.open_pr._api_request")
    def test_keeps_branch_with_open_pr(self, mock_api, mock_run):
        mock_run.return_value = _mock_run(
            0, stdout="abc\trefs/heads/docs/active-branch\n"
        )
        mock_api.return_value = [{"state": "open"}]

        _cleanup_stale_branches("tok", "owner", "repo", "docs/current")
        # Only ls-remote called, no delete
        assert mock_run.call_count == 1

    @patch("docs.gitops.open_pr.subprocess.run")
    @patch("docs.gitops.open_pr._api_request")
    def test_deletes_branch_with_closed_pr(self, mock_api, mock_run):
        mock_run.side_effect = [
            _mock_run(0, stdout="abc\trefs/heads/docs/merged-branch\n"),
            _mock_run(0),  # git push --delete
        ]
        mock_api.return_value = [{"state": "closed"}]

        _cleanup_stale_branches("tok", "owner", "repo", "docs/current")
        assert mock_run.call_count == 2

    @patch("docs.gitops.open_pr.subprocess.run")
    def test_handles_ls_remote_failure(self, mock_run):
        mock_run.return_value = _mock_run(1)
        # Should not raise
        _cleanup_stale_branches("tok", "owner", "repo", "docs/current")


# --- open_pr config validation ---

class TestOpenPrConfig:
    def test_missing_token_raises(self):
        with patch.dict("os.environ", {"GITHUB_REPOSITORY": "o/r"}, clear=True):
            with pytest.raises(GitOpsConfigError, match="GITHUB_TOKEN"):
                open_pr()

    def test_missing_repo_raises(self):
        with patch.dict("os.environ", {"GITHUB_TOKEN": "tok"}, clear=True):
            with pytest.raises(GitOpsConfigError, match="GITHUB_REPOSITORY"):
                open_pr()

    def test_invalid_repo_format_raises(self):
        with patch.dict("os.environ", {"GITHUB_TOKEN": "tok", "GITHUB_REPOSITORY": "noslash"}, clear=True):
            with pytest.raises(GitOpsConfigError, match="owner/repo"):
                open_pr()


# --- open_pr end-to-end (mocked) ---

class TestOpenPrFlow:
    @patch("docs.gitops.open_pr._cleanup_stale_branches")
    @patch("docs.gitops.open_pr._try_enable_auto_merge")
    @patch("docs.gitops.open_pr._try_add_label")
    @patch("docs.gitops.open_pr._api_request")
    @patch("docs.gitops.open_pr.subprocess.run")
    def test_successful_pr_creation(self, mock_run, mock_api, mock_label, mock_merge, mock_cleanup, tmp_path):
        manifest = {"commit": "abc123", "bundle_version": "1", "generated_at": "now"}
        (tmp_path / "manifest.json").write_text(json.dumps(manifest))
        (tmp_path / "changed_pages.json").write_text(json.dumps({"pages": ["p1"]}))

        mock_run.side_effect = [
            _mock_run(0, stdout="docs/test-branch\n"),  # git rev-parse
            _mock_run(0),  # git push
            _mock_run(0, stdout="  HEAD branch: main\n"),  # git remote show
        ]
        mock_api.return_value = {"html_url": "https://github.com/test/pr/1", "number": 42}

        with patch.dict("os.environ", {"GITHUB_TOKEN": "tok", "GITHUB_REPOSITORY": "owner/repo"}):
            open_pr(str(tmp_path))

        # Verify PR was created via API
        mock_api.assert_called_once()
        api_call = mock_api.call_args
        assert "pulls" in api_call[0][0]

        # Verify post-creation steps
        mock_label.assert_called_once_with("tok", "owner", "repo", 42, "generated-docs")
        mock_merge.assert_called_once_with("tok", "owner", "repo", 42)
        mock_cleanup.assert_called_once()

    @patch("docs.gitops.open_pr._api_request")
    @patch("docs.gitops.open_pr.subprocess.run")
    def test_client_error_not_retried(self, mock_run, mock_api, tmp_path):
        mock_run.side_effect = [
            _mock_run(0, stdout="branch\n"),
            _mock_run(0),
            _mock_run(0, stdout="  HEAD branch: main\n"),
        ]
        mock_api.side_effect = GitHubAPIError("POST", 422, "Validation Failed")

        with patch.dict("os.environ", {"GITHUB_TOKEN": "tok", "GITHUB_REPOSITORY": "o/r"}):
            with pytest.raises(GitHubAPIError, match="422"):
                open_pr(str(tmp_path))

        # Client error should not be retried
        assert mock_api.call_count == 1

    @patch("docs.gitops.open_pr.time.sleep")
    @patch("docs.gitops.open_pr._api_request")
    @patch("docs.gitops.open_pr.subprocess.run")
    def test_server_error_retried(self, mock_run, mock_api, mock_sleep, tmp_path):
        mock_run.side_effect = [
            _mock_run(0, stdout="branch\n"),
            _mock_run(0),
            _mock_run(0, stdout="  HEAD branch: main\n"),
        ]
        mock_api.side_effect = [
            GitHubAPIError("POST", 502, "Bad Gateway"),
            GitHubAPIError("POST", 502, "Bad Gateway"),
            {"html_url": "https://github.com/test/pr/1", "number": 1},
        ]

        with patch.dict("os.environ", {"GITHUB_TOKEN": "tok", "GITHUB_REPOSITORY": "o/r"}):
            with patch("docs.gitops.open_pr._try_add_label"), \
                 patch("docs.gitops.open_pr._try_enable_auto_merge"), \
                 patch("docs.gitops.open_pr._cleanup_stale_branches"):
                open_pr(str(tmp_path))

        assert mock_api.call_count == 3
        assert mock_sleep.call_count == 2
