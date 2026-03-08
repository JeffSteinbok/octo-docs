#!/usr/bin/env python3
"""Page writer: ensures directories exist and writes the final page file."""

from pathlib import Path


def write_page(output_path: Path, content: str) -> None:
    """
    Write formatted markdown content to the given output path.

    Creates parent directories as needed.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
