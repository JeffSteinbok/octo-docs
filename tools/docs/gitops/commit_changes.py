#!/usr/bin/env python3
"""
Stage and commit generated documentation changes.

Usage:
    python tools/docs/gitops/commit_changes.py [--docs-dir ./docs]
"""

import argparse
import subprocess
import sys

from docs.gitops.exceptions import GitCommandError


def commit_changes(docs_dir: str = "./docs", author_name: str = "", author_email: str = "") -> bool:
    """
    Stage and commit changes in the docs directory.

    Returns True if a commit was made, False if there were no changes.
    Raises GitCommandError on git failures.
    """
    try:
        if author_name:
            subprocess.run(["git", "config", "user.name", author_name], check=True,
                           capture_output=True, text=True)
        if author_email:
            subprocess.run(["git", "config", "user.email", author_email], check=True,
                           capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise GitCommandError("git config", getattr(exc, "stderr", "")) from exc

    # Stage docs changes
    result = subprocess.run(
        ["git", "add", docs_dir],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise GitCommandError("git add", result.stderr)

    # Check if there's anything to commit (returncode 1 = changes, 0 = clean)
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True,
        text=True,
    )
    if status.returncode == 0:
        print("No changes to commit.")
        return False
    if status.returncode != 1:
        raise GitCommandError("git diff --cached", status.stderr)

    # Commit
    commit_result = subprocess.run(
        ["git", "commit", "-m", "docs: update generated documentation from bundle"],
        capture_output=True,
        text=True,
    )
    if commit_result.returncode != 0:
        raise GitCommandError("git commit", commit_result.stderr)

    print("Changes committed successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Commit generated documentation changes.")
    parser.add_argument("--docs-dir", default="./docs", help="Path to docs directory")
    parser.add_argument("--author-name", default="github-actions[bot]")
    parser.add_argument("--author-email", default="github-actions[bot]@users.noreply.github.com")
    args = parser.parse_args()
    try:
        commit_changes(args.docs_dir, args.author_name, args.author_email)
    except GitCommandError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
