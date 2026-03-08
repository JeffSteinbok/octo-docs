#!/usr/bin/env python3
"""
generate-docs: Reads the openclaw config and uses the GitHub Copilot CLI
to render documentation pages. Section files in sections/*.md contain
LLM prompts that instruct the Copilot CLI how to format the gathered data
into Jekyll markdown pages.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml")
    raise SystemExit(1)

SECTIONS_DIR = Path(__file__).resolve().parent / "sections"


def parse_frontmatter_md(path: Path) -> dict:
    """Parse an MD file with optional YAML frontmatter, returning meta + body."""
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
            # Runtime layout: agents/<id>/workspace/skills
            ws = agent_dir / "workspace" / "skills"
            if ws.is_dir():
                skill_search_dirs.append(ws)
            # Repo layout: agents/<id>/skills (no workspace indirection)
            direct = agent_dir / "skills"
            if direct.is_dir() and direct != ws:
                skill_search_dirs.append(direct)

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
                parsed = parse_frontmatter_md(skill_md)
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
    # Repo layout: config_dir IS the repo root
    candidates.append(config_dir / "config" / "jobs.json")

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
            "source": "openclaw",
        })
    return jobs


def humanize_cron(expr: str) -> str:
    """Convert a cron expression like '0 8 * * *' to human-readable text."""
    parts = expr.split()
    if len(parts) != 5:
        return expr
    minute, hour, dom, month, dow = parts

    day_names = {"0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed",
                 "4": "Thu", "5": "Fri", "6": "Sat", "7": "Sun"}

    # Every minute
    if all(p == "*" for p in parts):
        return "Every minute"

    # Simple interval patterns: */N
    if minute.startswith("*/") and hour == "*" and dom == "*" and month == "*" and dow == "*":
        return f"Every {minute[2:]}m"
    if minute == "0" and hour.startswith("*/") and dom == "*" and month == "*" and dow == "*":
        return f"Every {hour[2:]}h"

    # Daily at HH:MM
    if dom == "*" and month == "*" and dow == "*" and not hour.startswith("*/"):
        time_str = f"{int(hour)}:{minute.zfill(2)} AM" if int(hour) < 12 else (
            f"{int(hour) - 12 if int(hour) > 12 else 12}:{minute.zfill(2)} PM"
        )
        return f"Daily at {time_str}"

    # Specific days of week
    if dom == "*" and month == "*" and dow != "*":
        days = [day_names.get(d, d) for d in dow.split(",")]
        time_str = f"{int(hour)}:{minute.zfill(2)} AM" if int(hour) < 12 else (
            f"{int(hour) - 12 if int(hour) > 12 else 12}:{minute.zfill(2)} PM"
        )
        return f"{','.join(days)} at {time_str}"

    return expr


def load_crontab_jobs() -> list[dict]:
    """Load jobs from the system crontab (sanitized)."""
    import subprocess
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return []
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []

    jobs = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 5)
        if len(parts) < 6:
            continue
        cron_expr = " ".join(parts[:5])
        command = parts[5]
        cmd_path = Path(command.split()[0])
        name = cmd_path.stem
        jobs.append({
            "name": name,
            "description": humanize_cron(cron_expr),
            "enabled": True,
            "interval": humanize_cron(cron_expr),
            "source": "crontab",
        })
    return jobs


def load_repo_readme(config_dir: Path) -> str:
    """Load README.md from the openclaw config repo (via workspace symlink or direct)."""
    # Runtime: agents/main/workspace -> repo/agents/main
    ws = config_dir / "agents" / "main" / "workspace"
    if ws.is_symlink() or ws.is_dir():
        repo_root = ws.resolve().parent.parent
        readme = repo_root / "README.md"
        if readme.exists():
            return readme.read_text(encoding="utf-8", errors="ignore")
    # Repo layout: config_dir IS the repo root
    readme = config_dir / "README.md"
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
            # Repo layout: agents/<id> is the workspace itself
            candidate = config_dir / "agents" / agent_id
            if candidate.is_dir():
                ws = candidate
            else:
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
    else:
        # Repo layout: config_dir IS the repo root
        if (config_dir / "services").is_dir():
            search_dirs.append(config_dir / "services")
        hub_services = config_dir.parent / "openclaw-hub" / "services"
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
                    parsed = parse_frontmatter_md(doc_path)
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


def extract_models(config: dict) -> dict:
    """Extract model config from agents.defaults."""
    defaults = config.get("agents", {}).get("defaults", {})
    model = defaults.get("model", {})
    image_model = defaults.get("imageModel", {})
    web_search = config.get("tools", {}).get("web", {}).get("search", {}).get("gemini", {}).get("model", "")
    return {
        "primary": model.get("primary", ""),
        "fallbacks": model.get("fallbacks", []),
        "image_primary": image_model.get("primary", ""),
        "image_fallbacks": image_model.get("fallbacks", []),
        "web_search": web_search,
    }


# ---------------------------------------------------------------------------
# Copilot CLI rendering
# ---------------------------------------------------------------------------


def render_with_copilot(prompt: str, timeout: int = 120) -> str:
    """Call the GitHub Copilot CLI with a prompt and return the response text."""
    prompt_len = len(prompt)
    print(f"    Prompt size: {prompt_len:,} chars")
    sys.stdout.flush()
    try:
        result = subprocess.run(
            ["gh", "copilot", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        print("Error: 'gh' CLI not found. Install from https://cli.github.com",
              file=sys.stderr)
        raise SystemExit(1)
    except subprocess.TimeoutExpired:
        print(f"    ✗ Copilot CLI timed out after {timeout}s", file=sys.stderr)
        return ""

    if result.returncode != 0:
        print(f"    ✗ Copilot CLI error (exit {result.returncode}): "
              f"{result.stderr.strip()}", file=sys.stderr)
        return ""

    output = result.stdout.strip()
    # Strip wrapping code fences the LLM sometimes adds
    if output.startswith("```"):
        lines = output.split("\n")
        if lines[-1].strip() == "```":
            output = "\n".join(lines[1:-1])
    print(f"    ✓ Got {len(output):,} chars back")
    sys.stdout.flush()
    return output


def build_prompt(section_body: str, data: dict) -> str:
    """Construct a rendering prompt from section instructions and gathered data."""
    data_json = json.dumps(data, indent=2, default=str)
    return (
        "You are generating a page for a Jekyll documentation site about OpenClaw, "
        "a modular AI assistant framework.\n\n"
        f"{section_body}\n\n"
        "## Data\n\n"
        f"```json\n{data_json}\n```\n\n"
        "IMPORTANT RULES:\n"
        "- Output ONLY the markdown body content.\n"
        "- Do NOT include Jekyll frontmatter (--- blocks).\n"
        "- Do NOT wrap your response in code fences.\n"
        "- Never include secrets, IP addresses, emails, account IDs, or personal identifiers.\n"
        "- Be concise and well-structured."
    )


# ---------------------------------------------------------------------------
# --source mode: read directly from an openclaw repo checkout
# ---------------------------------------------------------------------------


def discover_plugins_from_source(source: Path) -> list[dict]:
    """Discover plugins from a local openclaw repo checkout."""
    plugins = []
    plugins_dir = source / "plugins"
    if not plugins_dir.is_dir():
        return plugins
    for plugin_dir in sorted(plugins_dir.iterdir()):
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
            continue
        manifest = plugin_dir / "openclaw.plugin.json"
        if not manifest.exists():
            continue
        with open(manifest, encoding="utf-8") as f:
            info = json.load(f)
        readme = plugin_dir / "README.md"
        body = ""
        if readme.exists():
            parsed = parse_frontmatter_md(readme)
            body = parsed["body"]
        plugins.append({
            "name": info.get("name", plugin_dir.name),
            "description": info.get("description", ""),
            "version": info.get("version", ""),
            "emoji": info.get("emoji", "🔧"),
            "bins": [],
            "packages": [],
            "body": body,
            "source_url": None,
        })
    return plugins


def load_config_from_source(source: Path) -> dict:
    """Load openclaw.json from the repo's config directory."""
    cfg_path = source / "config" / "openclaw.json"
    if cfg_path.exists():
        with open(cfg_path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_jobs_from_source(source: Path) -> list[dict]:
    """Load jobs.json from the repo's config directory."""
    jobs_path = source / "config" / "jobs.json"
    if not jobs_path.exists():
        return []
    with open(jobs_path, encoding="utf-8") as f:
        data = json.load(f)
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
            "source": "openclaw",
        })
    return jobs


