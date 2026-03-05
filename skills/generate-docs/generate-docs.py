#!/usr/bin/env python3
"""
generate-docs: Reads the private openclaw config repo and produces sanitized
high-level documentation for the public GitHub Pages site.
"""

import argparse
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml")
    raise SystemExit(1)


def parse_skill_md(path: Path) -> dict:
    """Parse a SKILL.md file, extracting YAML frontmatter and markdown body."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return {"meta": {}, "body": text}
    front = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    return {"meta": front, "body": body}


def discover_skills(config_repo: Path) -> list[dict]:
    """Find all skills across both the config repo and the hub skills dir."""
    skills = []
    seen = set()

    # Hub skills (openclaw-hub/skills/*)
    hub_skills = config_repo.parent / "openclaw-hub" / "skills"
    # Also check octo-docs/skills (this repo)
    local_skills = Path(__file__).resolve().parent.parent
    # Config repo may also reference skills
    config_skills = config_repo / "skills" if (config_repo / "skills").is_dir() else None

    for skills_dir in [hub_skills, local_skills, config_skills]:
        if skills_dir is None or not skills_dir.exists():
            continue
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            if skill_dir.name in seen or skill_dir.name == "generate-docs":
                continue
            seen.add(skill_dir.name)
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                parsed = parse_skill_md(skill_md)
                skills.append({
                    "name": parsed["meta"].get("name", skill_dir.name),
                    "description": parsed["meta"].get("description", ""),
                    "version": parsed["meta"].get("version", ""),
                    "emoji": parsed["meta"]
                        .get("metadata", {})
                        .get("openclaw", {})
                        .get("emoji", "🔧"),
                    "bins": parsed["meta"].get("requires", {}).get("bins", []),
                    "packages": parsed["meta"].get("requires", {}).get("packages", []),
                    "body": parsed["body"],
                })
    return skills


def sanitize_body(body: str) -> str:
    """Strip sensitive details from skill documentation body."""
    sanitized = body

    # Remove lines that look like they contain secrets/IDs
    patterns_to_redact = [
        r"(?i)(account[_ ]?id|identity[_ ]?id|mailbox[_ ]?id)\s*[:=]\s*`?[\w-]+`?",
        r"(?i)(token|secret|password|key)\s*[:=]\s*.*",
        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?\b",  # IP addresses
        r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",  # Emails
        r"\b\d{8,}\b",  # Long numeric IDs (Telegram, Discord)
        r"camera\.\w+",  # HA entity IDs
    ]

    for pattern in patterns_to_redact:
        sanitized = re.sub(pattern, "[redacted]", sanitized)

    return sanitized


def extract_commands_from_body(body: str) -> list[dict]:
    """Extract command documentation from a skill body."""
    commands = []
    current_cmd = None

    for line in body.split("\n"):
        # Match markdown headers that look like command names
        cmd_match = re.match(r"^#{1,4}\s+`?(\w+)`?\s*(?:[:—-]\s*(.*))?", line)
        if cmd_match and cmd_match.group(1).lower() not in (
            "usage", "options", "example", "examples", "notes",
            "limitations", "dependencies", "requirements", "workflow",
        ):
            if current_cmd:
                commands.append(current_cmd)
            current_cmd = {
                "name": cmd_match.group(1),
                "description": cmd_match.group(2) or "",
            }
        elif current_cmd and line.strip() and not line.startswith("#"):
            if not current_cmd["description"]:
                current_cmd["description"] = line.strip()

    if current_cmd:
        commands.append(current_cmd)

    return commands


def load_config(config_repo: Path) -> dict:
    """Load openclaw.json and extract high-level structure."""
    config_path = config_repo / "config" / "openclaw.json"
    if not config_path.exists():
        return {}
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def extract_agents(config: dict) -> list[dict]:
    """Extract agent names and roles (sanitized)."""
    agents = []
    agents_section = config.get("agents", {})

    # agents may be {"defaults": {...}, "list": [...]} or a plain list
    if isinstance(agents_section, dict):
        agent_list = agents_section.get("list", [])
    elif isinstance(agents_section, list):
        agent_list = agents_section
    else:
        agent_list = []

    for agent in agent_list:
        if not isinstance(agent, dict):
            continue
        identity = agent.get("identity", {})
        agents.append({
            "name": identity.get("name", agent.get("name", agent.get("id", "unknown"))),
            "description": agent.get("description", ""),
            "emoji": identity.get("emoji", "🤖"),
        })
    return agents


def extract_channels(config: dict) -> list[dict]:
    """Extract channel types (not IDs)."""
    channels = []
    channels_section = config.get("channels", {})

    if isinstance(channels_section, dict):
        for name, ch in channels_section.items():
            if isinstance(ch, dict):
                channels.append({
                    "type": name,
                    "enabled": ch.get("enabled", True),
                })
            else:
                channels.append({"type": name, "enabled": True})
    elif isinstance(channels_section, list):
        for ch in channels_section:
            if isinstance(ch, dict):
                channels.append({
                    "type": ch.get("type", ch.get("name", "unknown")),
                    "enabled": ch.get("enabled", True),
                })

    return channels


def discover_services(config_repo: Path) -> list[dict]:
    """Find services in the config repo and sibling repos."""
    services = []
    seen = set()

    search_dirs = [
        config_repo / "services",
        config_repo.parent / "openclaw-hub" / "services",
    ]

    for services_dir in search_dirs:
        if not services_dir.exists():
            continue
        for svc_dir in sorted(services_dir.iterdir()):
            if not svc_dir.is_dir() or svc_dir.name.startswith("."):
                continue
            if svc_dir.name in seen:
                continue
            seen.add(svc_dir.name)

            svc = {"name": svc_dir.name, "description": "", "type": "daemon"}

            service_files = list(svc_dir.glob("*.service"))
            if service_files:
                svc["type"] = "systemd"

            for doc_name in ["SKILL.md", "README.md"]:
                doc_path = svc_dir / doc_name
                if doc_path.exists():
                    parsed = parse_skill_md(doc_path)
                    svc["description"] = parsed["meta"].get("description", "")
                    if not svc["description"]:
                        for line in parsed["body"].split("\n"):
                            if line.strip() and not line.startswith("#"):
                                svc["description"] = line.strip()
                                break
                    break

            if not svc["description"]:
                for py_file in svc_dir.glob("*.py"):
                    text = py_file.read_text(encoding="utf-8", errors="ignore")
                    doc_match = re.search(r'"""(.*?)"""', text, re.DOTALL)
                    if doc_match:
                        svc["description"] = doc_match.group(1).strip().split("\n")[0]
                        break

            services.append(svc)
    return services


# ---------------------------------------------------------------------------
# Markdown generators
# ---------------------------------------------------------------------------

def generate_index(skills: list, services: list, agents: list, channels: list) -> str:
    channel_list = ", ".join(
        ch["type"].title() for ch in channels if ch.get("enabled", True)
    ) or "None configured"

    lines = [
        "---",
        "layout: default",
        "title: Home",
        "---",
        "",
        "# 🐙 OpenClaw Hub",
        "",
        "OpenClaw is a modular AI assistant framework that connects language models to",
        "real-world services through **skills**, **agents**, and **channels**.",
        "",
        "## 📊 At a Glance",
        "",
        "| | Count |",
        "|---|---|",
        f"| 🔧 Skills | {len(skills)} |",
        f"| ⚙️ Services | {len(services)} |",
        f"| 🤖 Agents | {len(agents)} |",
        f"| 📡 Channels | {channel_list} |",
        "",
        "## 🧠 How It Works",
        "",
        "🤖 **Agents** are personas powered by language models. Each agent has its own",
        "identity, personality, and set of permitted tools. Agents communicate with",
        "users through **channels** — messaging platforms like Telegram or Discord.",
        "",
        "🔧 **Skills** are self-contained capabilities that agents can invoke: sending",
        "email, checking restaurant availability, snapping a security camera, and more.",
        "Each skill declares its own dependencies and is independently versioned.",
        "",
        "⚙️ **Services** are long-running background daemons that watch for events (like",
        "incoming email) and route notifications through the system.",
        "",
        "## 📚 Learn More",
        "",
        "- [🔧 Skills](skills.html) — what the system can do",
        "- [⚙️ Services](services.html) — background event processing",
        "- [🏗️ Architecture](architecture.html) — how the pieces fit together",
    ]

    return "\n".join(lines)


def extract_capability_summary(body: str) -> str:
    """Extract a brief capability summary from the skill body, sanitized."""
    capabilities = []
    for line in body.split("\n"):
        line = line.strip()
        # Skip code blocks, headers, empty lines, setup instructions
        if (not line or line.startswith("#") or line.startswith("```")
                or line.startswith("|") or line.startswith("---")):
            continue
        # Skip lines that are clearly setup/config instructions
        lower = line.lower()
        if any(kw in lower for kw in [
            "install", "pip ", "bash", "python3 skills/", "configuration.yaml",
            "env var", "token", "export ", "allowlist", "/home/", "~/"
        ]):
            continue
        capabilities.append(line)
        if len(capabilities) >= 3:
            break
    return sanitize_body(" ".join(capabilities))


def generate_skills_page(skills: list) -> str:
    lines = [
        "---",
        "layout: default",
        "title: Skills",
        "---",
        "",
        "# Skills",
        "",
        "Skills are modular capabilities that agents can use. Each skill is a",
        "self-contained package with its own metadata, dependencies, and commands.",
        "",
    ]

    # Human-readable skill summaries keyed by skill name
    skill_overviews = {
        "fastmail-send": {
            "what": "Send emails and calendar meeting invitations via Fastmail JMAP.",
            "capabilities": [
                "Compose and send plain-text emails with optional CC and attachments",
                "Create meeting requests with accept/decline buttons (iCalendar)",
                "Configurable signature and sender identity",
            ],
        },
        "hass-camera-snapshot": {
            "what": "Capture snapshots from home security cameras via Home Assistant.",
            "capabilities": [
                "Snap any individual camera or all cameras at once",
                "Automatically downloads and timestamps images locally",
                "Pre-flight checks with actionable error messages",
            ],
        },
        "opentable": {
            "what": "Check real-time restaurant availability on OpenTable.",
            "capabilities": [
                "Look up restaurant IDs from OpenTable URL slugs",
                "Query available reservation slots by date, party size, and time",
                "Returns direct booking links for available times",
            ],
        },
    }

    for skill in skills:
        emoji = skill.get("emoji", "🔧")
        lines.append(f"## {emoji} {skill['name']}")
        lines.append("")

        overview = skill_overviews.get(skill["name"])
        if overview:
            lines.append(overview["what"])
            lines.append("")
            lines.append("**Capabilities:**")
            lines.append("")
            for cap in overview["capabilities"]:
                lines.append(f"- {cap}")
            lines.append("")
        elif skill["description"]:
            desc = sanitize_body(skill["description"].strip())
            lines.append(desc)
            lines.append("")

        # Dependencies
        deps = []
        if skill.get("bins"):
            deps.extend(skill["bins"])
        if skill.get("packages"):
            deps.extend(skill["packages"])
        if deps:
            lines.append(f"**Dependencies:** {', '.join(deps)}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_services_page(services: list) -> str:
    lines = [
        "---",
        "layout: default",
        "title: Services",
        "---",
        "",
        "# Services",
        "",
        "Services are long-running background processes that watch for events",
        "and route notifications through the OpenClaw system.",
        "",
    ]

    # Map service names to human-friendly descriptions
    service_descriptions = {
        "fastmail-sse": (
            "Monitors an email inbox in real time using Server-Sent Events (SSE). "
            "When new mail arrives, it formats a notification and delivers it to "
            "the configured messaging channel. Automated and marketing emails are "
            "filtered out. Calendar RSVP responses are detected and displayed with "
            "appropriate status indicators."
        ),
    }

    for svc in services:
        lines.append(f"## ⚙️ {svc['name']}")
        lines.append("")

        desc = service_descriptions.get(svc["name"], svc.get("description", ""))
        if desc:
            lines.append(sanitize_body(desc))
            lines.append("")

        if svc.get("type") == "systemd":
            lines.append("**Deployment:** systemd user service (auto-restart on failure)")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_architecture_page(
    skills: list, services: list, agents: list, channels: list
) -> str:
    # Agent descriptions by known IDs
    agent_descriptions = {
        "Octo": "Primary personal assistant — full access to all skills and tools",
        "family-agent": "Family group chat agent with limited permissions",
        "group-agent": "Generic group chat agent — responds only when mentioned",
        "mail-agent": "Email processing agent with read-only access",
    }

    agent_rows = ""
    for a in agents:
        emoji = a.get("emoji", "🤖")
        name = a["name"]
        desc = a.get("description") or agent_descriptions.get(name, "")
        agent_rows += f"| {emoji} {name} | {desc} |\n"

    channel_rows = ""
    for ch in channels:
        status = "✅ Enabled" if ch.get("enabled", True) else "❌ Disabled"
        channel_rows += f"| {ch['type'].title()} | {status} |\n"

    skill_names = ", ".join(s["name"] for s in skills)

    lines = [
        "---",
        "layout: default",
        "title: Architecture",
        "---",
        "",
        "# Architecture",
        "",
        "OpenClaw follows a modular, event-driven architecture where agents, skills,",
        "channels, and services each play a distinct role.",
        "",
        "## Components",
        "",
        "```",
        "┌─────────────┐     ┌──────────────┐     ┌────────────┐",
        "│   Channels   │◄───►│    Agents     │◄───►│   Skills   │",
        "│  (Telegram,  │     │  (LLM-backed  │     │ (email,    │",
        "│   Discord)   │     │   personas)   │     │  cameras,  │",
        "└─────────────┘     └──────┬───────┘     │  dining)   │",
        "                           │              └────────────┘",
        "                    ┌──────▼───────┐",
        "                    │   Services    │",
        "                    │  (event       │",
        "                    │   watchers)   │",
        "                    └──────────────┘",
        "```",
        "",
        "## Agents",
        "",
        "Agents are LLM-powered personas, each with their own identity, permissions,",
        "and context. They decide which skills to invoke based on user requests.",
        "",
        "| Agent | Role |",
        "|-------|------|",
        agent_rows,
        "## Channels",
        "",
        "Channels are the messaging platforms through which users interact with agents.",
        "",
        "| Platform | Status |",
        "|----------|--------|",
        channel_rows,
        "## Skills",
        "",
        f"Skills are the system's capabilities: **{skill_names}**.",
        "Each is a self-contained module with declared dependencies, invoked by agents",
        "as needed. See the [Skills](skills.html) page for details.",
        "",
        "## Services",
        "",
        "Services run continuously in the background, watching for events (new email,",
        "calendar updates) and routing them as notifications through the messaging",
        "channels. See the [Services](services.html) page for details.",
        "",
        "## Design Principles",
        "",
        "- **Modular:** Each skill and service is independently versioned and deployed",
        "- **Secure:** Secrets stay in environment variables; public docs are auto-sanitized",
        "- **Observable:** Services log to journald; agents maintain conversation history",
        "- **Extensible:** New skills are added by dropping a folder with a `SKILL.md`",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate sanitized docs from private openclaw config"
    )
    parser.add_argument(
        "--config-repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent.parent / "openclaw",
        help="Path to the private openclaw config repo",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "docs",
        help="Path to the Jekyll site root (repo root)",
    )
    args = parser.parse_args()

    config_repo = args.config_repo.resolve()
    output_dir = args.output_dir.resolve()

    if not config_repo.exists():
        print(f"Error: Config repo not found at {config_repo}")
        raise SystemExit(1)

    print(f"Reading config from: {config_repo}")
    print(f"Writing docs to:     {output_dir}")

    # Gather data
    skills = discover_skills(config_repo)
    services = discover_services(config_repo)
    config = load_config(config_repo)
    agents = extract_agents(config)
    channels = extract_channels(config)

    print(f"Found {len(skills)} skills, {len(services)} services, "
          f"{len(agents)} agents, {len(channels)} channels")

    # Generate pages
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.md": generate_index(skills, services, agents, channels),
        "skills.md": generate_skills_page(skills),
        "services.md": generate_services_page(services),
        "architecture.md": generate_architecture_page(
            skills, services, agents, channels
        ),
    }

    for filename, content in pages.items():
        out_path = output_dir / filename
        out_path.write_text(content, encoding="utf-8")
        print(f"  Wrote {out_path}")

    print("\nDone! Preview locally with: cd docs && bundle exec jekyll serve")


if __name__ == "__main__":
    main()
