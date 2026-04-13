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
PLUGIN_DISPLAY_NAMES = {
    "config-backup": "Config Backup",
    "fastmail": "Fastmail",
    "github": "GitHub",
    "homeassistant": "Home Assistant",
    "ics-calendar": "ICS Calendar",
    "llmvision": "LLMVision",
    "opentable": "OpenTable",
    "opentable-heartbeat": "OpenTable Heartbeat",
    "outlook-calendar": "Outlook Calendar",
    "outlook-mail": "Outlook Mail",
    "outlook-work-calendar": "Outlook Work Calendar",
    "package-tracking": "Package Tracking",
    "spotify": "Spotify",
    "stock-quotes": "Stock Quotes",
    "usps-mail": "USPS Mail",
    "weightwatchers": "WeightWatchers",
}
PLUGIN_EMOJIS = {
    "config-backup": "🗄️",
    "fastmail": "📧",
    "github": "🐙",
    "homeassistant": "🏠",
    "ics-calendar": "🗓️",
    "llmvision": "🖼️",
    "opentable": "🍽️",
    "opentable-heartbeat": "🩺",
    "outlook-calendar": "📅",
    "outlook-mail": "📧",
    "outlook-work-calendar": "📅",
    "package-tracking": "📦",
    "spotify": "🎵",
    "stock-quotes": "📈",
    "usps-mail": "📬",
    "weightwatchers": "🍽️",
}
SERVICE_EMOJIS = {
    "fastmail-sse": "📡",
    "shared_mail_runtime": "🔄",
}
HOOK_EMOJIS = {
    "hass-hooks": "🪝",
}
SKILL_EMOJIS = {
    "home-music": "🎵",
}


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


def _plugin_id(plugin_json: dict, chunk_path: str) -> str:
    """Return the stable plugin identifier from bundle data or path."""
    plugin_id = plugin_json.get("plugin")
    if isinstance(plugin_id, str) and plugin_id.strip():
        return plugin_id.strip()
    return Path(chunk_path).stem


def _plugin_name(plugin_json: dict, chunk_path: str) -> str:
    """Return a human-friendly plugin name for public docs."""
    plugin_id = _plugin_id(plugin_json, chunk_path)
    explicit_name = plugin_json.get("name") or plugin_json.get("plugin_name")
    if isinstance(explicit_name, str) and explicit_name.strip():
        return explicit_name.strip()
    if plugin_id in PLUGIN_DISPLAY_NAMES:
        return PLUGIN_DISPLAY_NAMES[plugin_id]
    return plugin_id.replace("-", " ").title()


def _plugin_emoji(plugin_id: str) -> str:
    """Return a stable emoji for well-known plugins."""
    return PLUGIN_EMOJIS.get(plugin_id, "")


def _hook_id(hook_json: dict, chunk_path: str) -> str:
    """Return the stable hook identifier from bundle data or path."""
    hook_id = hook_json.get("agent") or hook_json.get("name")
    if isinstance(hook_id, str) and hook_id.strip():
        return hook_id.strip()
    return Path(chunk_path).stem


def _hook_name(hook_json: dict, chunk_path: str) -> str:
    """Return a human-friendly hook name for public docs."""
    hook_id = _hook_id(hook_json, chunk_path)
    explicit_name = hook_json.get("title")
    if isinstance(explicit_name, str) and explicit_name.strip():
        return explicit_name.strip()
    return hook_id.replace("-", " ").title()


def _hook_emoji(hook_id: str) -> str:
    """Return a stable emoji for hook pages."""
    return HOOK_EMOJIS.get(hook_id, "🪝")


def _skill_id(skill_json: dict, chunk_path: str) -> str:
    """Return the stable skill identifier from bundle data or path."""
    skill_id = skill_json.get("name")
    if isinstance(skill_id, str) and skill_id.strip():
        return skill_id.strip()
    return Path(chunk_path).stem


def _skill_name(skill_json: dict, chunk_path: str) -> str:
    """Return a human-friendly skill name for public docs."""
    skill_id = _skill_id(skill_json, chunk_path)
    explicit_title = skill_json.get("title")
    if isinstance(explicit_title, str) and explicit_title.strip():
        return explicit_title.strip()
    return skill_id.replace("-", " ").title()


