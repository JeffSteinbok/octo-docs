"""Merge satellite bundle plugin detail into the primary docs bundle."""

from __future__ import annotations

import shutil
from pathlib import Path

from docs.bundle.load_bundle import BundleLoader


def merge_openclaw_hub_plugins(primary_root: str | Path, satellite_root: str | Path) -> list[str]:
    """Copy hub-backed plugin chunks into the primary bundle.

    The primary `runtime-plugins.json` inventory decides which plugin IDs are
    sourced from `openclaw-hub` and should therefore receive first-class plugin
    detail pages from the satellite bundle.
    """

    primary_path = Path(primary_root).resolve()
    satellite_path = Path(satellite_root).resolve()
    primary_bundle = BundleLoader(str(primary_path))
    satellite_bundle = BundleLoader(str(satellite_path))

    if not primary_bundle.exists("runtime-plugins.json"):
        return []

    inventory = primary_bundle.load_json("runtime-plugins.json").get("plugins", [])
    desired_ids = [
        entry.get("id")
        for entry in inventory
        if isinstance(entry, dict)
        and entry.get("origin") == "openclaw-hub"
        and entry.get("docs_mode") == "local"
        and isinstance(entry.get("id"), str)
    ]

    merged: list[str] = []
    plugins_dir = primary_path / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    for plugin_id in desired_ids:
        relative_path = f"plugins/{plugin_id}.json"
        if not satellite_bundle.exists(relative_path):
            raise FileNotFoundError(f"Satellite bundle is missing required plugin chunk: {relative_path}")
        shutil.copy2(satellite_path / relative_path, plugins_dir / f"{plugin_id}.json")
        merged.append(plugin_id)

    return merged
