#!/usr/bin/env python3
"""Page writer: ensures directories exist and writes the final page file."""

from pathlib import Path


def write_page(output_path: Path, content: str, front_matter: dict = None) -> None:
    """
    Write formatted markdown content to the given output path.

    Optionally prepends Jekyll front matter (YAML) if provided.
    Creates parent directories as needed.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if front_matter:
        import yaml
        fm_yaml = yaml.dump(front_matter, default_flow_style=False, sort_keys=False)
        content = f"---\n{fm_yaml}---\n\n{content}"

    output_path.write_text(content, encoding="utf-8")