def _stringify_param_type(param_type: object) -> str:
    """Render a schema type value as human-readable text."""
    if isinstance(param_type, list):
        return " | ".join(str(item) for item in param_type)
    if isinstance(param_type, str) and param_type:
        return param_type
    return "string"


def _markdown_cell(value: object) -> str:
    """Escape content for a markdown table cell."""
    text = "" if value is None else str(value)
    return " ".join(text.replace("|", "\\|").split())


def _parameter_description(meta: dict) -> str:
    """Build a concise parameter description from bundle metadata."""
    parts = []
    description = meta.get("description")
    if isinstance(description, str) and description.strip():
        base = description.strip()
        if base[-1] not in ".!?:":
            base += "."
        parts.append(base)
    enum_values = meta.get("enum")
    if isinstance(enum_values, list) and enum_values:
        allowed = ", ".join(f"`{value}`" for value in enum_values)
        parts.append(f"Allowed: {allowed}.")
    if "default" in meta:
        parts.append(f"Default: `{meta['default']}`.")
    return _markdown_cell(" ".join(parts))


def _extract_parameters(tool: dict) -> dict[str, dict]:
    """Return ordered tool parameters from bundle metadata or legacy schema."""
    params = tool.get("parameters")
    if isinstance(params, dict):
        return params

    schema = tool.get("input_schema") or tool.get("inputSchema")
    if not isinstance(schema, dict):
        return {}

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        return {}

    required_names = schema.get("required", [])
    required = set(required_names if isinstance(required_names, list) else [])
    ordered_names = [name for name in properties if name in required]
    ordered_names.extend(name for name in properties if name not in required)

    extracted = {}
    for name in ordered_names:
        raw_meta = properties.get(name, {})
        meta = raw_meta if isinstance(raw_meta, dict) else {}
        extracted[name] = {
            "type": meta.get("type", "string"),
            "required": name in required,
            "description": meta.get("description", ""),
        }
        if "enum" in meta:
            extracted[name]["enum"] = meta["enum"]
        if "default" in meta:
            extracted[name]["default"] = meta["default"]
    return extracted


def _render_parameter_table(parameters: dict[str, dict]) -> list[str]:
    """Render a markdown table for tool parameters."""
    lines = [
        "| Name | Type | Required | Description |",
        "|------|------|----------|-------------|",
    ]
    for name, meta in parameters.items():
        required = "Required" if meta.get("required") else "Optional"
        lines.append(
            "| "
            f"`{_markdown_cell(name)}` | "
            f"{_markdown_cell(_stringify_param_type(meta.get('type')))} | "
            f"{required} | "
            f"{_parameter_description(meta)} |"
        )
    return lines


def _render_plugin_page_content(plugin_json: dict, chunk_path: str) -> tuple[str, dict]:
    """Render a plugin child page deterministically from bundle JSON."""
    plugin_id = _plugin_id(plugin_json, chunk_path)
    plugin_name = _plugin_name(plugin_json, chunk_path)
    emoji = _plugin_emoji(plugin_id)
    summary = plugin_json.get("summary", "")
    summary = summary.strip() if isinstance(summary, str) else ""

    lines = [f"# {emoji} {plugin_name}" if emoji else f"# {plugin_name}"]
    if summary:
        lines.extend(["", summary])

    for tool in plugin_json.get("tools", []):
        tool_name = tool.get("name", "")
        if not isinstance(tool_name, str) or not tool_name.strip():
            continue

        description = tool.get("description", "")
        description = description.strip() if isinstance(description, str) else ""
        parameters = _extract_parameters(tool)

        lines.extend(["", f"### `{tool_name.strip()}`"])
        if description:
            lines.extend(["", description])
        if parameters:
            lines.extend(["", *_render_parameter_table(parameters)])

    return "\n".join(lines).strip() + "\n", {
        "id": plugin_id,
        "slug": plugin_id,
        "name": plugin_name,
        "emoji": emoji,
        "description": summary,
        "tool_count": _count_tools(plugin_json),
    }


