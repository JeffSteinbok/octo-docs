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


def _extract_heading_emoji(markdown: str) -> str:
    """Extract the leading emoji from the first heading or first non-blank line."""
    # Try H1/H2 heading first
    match = re.search(r'^#{1,2}\s+(\S+)\s+', markdown, re.MULTILINE)
    if match and not match.group(1).isascii():
        return match.group(1)
    # Fall back: first non-blank line may start with an emoji (LLM sometimes omits #)
    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped:
            token = stripped.split()[0] if stripped.split() else ""
            if token and not token.isascii():
                return token
            break
    return ""


def _extract_first_paragraph(markdown: str) -> str:
    """Extract the first paragraph after the heading (for use as description)."""
    lines = markdown.strip().split("\n")
    # Skip heading line(s) and blank lines
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if line.startswith("#") or not line:
            idx += 1
            continue
        # First non-heading, non-blank line — check if it's the title line (emoji prefix)
        if not line[0].isascii():
            idx += 1
            # Skip blank lines after emoji title
            while idx < len(lines) and not lines[idx].strip():
                idx += 1
            break
        break
    # Collect paragraph lines until next blank line or heading
    para = []
    while idx < len(lines):
        line = lines[idx].strip()
        if not line or line.startswith("#"):
            break
        para.append(line)
        idx += 1
    return " ".join(para)


def _count_tools(plugin_json: dict) -> int:
    """Count tools defined in a plugin JSON structure."""
    tools = plugin_json.get("tools")
    if isinstance(tools, (list, dict)):
        return len(tools)
    functions = plugin_json.get("functions")
    if isinstance(functions, (list, dict)):
        return len(functions)
    return 0


def _build_index_table(entries: list, link_prefix: str = "plugins",
                       title: str = "Plugins") -> str:
    """Build a markdown index page with title, intro text and summary table."""
    total_tools = sum(e.get("tool_count", 0) for e in entries)
    intro = (
        f"# {title}\n"
        "\n"
        "Plugins are self-contained capabilities that Octo's agents can invoke — "
        "sending email, checking restaurant availability, controlling smart home "
        "devices, tracking packages, and more. Each plugin is independently "
        "developed and declares its own tools, parameters, and dependencies.\n"
        "\n"
        "Unlike [skills](skills), which provide knowledge through markdown prompts, "
        "plugins execute real code and interact with external APIs. Think of plugins "
        "as _tools_ and skills as _knowledge_.\n"
        "\n"
        f"Octo currently has **{len(entries)} plugins** providing **{total_tools} tools** in total.\n"
    )
    table_lines = [
        "| | Plugin | Description | Tools |",
        "|---|--------|-------------|:-----:|",
    ]
    for e in entries:
        emoji = e.get("emoji") or ""
        link = f"[{e['name']}]({link_prefix}/{e['slug']})"
        desc = e.get("description") or ""
        count = e.get("tool_count", 0)
        table_lines.append(f"| {emoji} | {link} | {desc} | {count} |")
    return intro + "\n" + "\n".join(table_lines)


def _process_chunked_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Generate separate child pages for each chunk source, plus an index page.

    Each glob-expanded source is sent to the LLM individually and written as its
    own page under ``chunk_output_dir``.  The main ``output_path`` becomes an
    index page with a summary table linking to the children.
    """
    page_id = page_spec["id"]
    output_path = REPO_ROOT / page_spec["output_path"]
    chunk_pattern = page_spec["chunk_source"]
    chunk_output_dir = page_spec.get("chunk_output_dir")
    instructions = page_spec.get("instructions", {})
    parent_title = page_spec.get("front_matter", {}).get("title", "")

    logger.info("Processing chunked page: %s -> %s", page_id, page_spec["output_path"])

    chunk_paths = sorted(bundle.glob(chunk_pattern))
    logger.info("Found %d chunks for pattern: %s", len(chunk_paths), chunk_pattern)

    if dry_run:
        logger.info("[dry-run] Would generate chunked page: %s (%d chunks)", page_id, len(chunk_paths))
        return page_spec["output_path"]

    if chunk_output_dir:
        child_dir = REPO_ROOT / chunk_output_dir
        child_dir.mkdir(parents=True, exist_ok=True)

    # Generate each chunk as a separate page
    plugin_entries = []
    for nav_index, chunk_path in enumerate(chunk_paths, start=1):
        # Extract metadata from plugin JSON
        try:
            plugin_json = bundle.load_json(chunk_path)
            plugin_name = (
                plugin_json.get("name")
                or plugin_json.get("plugin_name")
                or Path(chunk_path).stem.replace("-", " ").title()
            )
            plugin_desc = plugin_json.get("description", "")
            tool_count = _count_tools(plugin_json)
        except Exception:
            plugin_name = Path(chunk_path).stem.replace("-", " ").title()
            plugin_desc = ""
            tool_count = 0

        slug = _slugify(plugin_name)

        chunk_spec = {
            "id": page_id,
            "output_path": page_spec["output_path"],
            "template": "chunk_section",
            "sources": [{"path": chunk_path}],
            "instructions": {
                "audience": instructions.get("audience", "developers"),
                "include": [
                    f"Generate a standalone documentation page for the '{plugin_name}' plugin",
                    "Use a fitting emoji in the H1 heading",
                    "List every tool as an H3 heading with the tool name",
                    "Under each tool H3, include the tool's description and a "
                    "parameter table (name, type, description) if available",
                ],
                "exclude": instructions.get("exclude", []),
            },
        }
        selected = build_source_material(bundle, chunk_spec)
        prompt = build_prompt(chunk_spec, selected)
        content = generate_page(prompt)

        emoji = _extract_heading_emoji(content)
        # Prefer LLM-generated description over JSON metadata
        llm_desc = _extract_first_paragraph(content)
        formatted = format_markdown(content)

        # Write individual child page
        if chunk_output_dir:
            child_front_matter = {
                "layout": "default",
                "title": plugin_name,
                "parent": parent_title,
                "nav_order": nav_index,
            }
            child_path = child_dir / f"{slug}.md"
            write_page(child_path, formatted, front_matter=child_front_matter)
            logger.info("Written child page: %s", child_path)

        plugin_entries.append({
            "name": plugin_name,
            "slug": slug,
            "description": llm_desc or plugin_desc,
            "emoji": emoji,
            "tool_count": tool_count,
        })
        logger.info("Generated chunk: %s (%s)", chunk_path, plugin_name)

    # Build and write the index page with summary table
    link_prefix = Path(chunk_output_dir).name if chunk_output_dir else "plugins"
    index_content = _build_index_table(plugin_entries, link_prefix, title=parent_title)
    formatted_index = format_markdown(index_content)
    write_page(output_path, formatted_index, front_matter=page_spec.get("front_matter"))

    logger.info("Written index page: %s (%d plugins)", output_path, len(plugin_entries))
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
