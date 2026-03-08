#!/usr/bin/env python3
"""
Create a new git branch for generated documentation updates.

Usage:
    python tools/docs/gitops/create_branch.py [--bundle-root ./bundle]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_bundle_info(bundle_root: str) -> dict:
    """Load manifest info from the bundle if available."""
    manifest_path = Path(bundle_root) / "manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def create_branch(bundle_root: str = "./bundle") -> str:
    """
    Create a new git branch for the docs update.

    Returns the branch name.
    """
    manifest = get_bundle_info(bundle_root)
    commit_sha = manifest.get("commit", "")[:7] if manifest.get("commit") else ""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")

    if commit_sha:
        branch_name = f"docs/from-bundle-{commit_sha}-{timestamp}"
    else:
        branch_name = f"docs/update-{timestamp}"

    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error creating branch: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"Created branch: {branch_name}")
    return branch_name


def main():
    parser = argparse.ArgumentParser(description="Create a docs update branch.")
    parser.add_argument("--bundle-root", default="./bundle", help="Path to bundle directory")
    args = parser.parse_args()
    create_branch(args.bundle_root)


if __name__ == "__main__":
    main()