def _render_hook_page_content(hook_json: dict, chunk_path: str) -> tuple[str, dict]:
    """Render a hook child page deterministically from bundle JSON."""
    hook_id = _hook_id(hook_json, chunk_path)
    hook_name = _hook_name(hook_json, chunk_path)
    emoji = _hook_emoji(hook_id)
    summary = _sentence_case_lead(hook_json.get("summary", ""))
    sections = hook_json.get("sections", {})

    lines = [f"# {emoji} {hook_name}" if emoji else f"# {hook_name}"]
    if summary:
        lines.extend(["", summary])

    for title, body in sections.items():
        lines.extend(["", *_render_markdown_section(title, body)])

    return "\n".join(lines).strip() + "\n", {
        "id": hook_id,
        "slug": hook_id,
        "name": hook_name,
        "emoji": emoji,
        "description": summary,
        "section_count": len(sections) if isinstance(sections, dict) else 0,
    }


def _format_required(required: bool) -> str:
    """Render a boolean required flag for tables."""
    return "Yes" if required else "No"


def _render_env_var_table(env_vars: list[dict]) -> list[str]:
    """Render environment variables as a markdown table."""
    if not env_vars:
        return ["_No environment variables required._"]

    lines = [
        "| Variable | Required | Description |",
        "|----------|----------|-------------|",
    ]
    for env_var in env_vars:
        lines.append(
            "| "
            f"`{_markdown_cell(env_var.get('name', ''))}` | "
            f"{_format_required(bool(env_var.get('required')))} | "
            f"{_markdown_cell(env_var.get('description', ''))} |"
        )
    return lines


def _render_markdown_section(title: str, body: str, level: int = 2) -> list[str]:
    """Render a markdown section using prebuilt markdown body text."""
    heading = "#" * level
    return [f"{heading} {title}", "", body.strip()]


def _sentence_case_lead(text: str) -> str:
    """Capitalize a leading lowercase summary without rewriting the rest."""
    if not isinstance(text, str) or not text:
        return ""
    if text[0].islower():
        return text[0].upper() + text[1:]
    return text


def _extract_skill_topics(content: str) -> list[str]:
    """Extract top-level section headings from a markdown skill body."""
    if not isinstance(content, str):
        return []

    topics = []
    for line in content.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            if heading:
                topics.append(heading)
    return topics


def _load_json_if_present(bundle: BundleLoader, relative_path: str) -> dict | None:
    """Load a JSON artifact if it exists in the bundle."""
    if not bundle.exists(relative_path):
        return None
    return bundle.load_json(relative_path)


