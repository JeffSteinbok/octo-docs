#!/usr/bin/env python3
"""Markdown formatter: cleans up LLM output before writing."""

import re


def format_markdown(content: str) -> str:
    """
    Normalize and clean up LLM-generated markdown content.

    - Strips leading/trailing whitespace
    - Normalizes line endings to LF
    - Removes wrapping code fences (```markdown ... ```)
    - Ensures a single trailing newline
    - Enforces at most one H1 heading
    - Removes meta-commentary lines
    """
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = content.strip()

    # Strip wrapping markdown code fence if present
    content = _strip_wrapping_fence(content)

    content = content.strip()

    # Remove LLM meta-commentary at the start or end
    content = _strip_meta_commentary(content)

    # Normalize spacing around headings
    content = _normalize_heading_spacing(content)

    # Enforce single H1
    content = _enforce_single_h1(content)

    # Ensure single trailing newline
    content = content.rstrip("\n") + "\n"

    return content


def _strip_wrapping_fence(content: str) -> str:
    """Remove a wrapping ```markdown ... ``` fence if present."""
    pattern = r"^```(?:markdown|md)?\s*\n(.*)\n```\s*$"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content


def _strip_meta_commentary(content: str) -> str:
    """Remove lines that are clearly LLM meta-commentary."""
    meta_patterns = [
        r"^Here(?:'s| is) (?:the|your|a) (?:generated |updated |revised )?(?:documentation|page|markdown|content).*$",
        r"^I(?:'ve| have) generated.*$",
        r"^---+\s*$",
    ]
    lines = content.split("\n")
    # Check first line
    for pattern in meta_patterns[:2]:
        if lines and re.match(pattern, lines[0], re.IGNORECASE):
            lines = lines[1:]
            # Strip blank lines at start
            while lines and not lines[0].strip():
                lines = lines[1:]
            break
    return "\n".join(lines)


def _normalize_heading_spacing(content: str) -> str:
    """Ensure a blank line before each heading (except the very first line)."""
    lines = content.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i > 0 and re.match(r"^#{1,6} ", line):
            if result and result[-1].strip():
                result.append("")
        result.append(line)
    return "\n".join(result)


def _enforce_single_h1(content: str) -> str:
    """Demote extra H1 headings to H2 if more than one H1 exists."""
    lines = content.split("\n")
    h1_count = sum(1 for line in lines if re.match(r"^# [^#]", line))
    if h1_count <= 1:
        return content

    first_h1_seen = False
    result = []
    for line in lines:
        if re.match(r"^# [^#]", line):
            if first_h1_seen:
                line = "#" + line  # demote to H2
            else:
                first_h1_seen = True
        result.append(line)
    return "\n".join(result)
