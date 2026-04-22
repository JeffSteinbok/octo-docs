"""Tests for tools/docs/output/write_page.py"""

import sys
from pathlib import Path

_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TOOLS_ROOT))

from docs.output.write_page import write_page


class TestWritePage:
    def test_writes_plain_content(self, tmp_path):
        out = tmp_path / "page.md"
        write_page(out, "Hello world")
        assert out.read_text(encoding="utf-8") == "Hello world"

    def test_creates_parent_directories(self, tmp_path):
        out = tmp_path / "a" / "b" / "page.md"
        write_page(out, "nested")
        assert out.exists()
        assert out.read_text(encoding="utf-8") == "nested"

    def test_writes_front_matter(self, tmp_path):
        out = tmp_path / "page.md"
        write_page(out, "Body text", front_matter={"title": "Test", "layout": "default"})
        content = out.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert "title: Test" in content
        assert "layout: default" in content
        assert content.endswith("Body text")

    def test_no_front_matter_when_none(self, tmp_path):
        out = tmp_path / "page.md"
        write_page(out, "No FM")
        content = out.read_text(encoding="utf-8")
        assert not content.startswith("---")

    def test_no_front_matter_when_empty_dict(self, tmp_path):
        out = tmp_path / "page.md"
        write_page(out, "No FM", front_matter={})
        content = out.read_text(encoding="utf-8")
        assert not content.startswith("---")

    def test_accepts_string_path(self, tmp_path):
        out = str(tmp_path / "page.md")
        write_page(out, "string path")
        assert Path(out).read_text(encoding="utf-8") == "string path"

    def test_overwrites_existing_file(self, tmp_path):
        out = tmp_path / "page.md"
        out.write_text("old content")
        write_page(out, "new content")
        assert out.read_text(encoding="utf-8") == "new content"
