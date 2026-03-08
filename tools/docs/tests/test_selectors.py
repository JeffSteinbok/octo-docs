"""Tests for bundle source selectors."""

import json
import os
import tempfile
from pathlib import Path
import sys

# Add tools root to path
_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_ROOT))

from docs.bundle.load_bundle import BundleLoader
from docs.bundle.selectors import select_source, build_source_material


def _make_bundle(files: dict) -> str:
    """Create a temporary bundle directory with the given files."""
    tmp = tempfile.mkdtemp()
    for rel_path, content in files.items():
        full_path = Path(tmp) / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, (dict, list)):
            full_path.write_text(json.dumps(content), encoding="utf-8")
        else:
            full_path.write_text(content, encoding="utf-8")
    return tmp


def test_select_json_with_selectors():
    tmp = _make_bundle({
        "modules/auth.json": {
            "summary": "Auth module",
            "endpoints": ["/login"],
            "internal_secret": "do-not-include",
        }
    })
    try:
        bundle = BundleLoader(tmp)
        result = select_source(bundle, {
            "path": "modules/auth.json",
            "select": ["summary", "endpoints"],
        })
        assert result == {"summary": "Auth module", "endpoints": ["/login"]}
        assert "internal_secret" not in result
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def test_select_json_without_selectors():
    tmp = _make_bundle({
        "modules/auth.json": {"a": 1, "b": 2}
    })
    try:
        bundle = BundleLoader(tmp)
        result = select_source(bundle, {"path": "modules/auth.json"})
        assert result == {"a": 1, "b": 2}
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def test_select_text_file():
    tmp = _make_bundle({
        "concepts/architecture.md": "# Architecture\n\nDetails here."
    })
    try:
        bundle = BundleLoader(tmp)
        result = select_source(bundle, {"path": "concepts/architecture.md"})
        assert "# Architecture" in result
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def test_build_source_material_skips_missing():
    tmp = _make_bundle({
        "modules/auth.json": {"summary": "Auth"},
    })
    try:
        bundle = BundleLoader(tmp)
        page_spec = {
            "id": "auth-overview",
            "template": "overview",
            "instructions": {"audience": "developers"},
            "sources": [
                {"path": "modules/auth.json", "select": ["summary"]},
                {"path": "missing/file.json"},
            ],
        }
        result = build_source_material(bundle, page_spec)
        assert result["page_id"] == "auth-overview"
        assert "modules/auth.json" in result["source_material"]
        assert "missing/file.json" not in result["source_material"]
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def test_bundle_loader_load_changed_pages():
    tmp = _make_bundle({
        "changed_pages.json": {"pages": ["auth-overview", "release-latest"]},
        "manifest.json": {"bundle_version": 7, "commit": "abc1234"},
    })
    try:
        bundle = BundleLoader(tmp)
        pages = bundle.load_changed_pages()
        assert pages == ["auth-overview", "release-latest"]
        manifest = bundle.load_manifest()
        assert manifest["bundle_version"] == 7
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
