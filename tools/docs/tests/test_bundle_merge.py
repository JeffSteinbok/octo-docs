"""Tests for merging the openclaw-hub satellite bundle into the primary bundle."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_ROOT))

from docs.bundle.merge_satellite_bundle import merge_openclaw_hub_plugins


def test_merge_openclaw_hub_plugins_copies_only_hub_backed_plugins(tmp_path):
    primary = tmp_path / "primary"
    satellite = tmp_path / "satellite"
    (primary / "plugins").mkdir(parents=True)
    (satellite / "plugins").mkdir(parents=True)

    (primary / "manifest.json").write_text(json.dumps({"artifacts": ["runtime-plugins.json"]}), encoding="utf-8")
    (primary / "runtime-plugins.json").write_text(
        json.dumps(
            {
                "plugins": [
                    {"id": "stock-quotes", "origin": "openclaw-hub", "docs_mode": "local"},
                    {"id": "fastmail", "origin": "octo", "docs_mode": "local"},
                    {"id": "telegram", "origin": "external", "docs_mode": "external"},
                ]
            }
        ),
        encoding="utf-8",
    )
    (satellite / "manifest.json").write_text(json.dumps({"artifacts": ["plugins/stock-quotes.json"]}), encoding="utf-8")
    (satellite / "plugins" / "stock-quotes.json").write_text(json.dumps({"plugin": "stock-quotes"}), encoding="utf-8")

    merged = merge_openclaw_hub_plugins(primary, satellite)

    assert merged == ["stock-quotes"]
    assert json.loads((primary / "plugins" / "stock-quotes.json").read_text(encoding="utf-8"))["plugin"] == "stock-quotes"
    assert not (primary / "plugins" / "fastmail.json").exists()


def test_merge_openclaw_hub_plugins_skips_missing_satellite_chunk(tmp_path):
    primary = tmp_path / "primary"
    satellite = tmp_path / "satellite"
    primary.mkdir()
    satellite.mkdir()

    (primary / "manifest.json").write_text(json.dumps({"artifacts": ["runtime-plugins.json"]}), encoding="utf-8")
    (primary / "runtime-plugins.json").write_text(
        json.dumps({"plugins": [{"id": "stock-quotes", "origin": "openclaw-hub", "docs_mode": "local"}]}),
        encoding="utf-8",
    )
    (satellite / "manifest.json").write_text(json.dumps({"artifacts": []}), encoding="utf-8")

    merged = merge_openclaw_hub_plugins(primary, satellite)
    assert merged == []
