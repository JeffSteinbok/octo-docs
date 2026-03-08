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
import logging
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


def process_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Process a single page: select sources, build prompt, call LLM, write."""
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

    print(f"\nSummary: {len(generated)} page(s) generated, {len(errors)} error(s)")
    for path in generated:
        print(f"  ✓ {path}")
    for page_id, err in errors:
        print(f"  ✗ {page_id}: {err}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