def _process_agents_channels_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render the Agents & Channels page directly from config bundle data."""
    output_path = REPO_ROOT / page_spec["output_path"]
    config = bundle.load_json("config.json")
    config_agents = config.get("agents", [])
    agent_summaries = {
        agent.get("id", ""): agent
        for agent in bundle.load_json("agents.json").get("agents", [])
        if isinstance(agent, dict)
    }

    lines = [
        "# Agents & Channels",
        "",
        "This page lists the agent identities, model configuration, channel policies, and session settings exported in the public bundle.",
        "",
        "Private execution permissions, tool allowlists, and detailed channel-to-agent bindings are intentionally not included in the public bundle, so this page documents only the configuration that is published.",
        "",
        "## Models",
        "",
        f"- **Primary model:** `{config.get('models', {}).get('primary', 'unknown')}`",
    ]

    fallbacks = config.get("models", {}).get("fallbacks", [])
    if fallbacks:
        lines.append(
            f"- **Fallback models:** {', '.join(f'`{model}`' for model in fallbacks)}"
        )
    image_model = config.get("models", {}).get("imageModel", {})
    if isinstance(image_model, dict) and image_model.get("primary"):
        lines.append(f"- **Primary image model:** `{image_model['primary']}`")

    lines.extend(["", "## Agents", ""])
    lines.extend([
        "| Agent | ID | Public Summary |",
        "|-------|----|----------------|",
    ])
    for agent in config_agents:
        agent_id = agent.get("id", "")
        exported = agent_summaries.get(agent_id, {})
        detail = _load_json_if_present(bundle, f"agents/{agent_id}.json") or {}
        summary = exported.get("description") or detail.get("summary") or ""
        if summary in {"This folder is home. Treat it that way.", "On session start:"}:
            summary = ""
        lines.append(
            f"| {agent.get('emoji', '')} {agent.get('name', agent_id)} | "
            f"`{agent_id}` | "
            f"{_markdown_cell(summary or 'High-level role exported; private security details are omitted from the bundle.')} |"
        )

    for agent in config_agents:
        agent_id = agent.get("id", "")
        exported = agent_summaries.get(agent_id, {})
        detail = _load_json_if_present(bundle, f"agents/{agent_id}.json") or {}
        summary = exported.get("description") or detail.get("summary") or ""
        if summary in {"This folder is home. Treat it that way.", "On session start:"}:
            summary = ""
        section_names = list((detail.get("sections") or {}).keys())

        lines.extend([
            "",
            f"## {agent.get('emoji', '')} {agent.get('name', agent_id)}".strip(),
            "",
            f"- **Agent ID:** `{agent_id}`",
            f"- **Public summary:** {summary or 'Not explicitly exported in the public bundle.'}",
            "- **Security model:** Exec settings, permissions, and tool/plugin allowlists are not exported in the public bundle.",
            "- **Bindings:** Channel-to-agent binding details are not exported in the public bundle.",
        ])
        if section_names:
            lines.append(
                f"- **Published instruction sections:** {', '.join(f'`{name}`' for name in section_names)}"
            )

    lines.extend(["", "## Channels", ""])
    lines.extend([
        "| Channel | Enabled | DM Policy | Group Policy | Streaming |",
        "|---------|---------|-----------|--------------|-----------|",
    ])
    for channel in config.get("channels", []):
        lines.append(
            f"| `{channel.get('type', '')}` | "
            f"{_format_required(bool(channel.get('enabled')))} | "
            f"{_markdown_cell(channel.get('dmPolicy', ''))} | "
            f"{_markdown_cell(channel.get('groupPolicy', ''))} | "
            f"{_markdown_cell((channel.get('streaming') or {}).get('mode', ''))} |"
        )

    session = config.get("session", {})
    reset = session.get("reset", {}) if isinstance(session, dict) else {}
    lines.extend([
        "",
        "## Session Settings",
        "",
        "| Setting | Value |",
        "|---------|-------|",
        f"| Scope | `{_markdown_cell(session.get('scope', 'unknown'))}` |",
        f"| Reset mode | `{_markdown_cell(reset.get('mode', 'unknown'))}` |",
        f"| Reset hour | `{_markdown_cell(reset.get('atHour', 'unknown'))}` |",
    ])

    content = format_markdown("\n".join(lines))
    if dry_run:
        logger.info("[dry-run] Would generate page: %s", page_spec["id"])
        return page_spec["output_path"]
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written: %s", output_path)
    return page_spec["output_path"]


def _process_hooks_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render hook overview and child pages directly from structured bundle data."""
    page_id = page_spec["id"]
    output_path = REPO_ROOT / page_spec["output_path"]
    chunk_pattern = page_spec["chunk_source"]
    chunk_output_dir = page_spec.get("chunk_output_dir")
    parent_title = page_spec.get("front_matter", {}).get("title", "")

    logger.info("Processing bundle-rendered hooks page: %s -> %s", page_id, page_spec["output_path"])

    chunk_paths = sorted(bundle.glob(chunk_pattern))
    logger.info("Found %d hook chunks for pattern: %s", len(chunk_paths), chunk_pattern)

    if dry_run:
        logger.info("[dry-run] Would generate bundle-rendered page: %s (%d chunks)", page_id, len(chunk_paths))
        return page_spec["output_path"]

    child_dir = None
    if chunk_output_dir:
        child_dir = REPO_ROOT / chunk_output_dir
        child_dir.mkdir(parents=True, exist_ok=True)

    hook_entries = []
    for nav_index, chunk_path in enumerate(chunk_paths, start=1):
        hook_json = bundle.load_json(chunk_path)
        page_content, metadata = _render_hook_page_content(hook_json, chunk_path)
        hook_entries.append(metadata)

        if child_dir:
            child_front_matter = {
                "layout": "default",
                "title": metadata["name"],
                "parent": parent_title,
                "nav_order": nav_index,
            }
            child_path = child_dir / f"{metadata['id']}.md"
            write_page(child_path, format_markdown(page_content), front_matter=child_front_matter)
            logger.info("Written hook child page: %s", child_path)

    lines = [
        "# Hooks",
        "",
        "Hooks are event-driven entry points that react to real-world signals instead of running on a timer.",
        "",
        f"Octo currently publishes **{len(hook_entries)} hook{'s' if len(hook_entries) != 1 else ''}** in the public bundle.",
        "",
        "| | Hook | Description | Sections |",
        "|---|------|-------------|:--------:|",
    ]
    link_prefix = Path(chunk_output_dir).name if chunk_output_dir else "hooks"
    for entry in hook_entries:
        link = f"[{entry['name']}]({link_prefix}/{entry['slug']})"
        lines.append(
            f"| {entry.get('emoji') or '🪝'} | {link} | {entry.get('description') or ''} | {entry.get('section_count', 0)} |"
        )

    content = format_markdown("\n".join(lines))
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written hook index page: %s (%d hooks)", output_path, len(hook_entries))
    return page_spec["output_path"]


