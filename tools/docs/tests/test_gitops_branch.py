"""Tests for tools/docs/gitops/create_branch.py"""

import json
import subprocess
from unittest.mock import MagicMock, patch

import pytest

import sys
from pathlib import Path

_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TOOLS_ROOT))

from docs.gitops.create_branch import create_branch, get_bundle_info
from docs.gitops.exceptions import GitCommandError


def _mock_run(returncode=0, stdout="", stderr=""):
    m = MagicMock(spec=subprocess.CompletedProcess)
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


class TestGetBundleInfo:
    def test_loads_valid_manifest(self, tmp_path):
        manifest = {"commit": "abc1234def", "bundle_version": "2"}
        (tmp_path / "manifest.json").write_text(json.dumps(manifest))
        assert get_bundle_info(str(tmp_path)) == manifest

    def test_returns_empty_for_missing_manifest(self, tmp_path):
        assert get_bundle_info(str(tmp_path)) == {}

    def test_returns_empty_for_invalid_json(self, tmp_path):
        (tmp_path / "manifest.json").write_text("not json")
        assert get_bundle_info(str(tmp_path)) == {}


class TestCreateBranch:
    @patch("docs.gitops.create_branch.subprocess.run")
    def test_branch_name_includes_commit_sha(self, mock_run, tmp_path):
        manifest = {"commit": "abc1234def5678"}
        (tmp_path / "manifest.json").write_text(json.dumps(manifest))
        mock_run.return_value = _mock_run(0)

        name = create_branch(str(tmp_path))
        assert name.startswith("docs/from-bundle-abc1234-")
        # Verify seconds are included in timestamp (format: YYYYMMDD-HHMMSS)
        # Full name: docs/from-bundle-abc1234-YYYYMMDD-HHMMSS
        parts = name.replace("docs/from-bundle-abc1234-", "")
        assert len(parts) == 15  # YYYYMMDD-HHMMSS

    @patch("docs.gitops.create_branch.subprocess.run")
    def test_branch_name_without_manifest(self, mock_run, tmp_path):
        mock_run.return_value = _mock_run(0)
        name = create_branch(str(tmp_path))
        assert name.startswith("docs/update-")

    @patch("docs.gitops.create_branch.subprocess.run")
    def test_git_checkout_failure_raises(self, mock_run, tmp_path):
        mock_run.return_value = _mock_run(128, stderr="fatal: branch already exists")
        with pytest.raises(GitCommandError, match="git checkout"):
            create_branch(str(tmp_path))

    @patch("docs.gitops.create_branch.subprocess.run")
    def test_empty_commit_uses_update_prefix(self, mock_run, tmp_path):
        manifest = {"commit": ""}
        (tmp_path / "manifest.json").write_text(json.dumps(manifest))
        mock_run.return_value = _mock_run(0)
        name = create_branch(str(tmp_path))
        assert name.startswith("docs/update-")
