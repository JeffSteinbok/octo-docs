#!/usr/bin/env python3
"""
Orchestrator: reads page specs, loads bundle content, calls LLM, writes docs.

Usage:
    python tools/docs/generation/generate_all.py --bundle ./bundle
    python tools/docs/generation/generate_all.py --bundle ./bundle --all
    python tools/docs/generation/generate_all.py --bundle ./bundle --page auth-overview
    python tools/docs/generation/generate_all.py --bundle ./bundle --dry-run
"""

import argparse
import hashlib
import logging
import re
import sys
from pathlib import Path

# Allow running as a script from any working directory
_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TOOLS_ROOT))

from docs.bundle.load_bundle import BundleLoader
from docs.bundle.selectors import build_source_material
from docs.generation.build_prompt import build_prompt
from docs.generation.generate_page import generate_page
from docs.output.write_page import write_page
from docs.output.format_markdown import format_markdown

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml")
    raise SystemExit(1)

logger = logging.getLogger(__name__)

_DOCS_ROOT = _TOOLS_ROOT / "docs"
PAGE_SPECS_DIR = _DOCS_ROOT / "page_specs"
REPO_ROOT = _TOOLS_ROOT.parent
LAST_REF_PATH = REPO_ROOT / ".last_bundle_ref"


def load_page_spec(spec_path: Path) -> dict:
    """Load and parse a YAML page spec file."""
    with open(spec_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_all_page_specs() -> dict:
    """Return a dict mapping page_id -> spec dict for all page specs."""
    specs = {}
    for spec_file in sorted(PAGE_SPECS_DIR.glob("*.yml")):
        spec = load_page_spec(spec_file)
        if spec and "id" in spec:
            specs[spec["id"]] = spec
    return specs


def _bundle_fingerprint(bundle: BundleLoader) -> str | None:
    """Compute a stable content fingerprint of all bundle artifacts.

    Uses a SHA-256 hash of sorted artifact paths and their contents so that
    identical bundle content produces the same fingerprint regardless of the
    source commit (avoids false rebuilds from non-doc commits).
    """
    try:
        manifest = bundle.load_manifest()
        artifacts = sorted(manifest.get("artifacts", []))
    except FileNotFoundError:
        return None

    h = hashlib.sha256()
    for artifact_path in artifacts:
        h.update(artifact_path.encode("utf-8"))
        try:
            data = bundle.load_text(artifact_path)
            h.update(data.encode("utf-8"))
        except FileNotFoundError:
            continue
    return h.hexdigest()


def _read_last_ref() -> str | None:
    """Read the last successfully processed bundle fingerprint."""
    try:
        return LAST_REF_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None


def _write_last_ref(ref: str) -> None:
    """Record the bundle fingerprint after a successful generation run."""
    LAST_REF_PATH.write_text(ref + "\n", encoding="utf-8")


def _slugify(text: str) -> str:
    """Convert text to a lowercase-kebab-case anchor ID (no emojis/special chars)."""
    text = re.sub(r'[^\w\s-]', '', text)  # strip non-word chars (emojis, punctuation)
    return re.sub(r'[\s_]+', '-', text.strip().lower())


def _extract_heading_emoji(markdown: str) -> str | None:
    """Extract the leading emoji from the first H2 heading, if present."""
    match = re.search(r'^##\s+(\S+)\s+', markdown, re.MULTILINE)
    if match:
        token = match.group(1)
        if not token.isascii():
            return token
    return None


def _process_chunked_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Generate a page by processing each chunk source individually.

    Splits the glob source (chunk_source) into separate LLM calls so each
    stays within token limits.  The bullet-list index is built deterministically
    in Python from the generated section headings.
    """
    page_id = page_spec["id"]
    output_path = REPO_ROOT / page_spec["output_path"]
    chunk_pattern = page_spec["chunk_source"]
    instructions = page_spec.get("instructions", {})

    logger.info("Processing chunked page: %s -> %s", page_id, page_spec["output_path"])

    chunk_paths = sorted(bundle.glob(chunk_pattern))
    logger.info("Found %d chunks for pattern: %s", len(chunk_paths), chunk_pattern)

    if dry_run:
        logger.info("[dry-run] Would generate chunked page: %s (%d chunks)", page_id, len(chunk_paths))
        return page_spec["output_path"]

    # Generate each chunk section via its own LLM call
    section_data = []
    for chunk_path in chunk_paths:
        # Extract plugin name from JSON for deterministic anchoring
        try:
            plugin_json = bundle.load_json(chunk_path)
            plugin_name = (
                plugin_json.get("name")
                or plugin_json.get("plugin_name")
                or Path(chunk_path).stem.replace("-", " ").title()
            )
            plugin_desc = plugin_json.get("description", "")
        except Exception:
            plugin_name = Path(chunk_path).stem.replace("-", " ").title()
            plugin_desc = ""

        anchor = _slugify(plugin_name)

        chunk_spec = {
            "id": page_id,
            "output_path": page_spec["output_path"],
            "template": "chunk_section",
            "sources": [{"path": chunk_path}],
            "instructions": {
                "audience": instructions.get("audience", "developers"),
                "include": [
                    f"Generate ONLY the H2 section for the '{plugin_name}' plugin",
                    "Use a fitting emoji in the H2 heading",
                    "List every tool as an H4 heading with the tool name",
                    "Under each tool H4, include the tool's description and a "
                    "parameter table (name, type, description) if available",
                ],
                "exclude": instructions.get("exclude", []),
            },
        }
        selected = build_source_material(bundle, chunk_spec)
        prompt = build_prompt(chunk_spec, selected)
        content = generate_page(prompt)

        emoji = _extract_heading_emoji(content)

        section_data.append({
            "name": plugin_name,
            "description": plugin_desc,
            "anchor": anchor,
            "emoji": emoji,
            "content": content.strip(),
        })
        logger.info("Generated chunk: %s (%s)", chunk_path, plugin_name)

    # Build deterministic index bullet list
    index_lines = []
    for s in section_data:
        prefix = f"{s['emoji']} " if s["emoji"] else ""
        desc = f" — {s['description']}" if s["description"] else ""
        index_lines.append(f"- {prefix}[{s['name']}](#{s['anchor']}){desc}")
    index_block = "\n".join(index_lines)

    # Prepend deterministic anchor tags and assemble final page
    parts = [index_block, ""]
    for s in section_data:
        parts.append(f'<a id="{s["anchor"]}"></a>\n\n{s["content"]}')

    combined = "\n\n".join(parts)
    formatted = format_markdown(combined)
    front_matter = page_spec.get("front_matter")
    write_page(output_path, formatted, front_matter=front_matter)

    logger.info("Written chunked page: %s (%d sections)", output_path, len(section_data))
    return page_spec["output_path"]


def process_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Process a single page: select sources, build prompt, call LLM, write."""
    if page_spec.get("strategy") == "chunked":
        return _process_chunked_page(page_spec, bundle, dry_run)
    page_id = page_spec["id"]
    output_path = REPO_ROOT / page_spec["output_path"]

    logger.info("Processing page: %s -> %s", page_id, page_spec["output_path"])

    selected = build_source_material(bundle, page_spec)
    prompt = build_prompt(page_spec, selected)

    if dry_run:
        logger.info("[dry-run] Would generate page: %s", page_id)
        return page_spec["output_path"]

    raw_content = generate_page(prompt)
    formatted = format_markdown(raw_content)
    front_matter = page_spec.get("front_matter")
    write_page(output_path, formatted, front_matter=front_matter)

    logger.info("Written: %s", output_path)
    return page_spec["output_path"]


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="Generate public documentation pages.")
    parser.add_argument(
        "--bundle",
        required=True,
        help="Path to the sanitized docs bundle directory",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Regenerate all pages, ignoring changed_pages.json",
    )
    parser.add_argument(
        "--page",
        metavar="PAGE_ID",
        help="Regenerate a single page by ID",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without calling the LLM or writing files",
    )
    args = parser.parse_args()

    bundle = BundleLoader(args.bundle)
    all_specs = get_all_page_specs()

    if not all_specs:
        logger.warning("No page specs found in %s", PAGE_SPECS_DIR)
        return

    # Determine which pages to process
    if args.page:
        if args.page not in all_specs:
            logger.error("Page spec not found: %s", args.page)
            sys.exit(1)
        pages_to_run = [args.page]
    elif args.all:
        pages_to_run = list(all_specs.keys())
    else:
        try:
            changed = bundle.load_changed_pages()
        except FileNotFoundError:
            logger.warning("changed_pages.json not found — processing all pages")
            changed = list(all_specs.keys())
        pages_to_run = [p for p in changed if p in all_specs]
        if not pages_to_run:
            # Drift detection: compare a content fingerprint of the bundle
            # against the last successfully processed fingerprint.  If they
            # differ (or the ref file is missing), trigger a full rebuild.
            fingerprint = _bundle_fingerprint(bundle)
            last_ref = _read_last_ref()
            if fingerprint is None or fingerprint != last_ref:
                logger.info(
                    "Bundle content changed (%s -> %s) but changed_pages is empty — full rebuild",
                    (last_ref or "none")[:12],
                    (fingerprint or "unknown")[:12],
                )
                pages_to_run = list(all_specs.keys())
            else:
                logger.info("No matching pages in changed_pages.json. Nothing to do.")
                return

    generated = []
    errors = []

    for page_id in pages_to_run:
        spec = all_specs[page_id]
        try:
            output_path = process_page(spec, bundle, dry_run=args.dry_run)
            generated.append(output_path)
        except Exception as exc:
            logger.error("Failed to generate page %s: %s", page_id, exc)
            errors.append((page_id, str(exc)))

    # Record the bundle fingerprint on full success (not --page or --dry-run)
    # so future runs can detect content drift.
    if not errors and not args.dry_run and not args.page:
        fingerprint = _bundle_fingerprint(bundle)
        if fingerprint:
            _write_last_ref(fingerprint)
            logger.info("Updated last bundle ref: %s", fingerprint[:12])

    print(f"\nSummary: {len(generated)} page(s) generated, {len(errors)} error(s)")
    for path in generated:
        print(f"  ✓ {path}")
    for page_id, err in errors:
        print(f"  ✗ {page_id}: {err}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