def _process_services_overview_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render the services overview page from service bundle artifacts."""
    output_path = REPO_ROOT / page_spec["output_path"]
    services = bundle.load_json("services.json").get("services", [])

    lines = [
        "# Services",
        "",
        "OpenClaw services are background processes that keep long-running automations and shared runtimes available between conversations.",
        "",
        "## Service Summary",
        "",
        "| Service | Description | Docs |",
        "|---------|-------------|------|",
    ]

    for service in services:
        service_id = service.get("id", "")
        link = f"[Read more →](services/{service_id})" if bundle.exists(f"services/{service_id}.json") else "—"
        lines.append(
            f"| {SERVICE_EMOJIS.get(service_id, '⚙️')} {service.get('name', service_id)} | "
            f"{_markdown_cell(service.get('description', ''))} | "
            f"{link} |"
        )

    for service in services:
        service_id = service.get("id", "")
        detail = _load_json_if_present(bundle, f"services/{service_id}.json") or {}
        features = detail.get("features", [])
        env_vars = detail.get("env_vars", [])
        lines.extend([
            "",
            f"## {SERVICE_EMOJIS.get(service_id, '⚙️')} {service.get('name', service_id)}",
            "",
            detail.get("summary") or service.get("description", ""),
        ])
        if features:
            lines.extend(["", "### Key Features", ""])
            lines.extend(f"- {feature}" for feature in features)
        lines.extend(["", "### Environment Variables", ""])
        lines.extend(_render_env_var_table(env_vars))
        if bundle.exists(f"services/{service_id}.json"):
            lines.extend(["", f"[Read more →](services/{service_id})"])

    content = format_markdown("\n".join(lines))
    if dry_run:
        logger.info("[dry-run] Would generate page: %s", page_spec["id"])
        return page_spec["output_path"]
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written: %s", output_path)
    return page_spec["output_path"]


def _process_service_detail_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render a service detail page from a single service JSON artifact."""
    output_path = REPO_ROOT / page_spec["output_path"]
    source_path = page_spec["sources"][0]["path"]
    service = bundle.load_json(source_path)

    lines = [
        f"# {service.get('name', page_spec.get('front_matter', {}).get('title', 'Service'))}",
        "",
        service.get("summary", ""),
    ]
    for section_title, body in (service.get("sections") or {}).items():
        lines.extend(["", *_render_markdown_section(section_title, body)])

    if source_path in {"services/shared_mail_runtime.json", "libs/mail_runtime_core.json"} and bundle.exists("libs/mail_action_usps-action.json"):
        lines.extend([
            "",
            "## Related Runtime Docs",
            "",
            "- [USPS Mail Runtime](shared-mail-runtime-usps)",
        ])

    content = format_markdown("\n".join(lines))
    content = content.replace("[`usps/README.md`](./usps/README.md)", "[USPS Mail Runtime](shared-mail-runtime-usps)")
    content = content.replace(
        "[`services/shared_mail_runtime/usps/README.md`](../shared_mail_runtime/usps/README.md)",
        "[USPS Mail Runtime](shared-mail-runtime-usps)",
    )
    content = content.replace("`services/shared_mail_runtime/README.md`", "[Shared Mail Runtime](shared_mail_runtime)")
    if dry_run:
        logger.info("[dry-run] Would generate page: %s", page_spec["id"])
        return page_spec["output_path"]
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written: %s", output_path)
    return page_spec["output_path"]