def discover_services_from_source(source: Path) -> list[dict]:
    """Discover services from a local openclaw repo checkout."""
    services = []
    services_dir = source / "services"
    if not services_dir.is_dir():
        return services
    for svc_dir in sorted(services_dir.iterdir()):
        if not svc_dir.is_dir() or svc_dir.name.startswith("."):
            continue
        svc = {"name": svc_dir.name, "description": "", "type": "daemon"}
        service_files = list(svc_dir.glob("*.service"))
        if service_files:
            svc["type"] = "systemd"
        for doc_name in ["SKILL.md", "README.md"]:
            doc_path = svc_dir / doc_name
            if doc_path.exists():
                parsed = parse_frontmatter_md(doc_path)
                svc["description"] = parsed["meta"].get("description", "")
                if not svc["description"]:
                    for line in parsed["body"].split("\n"):
                        if line.strip() and not line.startswith("#"):
                            svc["description"] = line.strip()
                            break
                break
        services.append(svc)
    return services


def load_readme_from_source(source: Path) -> str:
    """Load README.md from the openclaw repo checkout."""
    readme = source / "README.md"
    if readme.exists():
        return readme.read_text(encoding="utf-8", errors="ignore")
    return ""


# ---------------------------------------------------------------------------
# Page generation
# ---------------------------------------------------------------------------


