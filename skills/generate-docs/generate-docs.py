#!/usr/bin/env python3
"""
generate-docs: Reads the ~/.openclaw runtime config directory and produces
sanitized high-level documentation for the public GitHub Pages site.
Skills symlinked from openclaw-hub get source links in the generated docs.
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


def resolve_hub_source(skill_dir: Path) -> str | None:
    """If skill_dir is a symlink whose target lives inside openclaw-hub, return
    a GitHub URL to the source directory.  Otherwise return None."""
    if not skill_dir.is_symlink():
        return None
    target = skill_dir.resolve()
    # Walk up the resolved path looking for an openclaw-hub git repo
    for parent in [target, *target.parents]:
        if (parent / ".git").exists():
            try:
                remote_url = (
                    (parent / ".git" / "config").read_text(encoding="utf-8")
                )
                if "openclaw-hub" not in remote_url:
                    break
                # Extract owner/repo from the remote URL
                match = re.search(
                    r"github\.com[:/](.+?/openclaw-hub?)(?:\.git)?", remote_url
                )
                if match:
                    repo_slug = match.group(1)
                    rel = target.relative_to(parent)
                    return f"https://github.com/{repo_slug}/tree/main/{rel}"
            except (OSError, ValueError):
                pass
            break
    return None


def discover_skills(config_dir: Path) -> list[dict]:
    """Find all skills across agent workspaces in the .openclaw directory."""
    skills = []
    seen = set()

    # Primary skill source: main agent workspace skills
    agents_dir = config_dir / "agents"
    skill_search_dirs: list[Path] = []

    if agents_dir.is_dir():
        for agent_dir in sorted(agents_dir.iterdir()):
            ws = agent_dir / "workspace" / "skills"
            if ws.is_dir():
                skill_search_dirs.append(ws)

    # Also check octo-docs/skills (this repo)
    local_skills = Path(__file__).resolve().parent.parent
    skill_search_dirs.append(local_skills)

    for skills_dir in skill_search_dirs:
        if not skills_dir.exists():
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
                    "source_url": resolve_hub_source(skill_dir),
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


def load_config(config_dir: Path) -> dict:
    """Load openclaw.json from the .openclaw directory."""
    for candidate in [config_dir / "openclaw.json", config_dir / "config" / "openclaw.json"]:
        if candidate.exists():
            with open(candidate, encoding="utf-8") as f:
                return json.load(f)
    return {}


def load_jobs(config_dir: Path) -> list[dict]:
    """Load scheduled jobs from cron/jobs.json (sanitized)."""
    # Check both the runtime dir and the config repo (via workspace symlink)
    candidates = [config_dir / "cron" / "jobs.json"]
    ws = config_dir / "agents" / "main" / "workspace"
    if ws.is_symlink() or ws.is_dir():
        repo_root = ws.resolve().parent.parent
        candidates.append(repo_root / "config" / "jobs.json")

    data = {}
    for jobs_path in candidates:
        if jobs_path.exists():
            with open(jobs_path, encoding="utf-8") as f:
                data = json.load(f)
            break
    if not data:
        return []

    jobs = []
    for job in data.get("jobs", []):
        schedule_info = job.get("schedule", {})
        every_ms = schedule_info.get("everyMs", 0)
        if every_ms >= 86400000:
            interval = f"Every {every_ms // 86400000}d"
        elif every_ms >= 3600000:
            interval = f"Every {every_ms // 3600000}h"
        elif every_ms >= 60000:
            interval = f"Every {every_ms // 60000}m"
        else:
            interval = schedule_info.get("kind", "unknown")
        jobs.append({
            "name": job.get("name", job.get("id", "unknown")),
            "description": job.get("description", ""),
            "enabled": job.get("enabled", True),
            "interval": interval,
        })
    return jobs


def load_repo_readme(config_dir: Path) -> str:
    """Load README.md from the openclaw config repo (via workspace symlink)."""
    ws = config_dir / "agents" / "main" / "workspace"
    if ws.is_symlink() or ws.is_dir():
        repo_root = ws.resolve().parent.parent
        readme = repo_root / "README.md"
        if readme.exists():
            return readme.read_text(encoding="utf-8", errors="ignore")
    return ""


def extract_agents(config: dict, config_dir: Path) -> list[dict]:
    """Extract agent names, roles, and active status (sanitized)."""
    agents = []
    agents_section = config.get("agents", {})

    # agents may be {"defaults": {...}, "list": [...]} or a plain list
    if isinstance(agents_section, dict):
        agent_list = agents_section.get("list", [])
    elif isinstance(agents_section, list):
        agent_list = agents_section
    else:
        agent_list = []

    # Check bindings to determine which agents are actually routed to
    bound_agents = set()
    for binding in config.get("bindings", []):
        if isinstance(binding, dict) and binding.get("agentId"):
            bound_agents.add(binding["agentId"])

    for agent in agent_list:
        if not isinstance(agent, dict):
            continue
        identity = agent.get("identity", {})
        agent_id = agent.get("id", "unknown")

        # Check if agent workspace has a completed IDENTITY.md (not template)
        active = agent_id in bound_agents
        ws = config_dir / "agents" / agent_id / "workspace"
        if not ws.exists():
            ws = Path(agent.get("workspace", ""))
        id_file = ws / "IDENTITY.md" if ws.exists() else None
        if id_file and id_file.exists():
            text = id_file.read_text(encoding="utf-8", errors="ignore")
            if "_(pick something you like)_" in text:
                active = False

        # Use the agent ID as the display name (e.g. "main", "family-agent")
        display_name = agent_id

        agents.append({
            "id": agent_id,
            "name": display_name,
            "description": agent.get("description", ""),
            "emoji": identity.get("emoji", "🤖"),
            "active": active,
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


def discover_services(config_dir: Path) -> list[dict]:
    """Find services in the .openclaw directory and linked repos."""
    services = []
    seen = set()

    search_dirs: list[Path] = []

    # Direct services dir in .openclaw
    if (config_dir / "services").is_dir():
        search_dirs.append(config_dir / "services")

    # Follow the main agent workspace symlink to find the config repo's services
    ws = config_dir / "agents" / "main" / "workspace"
    if ws.is_symlink() or ws.is_dir():
        repo_root = ws.resolve().parent.parent  # e.g. ~/git/openclaw
        if (repo_root / "services").is_dir():
            search_dirs.append(repo_root / "services")
        # Also check sibling openclaw-hub repo
        hub_services = repo_root.parent / "openclaw-hub" / "services"
        if hub_services.is_dir():
            search_dirs.append(hub_services)

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

def generate_index(skills: list, services: list, agents: list, channels: list,
                   jobs: list | None = None) -> str:
    jobs = jobs or []
    channel_list = ", ".join(
        ch["type"].title() for ch in channels if ch.get("enabled", True)
    ) or "None configured"

    lines = [
        "---",
        "layout: default",
        "title: Home",
        "nav_order: 1",
        "---",
        "",
        "# 🐙 Octo Docs",
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
        f"| ⏰ Scheduled Jobs | {len(jobs)} |",
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
        "⏰ **Scheduled Jobs** run automatically on a timer — fetching calendars,",
        "backing up config, and other recurring tasks without user intervention.",
        "",
        "## 📚 Learn More",
        "",
        "- [🔧 Skills](skills.html) — what the system can do",
        "- [⚙️ Services](services.html) — background event processing",
        "- [⏰ Scheduled Jobs](jobs.html) — automated recurring tasks",
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
        "nav_order: 2",
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
        "homeassistant-cli": {
            "what": "Advanced Home Assistant control using the official hass-cli tool.",
            "capabilities": [
                "Control lights, switches, climate, locks, and alarm systems",
                "Query entity states, history, and event logs",
                "Auto-completion and rich output formatting",
            ],
        },
        "config-backup": {
            "what": "Backup OpenClaw config to Git with automatic change detection.",
            "capabilities": [
                "Detects changes to openclaw.json and commits only when needed",
                "Designed for cron — runs silently unless something goes wrong",
                "Supports forced commits for manual snapshots",
            ],
        },
        "outlook-work-calendar": {
            "what": "Fetch work calendar events from a published Outlook endpoint.",
            "capabilities": [
                "Query events by date range with subject, time, and location",
                "Shows busy status and sensitivity level for scheduling",
                "No authentication required — uses published calendar feed",
            ],
        },
        "personal-calendars": {
            "what": "Fetch personal and family calendars from Outlook Live ICS feeds.",
            "capabilities": [
                "Query personal, family, or all calendars by date range",
                "Returns events with subject, time, and location",
                "Supports multiple calendar sources in a single query",
            ],
        },
    }

    for skill in skills:
        emoji = skill.get("emoji", "🔧")
        lines.append(f"## {emoji} {skill['name']}")
        lines.append("")

        source_url = skill.get("source_url")
        if source_url:
            lines.append(f"📦 [Source on GitHub]({source_url})")
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
        "nav_order: 3",
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
        "main": "Primary personal assistant — full access to all skills and tools",
        "family-agent": "Family group chat agent with limited permissions",
        "group-agent": "Generic group chat agent — responds only when mentioned",
        "mail-agent": "Email processing agent with read-only access",
    }

    agent_rows = ""
    for a in agents:
        emoji = a.get("emoji", "🤖")
        agent_id = a.get("id", a["name"])
        name = a["name"]
        desc = a.get("description") or agent_descriptions.get(agent_id, "")
        status = "✅ Active" if a.get("active") else "💤 Inactive"
        agent_rows += f"| {emoji} {name} | {desc} | {status} |\n"

    channel_rows = ""
    for ch in channels:
        status = "✅ Enabled" if ch.get("enabled", True) else "❌ Disabled"
        channel_rows += f"| {ch['type'].title()} | {status} |\n"

    skill_names = ", ".join(s["name"] for s in skills)

    lines = [
        "---",
        "layout: default",
        "title: Architecture",
        "nav_order: 5",
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
        "| Agent | Role | Status |",
        "|-------|------|--------|",
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


def generate_jobs_page(jobs: list) -> str:
    lines = [
        "---",
        "layout: default",
        "title: Scheduled Jobs",
        "nav_order: 4",
        "---",
        "",
        "# Scheduled Jobs",
        "",
        "Cron-style jobs that run automatically on a schedule. Each job spawns an",
        "isolated agent session, executes its task, and exits — no user interaction",
        "required.",
        "",
    ]

    if not jobs:
        lines.append("_No scheduled jobs configured._")
        lines.append("")
        return "\n".join(lines)

    lines.extend([
        "| Job | Description | Schedule | Status |",
        "|-----|-------------|----------|--------|",
    ])

    for job in jobs:
        status = "✅ Enabled" if job.get("enabled") else "❌ Disabled"
        lines.append(
            f"| **{job['name']}** | {job['description']} "
            f"| {job['interval']} | {status} |"
        )

    lines.append("")
    lines.extend([
        "## How It Works",
        "",
        "Jobs are defined in `cron/jobs.json` inside the `.openclaw` directory.",
        "The OpenClaw gateway reads this file and fires each job on its configured",
        "schedule. Jobs run in isolated sessions so they don't pollute the main",
        "conversation history.",
        "",
        "Agents can create, edit, and delete jobs at runtime — for example,",
        '`"remind me in 20 minutes"` creates a one-shot cron job that delivers',
        "a message back through the active channel.",
    ])

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Generate sanitized docs from the .openclaw config directory"
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path.home() / ".openclaw",
        help="Path to the .openclaw runtime config directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "docs",
        help="Path to the Jekyll site root (repo root)",
    )
    args = parser.parse_args()

    config_dir = args.config_dir.resolve()
    output_dir = args.output_dir.resolve()

    if not config_dir.exists():
        print(f"Error: Config directory not found at {config_dir}")
        raise SystemExit(1)

    print(f"Reading config from: {config_dir}")
    print(f"Writing docs to:     {output_dir}")

    # Gather data
    skills = discover_skills(config_dir)
    services = discover_services(config_dir)
    config = load_config(config_dir)
    agents = extract_agents(config, config_dir)
    channels = extract_channels(config)
    jobs = load_jobs(config_dir)

    print(f"Found {len(skills)} skills, {len(services)} services, "
          f"{len(agents)} agents, {len(channels)} channels, {len(jobs)} jobs")

    # Generate pages
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.md": generate_index(skills, services, agents, channels, jobs),
        "skills.md": generate_skills_page(skills),
        "services.md": generate_services_page(services),
        "jobs.md": generate_jobs_page(jobs),
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