def _process_skills_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render skill overview and child pages directly from structured bundle data."""
    page_id = page_spec["id"]
    output_path = REPO_ROOT / page_spec["output_path"]
    chunk_pattern = page_spec["chunk_source"]
    chunk_output_dir = page_spec.get("chunk_output_dir")
    parent_title = page_spec.get("front_matter", {}).get("title", "")

    logger.info("Processing bundle-rendered skills page: %s -> %s", page_id, page_spec["output_path"])

    chunk_paths = sorted(bundle.glob(chunk_pattern))
    logger.info("Found %d skill chunks for pattern: %s", len(chunk_paths), chunk_pattern)

    if dry_run:
        logger.info("[dry-run] Would generate bundle-rendered page: %s (%d chunks)", page_id, len(chunk_paths))
        return page_spec["output_path"]

    child_dir = None
    if chunk_output_dir:
        child_dir = REPO_ROOT / chunk_output_dir
        child_dir.mkdir(parents=True, exist_ok=True)

    skill_entries = []
    for nav_index, chunk_path in enumerate(chunk_paths, start=1):
        skill_json = bundle.load_json(chunk_path)
        skill_id = _skill_id(skill_json, chunk_path)
        skill_name = _skill_name(skill_json, chunk_path)
        emoji = SKILL_EMOJIS.get(skill_id, "🧠")
        description = skill_json.get("description", "")
        description = description.strip() if isinstance(description, str) else ""
        agent = skill_json.get("agent", "unknown")
        topics = _extract_skill_topics(skill_json.get("content", ""))
        content = skill_json.get("content", "").strip()
        formatted = format_markdown(content if isinstance(content, str) and content.strip() else f"# {skill_name}\n")
        formatted = _replace_h1(formatted, emoji, skill_name)

        if child_dir:
            child_front_matter = {
                "layout": "default",
                "title": skill_name,
                "parent": parent_title,
                "nav_order": nav_index,
            }
            child_path = child_dir / f"{skill_id}.md"
            write_page(child_path, formatted, front_matter=child_front_matter)
            logger.info("Written skill child page: %s", child_path)

        skill_entries.append({
            "id": skill_id,
            "slug": skill_id,
            "name": skill_name,
            "emoji": emoji,
            "description": description,
            "agent": agent,
            "topics": topics,
        })

    lines = [
        "# Skills",
        "",
        "Skills are markdown-defined guidance modules that agents load for domain-specific rules, workflows, and operating context.",
        "",
        "Unlike plugins, skills do not execute code. They give agents shared instructions for how to use tools and interpret a problem domain.",
        "",
        f"Octo currently publishes **{len(skill_entries)} skill{'s' if len(skill_entries) != 1 else ''}** in the public bundle.",
        "",
        "| | Skill | Used by | Description |",
        "|---|-------|---------|-------------|",
    ]
    link_prefix = Path(chunk_output_dir).name if chunk_output_dir else "skills"
    for entry in skill_entries:
        link = f"[{entry['name']}]({link_prefix}/{entry['slug']})"
        lines.append(
            f"| {entry.get('emoji') or '🧠'} | {link} | `{_markdown_cell(entry.get('agent', 'unknown'))}` | {entry.get('description') or ''} |"
        )

    lines.extend([
        "",
        "## How Skills Differ from Plugins",
        "",
        "- **Skills** are bundled markdown knowledge for agents to read and follow.",
        "- **Plugins** are executable integrations that expose callable tools and APIs.",
        "- Skills can reference plugins, but they do not execute on their own.",
    ])

    content = format_markdown("\n".join(lines))
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written skills index page: %s (%d skills)", output_path, len(skill_entries))
    return page_spec["output_path"]


def _format_release_change(change: object) -> str:
    """Render a release change entry from structured or string data."""
    if isinstance(change, str):
        return change
    if isinstance(change, dict):
        title = (
            change.get("title")
            or change.get("summary")
            or change.get("description")
            or change.get("change")
        )
        category = change.get("category") or change.get("type")
        if title and category:
            return f"**{category}:** {title}"
        if title:
            return str(title)
    return _markdown_cell(change)


def _append_release_section(lines: list[str], title: str, items: object) -> None:
    """Append a release-notes subsection when items are present."""
    if not isinstance(items, list) or not items:
        return
    lines.extend(["", f"### {title}", ""])
    lines.extend(f"- {_format_release_change(item)}" for item in items)


def _format_job_schedule(schedule: dict) -> str:
    """Render a compact public schedule label from job bundle data."""
    kind = schedule.get("kind", "unknown")
    if kind == "cron":
        expr = schedule.get("expr", "unknown")
        tz = schedule.get("tz")
        return f"`{expr}`" + (f" ({tz})" if tz else "")
    if kind == "every":
        every_ms = schedule.get("everyMs")
        if isinstance(every_ms, int):
            hours = every_ms // 3_600_000
            if hours and every_ms % 3_600_000 == 0:
                unit = "hour" if hours == 1 else "hours"
                return f"Every {hours} {unit}"
            days = every_ms // 86_400_000
            if days and every_ms % 86_400_000 == 0:
                unit = "day" if days == 1 else "days"
                return f"Every {days} {unit}"
        return "Repeating interval"
    if kind == "at":
        return f"One-shot at `{schedule.get('at', schedule.get('atMs', 'unknown'))}`"
    return kind.title()


def _process_scheduled_tasks_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render the scheduled infrastructure tasks page from jobs.json."""
    output_path = REPO_ROOT / page_spec["output_path"]
    jobs = [
        job
        for job in bundle.load_json("jobs.json").get("jobs", [])
        if job.get("public", True) and job.get("category") == "infrastructure"
    ]

    lines = [
        "# Scheduled Tasks",
        "",
        "Scheduled tasks are background jobs that run without direct user input. The public bundle only includes infrastructure jobs that keep Octo healthy or maintained.",
        "",
        "Feature-specific reminders, briefs, personal nudges, and other user-facing automations are intentionally excluded from the public bundle and from this page.",
        "",
        f"Octo currently publishes **{len(jobs)} infrastructure task{'s' if len(jobs) != 1 else ''}**.",
        "",
        "## Infrastructure Tasks",
        "",
        "| Task | Schedule | What it does |",
        "|------|----------|--------------|",
    ]
    for job in jobs:
        lines.append(
            f"| `{job.get('name', '')}` | {_format_job_schedule(job.get('schedule', {}))} | "
            f"{_markdown_cell(job.get('summary') or job.get('description', ''))} |"
        )
    lines.append("")

    content = format_markdown("\n".join(lines))
    if dry_run:
        logger.info("[dry-run] Would generate page: %s", page_spec["id"])
        return page_spec["output_path"]
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written: %s", output_path)
    return page_spec["output_path"]


