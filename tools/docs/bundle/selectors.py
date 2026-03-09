#!/usr/bin/env python3
"""Source selectors: reads page specs and selects relevant bundle content."""

from pathlib import Path
from .load_bundle import BundleLoader


def select_source(bundle: BundleLoader, source_spec: dict) -> object:
    """Load and optionally filter a single source from the bundle."""
    path = source_spec["path"]
    selectors = source_spec.get("select")

    if path.endswith(".json"):
        data = bundle.load_json(path)
        if selectors:
            return {k: data[k] for k in selectors if k in data}
        return data
    else:
        return bundle.load_text(path)


def expand_sources(bundle: BundleLoader, sources: list) -> list:
    """Expand any glob patterns in the sources list into concrete paths.

    A source with a glob character (* or ?) gets expanded to one source
    entry per matching file. Non-glob sources pass through unchanged.
    """
    expanded = []
    for source_spec in sources:
        path = source_spec["path"]
        if "*" in path or "?" in path:
            for match in bundle.glob(path):
                expanded.append({**source_spec, "path": match})
        else:
            expanded.append(source_spec)
    return expanded


def build_source_material(bundle: BundleLoader, page_spec: dict) -> dict:
    """
    Read a page spec and load selected source material from the bundle.

    Returns a normalized dict suitable for prompt generation.
    """
    sources = expand_sources(bundle, page_spec.get("sources", []))
    source_material = {}
    for source_spec in sources:
        path = source_spec["path"]
        if not bundle.exists(path):
            continue
        source_material[path] = select_source(bundle, source_spec)

    return {
        "page_id": page_spec["id"],
        "template": page_spec.get("template", "overview"),
        "instructions": page_spec.get("instructions", {}),
        "source_material": source_material,
    }