def generate_page(section: dict, data: dict, i: int = 0, total: int = 0) -> str:
    """Generate a complete Jekyll page by calling the Copilot CLI."""
    meta = section["meta"]
    body = section["body"]

    # Strip legacy <!-- instructions: ... --> HTML comments
    body = re.sub(r"<!--\s*instructions:.*?-->\s*", "", body, flags=re.DOTALL)

    # Select relevant data slices
    data_keys = meta.get("data_keys", [])
    if data_keys:
        relevant = {k: data.get(k, []) for k in data_keys}
    else:
        relevant = data

    prompt = build_prompt(body, relevant)

    print(f"  [{i}/{total}] Rendering {meta['output']} via Copilot CLI ...")
    sys.stdout.flush()
    rendered = render_with_copilot(prompt)

    if not rendered:
        print(f"  [{i}/{total}] ✗ Empty response for {meta['output']}")
        rendered = "_Documentation generation pending — re-run the workflow to generate._"
    else:
        print(f"  [{i}/{total}] ✓ {meta['output']} complete")

    header = "\n".join([
        "---",
        "layout: default",
        f"title: {meta['title']}",
        f"nav_order: {meta.get('nav_order', 99)}",
        "---",
        "",
        f"# {meta['title']}",
        "",
        "*Generated by an AI skill reading the live OpenClaw configs from Octo.* 🐙",
        "",
    ])

    return header + "\n" + rendered.rstrip("\n") + "\n"


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
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Path to a local openclaw repo checkout (CI mode)",
    )
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()

    # --source mode: read directly from a repo checkout (for CI)
    if args.source is not None:
        source = args.source.resolve()
        if not source.exists():
            print(f"Error: Source directory not found at {source}")
            raise SystemExit(1)

        print(f"Reading source from: {source}")
        print(f"Writing docs to:     {output_dir}")

        plugins = discover_plugins_from_source(source)
        skills = []  # Skills are discovered at runtime; plugins come from source
        services = discover_services_from_source(source)
        config = load_config_from_source(source)
        agents = extract_agents(config, source)
        channels = extract_channels(config)
        jobs = load_jobs_from_source(source)
        models = extract_models(config)

        print(f"Found {len(plugins)} plugins, {len(skills)} skills, "
              f"{len(services)} services, {len(agents)} agents, "
              f"{len(channels)} channels, {len(jobs)} jobs")

        data = {
            "plugins": plugins,
            "skills": skills,
            "services": services,
            "agents": agents,
            "channels": channels,
            "jobs": jobs,
            "models": models,
        }

        output_dir.mkdir(parents=True, exist_ok=True)

        if not SECTIONS_DIR.is_dir():
            print(f"Error: Sections directory not found at {SECTIONS_DIR}")
            raise SystemExit(1)

        sections = sorted(SECTIONS_DIR.glob("*.md"))
        total = len(sections)
        print(f"\nRendering {total} sections ...\n")
        sys.stdout.flush()

        for i, section_path in enumerate(sections, 1):
            section = parse_frontmatter_md(section_path)
            meta = section["meta"]
            if "output" not in meta:
                print(f"  [{i}/{total}] Skipping {section_path.name} (no output defined)")
                continue

            content = generate_page(section, data, i, total)
            out_path = output_dir / meta["output"]
            out_path.write_text(content, encoding="utf-8")
            print(f"  Wrote {out_path}")

        print("\nDone!")
        return

    # Legacy mode: read from ~/.openclaw runtime directory
    config_dir = args.config_dir.resolve()

    if not config_dir.exists():
        print(f"Error: Config directory not found at {config_dir}")
        raise SystemExit(1)

    print(f"Reading config from: {config_dir}")
    print(f"Writing docs to:     {output_dir}")

    plugins = []  # Plugins come from source repo only
    skills = discover_skills(config_dir)
    services = discover_services(config_dir)
    config = load_config(config_dir)
    agents = extract_agents(config, config_dir)
    channels = extract_channels(config)
    jobs = load_jobs(config_dir) + load_crontab_jobs()
    models = extract_models(config)

    print(f"Found {len(plugins)} plugins, {len(skills)} skills, "
          f"{len(services)} services, {len(agents)} agents, "
          f"{len(channels)} channels, {len(jobs)} jobs")

    data = {
        "plugins": plugins,
        "skills": skills,
        "services": services,
        "agents": agents,
        "channels": channels,
        "jobs": jobs,
        "models": models,
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    if not SECTIONS_DIR.is_dir():
        print(f"Error: Sections directory not found at {SECTIONS_DIR}")
        raise SystemExit(1)

    sections = sorted(SECTIONS_DIR.glob("*.md"))
    total = len(sections)
    print(f"\nRendering {total} sections ...\n")
    sys.stdout.flush()

    for i, section_path in enumerate(sections, 1):
        section = parse_frontmatter_md(section_path)
        meta = section["meta"]
        if "output" not in meta:
            print(f"  [{i}/{total}] Skipping {section_path.name} (no output defined)")
            continue
        content = generate_page(section, data, i, total)
        out_path = output_dir / meta["output"]
        out_path.write_text(content, encoding="utf-8")
        print(f"  Wrote {out_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()