def _process_release_notes_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render release notes deterministically from release/changes.json."""
    output_path = REPO_ROOT / page_spec["output_path"]
    release = bundle.load_json("release/changes.json")
    changes = release.get("changes", [])

    lines = ["# Release Notes", ""]

    if changes:
        for change in changes:
            if isinstance(change, dict):
                version = change.get("version") or "Unknown release"
                date = change.get("date") or ""
                heading = f"## {version}"
                if date:
                    heading += f" ({date})"
                lines.extend([heading, ""])
                sections = change.get("sections")
                if isinstance(sections, dict) and sections:
                    for section_name, items in sections.items():
                        _append_release_section(lines, str(section_name), items)
                else:
                    summary = _format_release_change(change)
                    if summary:
                        lines.append(f"- {summary}")
                lines.append("")
            else:
                lines.append(f"- {_format_release_change(change)}")
    else:
        lines.append("No bundled changes were recorded for this release.")

    content = format_markdown("\n".join(lines))
    if dry_run:
        logger.info("[dry-run] Would generate page: %s", page_spec["id"])
        return page_spec["output_path"]
    write_page(output_path, content, front_matter=page_spec.get("front_matter"))
    logger.info("Written: %s", output_path)
    return page_spec["output_path"]


def _ensure_h1(content: str, emoji: str, name: str) -> str:
    """Ensure content starts with a proper H1 heading.

    If the first non-blank line is already an H1 (starts with ``# ``), return
    as-is.  Otherwise replace the first line (which is typically just the emoji
    + name as plain text) with a proper ``# emoji name`` heading.
    """
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.strip():
            if line.strip().startswith("# "):
                return content  # already has H1
            # Replace plain-text title line with proper H1
            heading = f"# {emoji} {name}" if emoji else f"# {name}"
            lines[i] = heading
            return "\n".join(lines)
    return content


def _replace_h1(content: str, emoji: str, name: str) -> str:
    """Replace the first H1 with a deterministic heading, or insert one if missing."""
    heading = f"# {emoji} {name}" if emoji else f"# {name}"
    lines = content.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            lines[i] = heading
            return "\n".join(lines)
        lines.insert(i, heading)
        lines.insert(i + 1, "")
        return "\n".join(lines)
    return heading + "\n"


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


def _process_plugin_bundle_page(
    page_spec: dict,
    bundle: BundleLoader,
    dry_run: bool = False,
) -> str:
    """Render plugin overview and child pages directly from structured bundle data."""
    page_id = page_spec["id"]
    output_path = REPO_ROOT / page_spec["output_path"]
    chunk_pattern = page_spec["chunk_source"]
    chunk_output_dir = page_spec.get("chunk_output_dir")
    parent_title = page_spec.get("front_matter", {}).get("title", "")

    logger.info("Processing bundle-rendered plugin page: %s -> %s", page_id, page_spec["output_path"])

    chunk_paths = sorted(bundle.glob(chunk_pattern))
    logger.info("Found %d plugin chunks for pattern: %s", len(chunk_paths), chunk_pattern)

    if dry_run:
        logger.info("[dry-run] Would generate bundle-rendered page: %s (%d chunks)", page_id, len(chunk_paths))
        return page_spec["output_path"]

    child_dir = None
    if chunk_output_dir:
        child_dir = REPO_ROOT / chunk_output_dir
        child_dir.mkdir(parents=True, exist_ok=True)

    plugin_entries = []
    for nav_index, chunk_path in enumerate(chunk_paths, start=1):
        plugin_json = bundle.load_json(chunk_path)
        page_content, metadata = _render_plugin_page_content(plugin_json, chunk_path)
        plugin_entries.append(metadata)

        if child_dir:
            child_front_matter = {
                "layout": "default",
                "title": metadata["name"],
                "parent": parent_title,
                "nav_order": nav_index,
            }
            child_path = child_dir / f"{metadata['id']}.md"
            write_page(child_path, format_markdown(page_content), front_matter=child_front_matter)
            logger.info("Written plugin child page: %s", child_path)

    link_prefix = Path(chunk_output_dir).name if chunk_output_dir else "plugins"
    index_content = _build_index_table(plugin_entries, link_prefix, title=parent_title)
    write_page(output_path, format_markdown(index_content), front_matter=page_spec.get("front_matter"))

    logger.info("Written plugin index page: %s (%d plugins)", output_path, len(plugin_entries))
    return page_spec["output_path"]


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

        # Ensure the content starts with a proper H1 heading (LLM sometimes omits #)
        formatted = _ensure_h1(formatted, emoji, plugin_name)

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
    strategy = page_spec.get("strategy")
    if strategy == "bundle-agents-channels":
        return _process_agents_channels_page(page_spec, bundle, dry_run)
    if strategy == "bundle-hooks":
        return _process_hooks_page(page_spec, bundle, dry_run)
    if strategy == "bundle-services":
        return _process_services_overview_page(page_spec, bundle, dry_run)
    if strategy == "bundle-service-detail":
        return _process_service_detail_page(page_spec, bundle, dry_run)
    if strategy == "bundle-scheduled-tasks":
        return _process_scheduled_tasks_page(page_spec, bundle, dry_run)
    if strategy == "bundle-skills":
        return _process_skills_page(page_spec, bundle, dry_run)
    if strategy == "bundle-release":
        return _process_release_notes_page(page_spec, bundle, dry_run)
    if page_spec.get("strategy") == "bundle-plugins":
        return _process_plugin_bundle_page(page_spec, bundle, dry_run)
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
