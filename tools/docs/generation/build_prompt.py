#!/usr/bin/env python3
"""Prompt builder: assembles the full LLM prompt for a documentation page."""

import json
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {filename}")
    return path.read_text(encoding="utf-8").strip()


def build_prompt(page_spec: dict, selected_sources: dict) -> str:
    """
    Build the full LLM prompt for a documentation page.

    Args:
        page_spec: The parsed page spec dict (id, template, instructions, output_path)
        selected_sources: The normalized source material dict from selectors

    Returns:
        A string prompt ready to send to the LLM API.
    """
    base = _load_prompt("base_prompt.md")
    template_name = page_spec.get("template", "overview")
    template = _load_prompt(f"{template_name}.md")

    instructions = page_spec.get("instructions", {})
    audience = instructions.get("audience", "developers")
    include = instructions.get("include", [])
    exclude = instructions.get("exclude", [])

    source_material = selected_sources.get("source_material", {})

    parts = [
        base,
        "",
        template,
        "",
        "## Page Metadata",
        f"- Page ID: {page_spec.get('id', '')}",
        f"- Audience: {audience}",
        f"- Output path: {page_spec.get('output_path', '')}",
        "",
    ]

    if include:
        parts.append("## Include in this page")
        for item in include:
            parts.append(f"- {item}")
        parts.append("")

    if exclude:
        parts.append("## Exclude from this page")
        for item in exclude:
            parts.append(f"- {item}")
        parts.append("")

    parts.append("## Source Material")
    parts.append("")

    for source_path, content in source_material.items():
        parts.append(f"### {source_path}")
        if isinstance(content, (dict, list)):
            parts.append("```json")
            parts.append(json.dumps(content, indent=2))
            parts.append("```")
        else:
            parts.append(str(content))
        parts.append("")

    return "\n".join(parts)
