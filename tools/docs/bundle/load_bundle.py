#!/usr/bin/env python3
"""Bundle loader: reads sanitized bundle files from a local directory."""

import json
import os
from pathlib import Path


class BundleLoader:
    """Loads and exposes bundle artifacts by relative path."""

    def __init__(self, bundle_root: str):
        self.bundle_root = Path(bundle_root).resolve()
        if not self.bundle_root.is_dir():
            raise FileNotFoundError(f"Bundle root not found: {self.bundle_root}")

    def load_json(self, relative_path: str) -> dict:
        """Load a JSON file from the bundle."""
        full_path = self.bundle_root / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Bundle file not found: {relative_path}")
        with open(full_path, encoding="utf-8") as f:
            return json.load(f)

    def load_text(self, relative_path: str) -> str:
        """Load a text/markdown file from the bundle."""
        full_path = self.bundle_root / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Bundle file not found: {relative_path}")
        return full_path.read_text(encoding="utf-8")

    def load_manifest(self) -> dict:
        """Load the bundle manifest.json."""
        return self.load_json("manifest.json")

    def load_changed_pages(self) -> list:
        """Load the list of changed page IDs from changed_pages.json."""
        data = self.load_json("changed_pages.json")
        return data.get("pages", [])

    def exists(self, relative_path: str) -> bool:
        """Check if a bundle artifact exists."""
        return (self.bundle_root / relative_path).exists()

    def glob(self, pattern: str) -> list:
        """Return relative paths matching a glob pattern within the bundle."""
        matches = sorted(self.bundle_root.glob(pattern))
        return [str(m.relative_to(self.bundle_root)) for m in matches if m.is_file()]
