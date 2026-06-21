"""Tests for page generation (LLM client and orchestration), with mocked LLM."""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add tools root to path
_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_ROOT))

from docs.output.format_markdown import format_markdown


def test_format_markdown_strips_wrapping_fence():
    content = "```markdown\n# Title\n\nSome content.\n```"
    result = format_markdown(content)
    assert result.startswith("# Title")
    assert "```markdown" not in result


def test_format_markdown_enforces_single_h1():
    content = "# Title One\n\n# Title Two\n\nSome text."
    result = format_markdown(content)
    import re
    h1_count = sum(1 for line in result.split("\n") if re.match(r"^# [^#]", line))
    assert h1_count == 1


def test_format_markdown_single_trailing_newline():
    content = "# Title\n\nContent here.\n\n\n"
    result = format_markdown(content)
    assert result.endswith("\n")
    assert not result.endswith("\n\n")


def test_format_markdown_normalizes_line_endings():
    content = "# Title\r\n\r\nContent.\r\n"
    result = format_markdown(content)
    assert "\r" not in result


def test_generate_page_missing_token():
    """generate_page raises EnvironmentError when GITHUB_TOKEN is missing."""
    import os
    env_backup = os.environ.pop("GITHUB_TOKEN", None)
    try:
        from docs.generation.generate_page import generate_page
        try:
            generate_page("test prompt")
            assert False, "Should have raised EnvironmentError"
        except EnvironmentError as e:
            assert "GITHUB_TOKEN" in str(e)
    finally:
        if env_backup is not None:
            os.environ["GITHUB_TOKEN"] = env_backup


def test_generate_page_calls_openai():
    """generate_page calls the OpenAI client with the prompt."""
    import os
    from unittest.mock import patch, MagicMock

    mock_choice = MagicMock()
    mock_choice.message.content = "# Generated\n\nContent here."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_response.usage = None

    mock_client_instance = MagicMock()
    mock_client_instance.chat.completions.create.return_value = mock_response
    mock_openai_class = MagicMock(return_value=mock_client_instance)
    mock_openai_module = MagicMock()
    mock_openai_module.OpenAI = mock_openai_class

    with patch.dict(os.environ, {"GITHUB_TOKEN": "test-gh-token"}):
        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            from importlib import reload
            import docs.generation.generate_page as gp
            reload(gp)
            result = gp.generate_page("test prompt")
            assert "Generated" in result


def test_process_page_bundle_plugins_renders_without_llm(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    plugins_dir = bundle_root / "plugins"
    plugins_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["plugins/github.json"]}),
        encoding="utf-8",
    )
    (plugins_dir / "github.json").write_text(
        json.dumps(
            {
                "plugin": "github",
                "summary": "Manage GitHub issues.",
                "configuration": "```json\n{\n  \"enabled\": true\n}\n```",
                "config_schema": {
                    "type": "object",
                    "properties": {
                        "token": {
                            "type": "string",
                            "description": "GitHub token",
                        },
                        "repos": {
                            "type": "array",
                            "description": "Configured repositories",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "owner": {
                                        "type": "string",
                                        "description": "Repository owner",
                                    },
                                    "name": {
                                        "type": "string",
                                        "description": "Repository name",
                                    },
                                },
                                "required": ["owner", "name"],
                            },
                        },
                    },
                },
                "env_vars": [
                    {
                        "name": "GITHUB_TOKEN",
                        "required": True,
                        "description": "GitHub access token",
                    }
                ],
                "tools": [
                    {
                        "name": "github_list_issues",
                        "description": "List issues in a repository.",
                        "parameters": {
                            "owner": {
                                "type": "string",
                                "required": True,
                                "description": "Repository owner",
                            },
                            "state": {
                                "type": "string",
                                "required": False,
                                "description": "Issue state",
                                "enum": ["open", "closed"],
                                "default": "open",
                            },
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "plugins-overview",
        "output_path": "docs/plugins.md",
        "template": "overview",
        "strategy": "bundle-plugins",
        "chunk_source": "plugins/*.json",
        "chunk_output_dir": "docs/plugins",
        "front_matter": {
            "layout": "default",
            "title": "Plugins",
            "nav_order": 3,
            "has_children": True,
        },
        "sources": [
            {"path": "plugins/*.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/plugins.md"
    index_content = (repo_root / "docs/plugins.md").read_text(encoding="utf-8")
    child_content = (repo_root / "docs/plugins/github.md").read_text(encoding="utf-8")

    assert "[GitHub](plugins/github)" in index_content
    assert "# 🐙 GitHub" in child_content
    assert "## Configuration Schema" in child_content
    assert "## Example config" in child_content
    assert child_content.index("## Configuration Schema") < child_content.index("## Example config")
    assert '"enabled": true' in child_content
    assert '<table class="config-schema-table">' in child_content
    assert "<th>Description</th>" in child_content
    assert "<td><code>token</code></td><td>string</td><td>Optional</td><td>GitHub token.</td>" in child_content
    assert "<td><code>repos[].owner</code></td><td>string</td><td>Required</td><td>Repository owner.</td>" in child_content
    assert "## Environment Variables" in child_content
    assert "| `GITHUB_TOKEN` | Yes | GitHub access token |" in child_content
    assert "## Tools" in child_content
    assert "### `github_list_issues`" in child_content
    assert "| Name | Type | Required | Description |" in child_content
    assert "| `owner` | string | Required | Repository owner. |" in child_content
    assert "Allowed: `open`, `closed`." in child_content
    assert "Default: `open`." in child_content


def test_process_page_bundle_plugins_mixes_local_and_external_inventory(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    plugins_dir = bundle_root / "plugins"
    plugins_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["plugins/fastmail.json", "runtime-plugins.json"]}),
        encoding="utf-8",
    )
    (plugins_dir / "fastmail.json").write_text(
        json.dumps(
            {
                "plugin": "fastmail",
                "name": "FastMail tools",
                "summary": "Send mail and manage calendar events.",
                "tools": [{"name": "fastmail_send", "description": "Send email."}],
            }
        ),
        encoding="utf-8",
    )
    (bundle_root / "runtime-plugins.json").write_text(
        json.dumps(
            {
                "plugins": [
                    {
                        "id": "fastmail",
                        "name": "FastMail tools",
                        "summary": "Send mail and manage calendar events.",
                        "emoji": "📧",
                        "origin": "openclaw-hub",
                        "docs_mode": "local",
                        "docs_url": "/plugins/fastmail",
                        "source_url": "https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail",
                        "tool_count": 1,
                    },
                    {
                        "id": "telegram",
                        "name": "Telegram",
                        "summary": "Chat channel plugin used by the live assistant.",
                        "emoji": "💬",
                        "origin": "external",
                        "docs_mode": "external",
                        "docs_url": "https://core.telegram.org/bots",
                        "source_url": "https://core.telegram.org/bots",
                        "tool_count": None,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "plugins-overview",
        "output_path": "docs/plugins.md",
        "template": "overview",
        "strategy": "bundle-plugins",
        "overview_source": "runtime-plugins.json",
        "chunk_source": "plugins/*.json",
        "chunk_output_dir": "docs/plugins",
        "front_matter": {
            "layout": "default",
            "title": "Plugins",
            "nav_order": 3,
            "has_children": True,
        },
        "sources": [
            {"path": "runtime-plugins.json"},
            {"path": "plugins/*.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/plugins.md"
    index_content = (repo_root / "docs/plugins.md").read_text(encoding="utf-8")
    child_content = (repo_root / "docs/plugins/fastmail.md").read_text(encoding="utf-8")

    assert "## 📦 Open Source" in index_content
    assert "## 🔌 External" in index_content
    assert "[FastMail tools](plugins/fastmail)" in index_content
    assert "[GitHub ↗](https://core.telegram.org/bots)" in index_content
    assert "**Source:**" in child_content
    assert "openclaw-hub" in child_content
    assert "# 📧 FastMail tools" in child_content


def test_process_page_bundle_plugins_without_inventory_keeps_local_overview(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    plugins_dir = bundle_root / "plugins"
    plugins_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["plugins/github.json"]}),
        encoding="utf-8",
    )
    (plugins_dir / "github.json").write_text(
        json.dumps(
            {
                "plugin": "github",
                "name": "GitHub",
                "summary": "Manage GitHub issues.",
                "tools": [{"name": "github_list_issues", "description": "List issues."}],
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "plugins-overview",
        "output_path": "docs/plugins.md",
        "template": "overview",
        "strategy": "bundle-plugins",
        "chunk_source": "plugins/*.json",
        "chunk_output_dir": "docs/plugins",
        "front_matter": {
            "layout": "default",
            "title": "Plugins",
            "nav_order": 3,
            "has_children": True,
        },
        "sources": [{"path": "plugins/*.json"}],
    }

    ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    index_content = (repo_root / "docs/plugins.md").read_text(encoding="utf-8")

    assert "## 🔒 Private (octo)" in index_content
    assert "[GitHub](plugins/github)" in index_content


def test_process_page_bundle_service_detail_renders_without_llm(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    services_dir = bundle_root / "services"
    services_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["services/demo.json"]}),
        encoding="utf-8",
    )
    (services_dir / "demo.json").write_text(
        json.dumps(
            {
                "service": "demo",
                "name": "Demo Service",
                "summary": "Structured demo service summary.",
                "sections": {
                    "Features": "- One\n- Two",
                    "Configuration": "Use deterministic bundle data.",
                },
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "demo-service",
        "output_path": "docs/services/demo.md",
        "template": "overview",
        "strategy": "bundle-service-detail",
        "front_matter": {
            "layout": "default",
            "title": "Demo Service",
            "parent": "Services",
            "nav_order": 1,
        },
        "sources": [
            {"path": "services/demo.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/services/demo.md"
    content = (repo_root / "docs/services/demo.md").read_text(encoding="utf-8")
    assert "# Demo Service" in content
    assert "Structured demo service summary." in content
    assert "## Features" in content
    assert "Use deterministic bundle data." in content


def test_process_page_bundle_scheduled_tasks_renders_without_llm(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["jobs.json"]}),
        encoding="utf-8",
    )
    (bundle_root / "jobs.json").write_text(
        json.dumps(
            {
                "jobs": [
                    {
                        "name": "daily-health-check",
                        "category": "infrastructure",
                        "public": True,
                        "summary": "Checks outbound email health.",
                        "schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "America/Los_Angeles"},
                    },
                    {
                        "name": "calendar-fetch-hourly",
                        "category": "feature",
                        "public": False,
                        "summary": "Refreshes calendar memory snapshots.",
                        "schedule": {"kind": "cron", "expr": "0 7-17 * * *", "tz": "America/Los_Angeles"},
                    },
                    {
                        "name": "test-reminder",
                        "category": "feature",
                        "public": False,
                        "summary": "Should be hidden.",
                        "schedule": {"kind": "at", "at": "2026-04-11T06:20:00.000Z"},
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "scheduled-tasks",
        "output_path": "docs/scheduled-tasks.md",
        "template": "overview",
        "strategy": "bundle-scheduled-tasks",
        "front_matter": {
            "layout": "default",
            "title": "Scheduled Tasks",
            "nav_order": 6,
        },
        "sources": [
            {"path": "jobs.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/scheduled-tasks.md"
    content = (repo_root / "docs/scheduled-tasks.md").read_text(encoding="utf-8")
    assert "## Infrastructure Tasks" in content
    assert "`daily-health-check`" in content
    assert "Checks outbound email health." in content
    assert "calendar-fetch-hourly" not in content
    assert "test-reminder" not in content


def test_process_page_bundle_hooks_renders_without_llm(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    agents_dir = bundle_root / "agents"
    agents_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["agents/hass-hooks.json"]}),
        encoding="utf-8",
    )
    (agents_dir / "hass-hooks.json").write_text(
        json.dumps(
            {
                "agent": "hass-hooks",
                "summary": "React to Home Assistant webhooks.",
                "sections": {
                    "What arrives": "Webhook payload fields.",
                    "Step 1": "Decide if the event matters.",
                },
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "hooks-overview",
        "output_path": "docs/hooks.md",
        "template": "overview",
        "strategy": "bundle-hooks",
        "chunk_source": "agents/*hooks*.json",
        "chunk_output_dir": "docs/hooks",
        "front_matter": {
            "layout": "default",
            "title": "Hooks",
            "nav_order": 6,
            "has_children": True,
        },
        "sources": [
            {"path": "agents/*hooks*.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/hooks.md"
    index_content = (repo_root / "docs/hooks.md").read_text(encoding="utf-8")
    child_content = (repo_root / "docs/hooks/hass-hooks.md").read_text(encoding="utf-8")
    assert "# Hooks" in index_content
    assert "[Hass Hooks](hooks/hass-hooks)" in index_content
    assert "# 🪝 Hass Hooks" in child_content
    assert "React to Home Assistant webhooks." in child_content
    assert "## What arrives" in child_content
    assert "## Step 1" in child_content


def test_process_page_bundle_skills_renders_without_llm(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    skills_dir = bundle_root / "skills"
    skills_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["skills/home-music.json"]}),
        encoding="utf-8",
    )
    (skills_dir / "home-music.json").write_text(
        json.dumps(
            {
                "name": "home-music",
                "description": "Control music around the house.",
                "content": "# Home Music Skill\n\nControl music.\n\n## Rules\n\n- Be careful.\n",
                "agent": "main",
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "skills-overview",
        "output_path": "docs/skills.md",
        "template": "overview",
        "strategy": "bundle-skills",
        "chunk_source": "skills/*.json",
        "chunk_output_dir": "docs/skills",
        "front_matter": {
            "layout": "default",
            "title": "Skills",
            "nav_order": 4,
            "has_children": True,
        },
        "sources": [
            {"path": "skills.json"},
            {"path": "skills/*.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/skills.md"
    index_content = (repo_root / "docs/skills.md").read_text(encoding="utf-8")
    child_content = (repo_root / "docs/skills/home-music.md").read_text(encoding="utf-8")
    assert "# Skills" in index_content
    assert "[Home Music](skills/home-music)" in index_content
    assert "`main`" in index_content
    assert "# 🎵 Home Music" in child_content
    assert "## Rules" in child_content


def test_process_page_bundle_skills_omits_empty_table_when_no_skills(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    skills_dir = bundle_root / "skills"
    skills_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["skills.json"]}),
        encoding="utf-8",
    )
    (bundle_root / "skills.json").write_text(
        json.dumps({"skills": []}),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "skills-overview",
        "output_path": "docs/skills.md",
        "template": "overview",
        "strategy": "bundle-skills",
        "chunk_source": "skills/*.json",
        "chunk_output_dir": "docs/skills",
        "front_matter": {
            "layout": "default",
            "title": "Skills",
            "nav_order": 4,
            "has_children": True,
        },
        "sources": [
            {"path": "skills.json"},
            {"path": "skills/*.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/skills.md"
    index_content = (repo_root / "docs/skills.md").read_text(encoding="utf-8")
    assert "No public skills are currently published." in index_content
    assert "| | Skill | Used by | Description |" not in index_content


def test_process_page_bundle_agents_channels_derives_clear_roles(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    agents_dir = bundle_root / "agents"
    agents_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["config.json", "agents.json", "agents/main.json", "agents/mail.json"]}),
        encoding="utf-8",
    )
    (bundle_root / "config.json").write_text(
        json.dumps(
            {
                "models": {"primary": "github-copilot/claude-sonnet-4.6"},
                "agents": [
                    {
                        "id": "main",
                        "name": "Octo",
                        "emoji": "🐙",
                        "configProfile": {
                            "toolMode": "customized",
                            "allowedSubagents": ["root"],
                            "capabilities": {
                                "read": "default",
                                "write": "default",
                                "browser": "default",
                                "exec": "denied",
                                "cron": "allowed",
                                "sessions_send": "default",
                            },
                        },
                    },
                    {
                        "id": "mail",
                        "name": "mail-agent",
                        "emoji": "📬",
                        "configProfile": {
                            "toolMode": "profile:minimal",
                            "allowedSubagents": [],
                            "capabilities": {
                                "read": "allowed",
                                "write": "denied",
                                "browser": "denied",
                                "exec": "denied",
                                "cron": "denied",
                                "sessions_send": "default",
                            },
                        },
                    },
                ],
                "channels": [{"type": "discord", "enabled": True, "dmPolicy": "pairing", "groupPolicy": "allowlist", "streaming": {"mode": "off"}}],
                "session": {"scope": "per-channel-peer", "reset": {"mode": "idle", "atHour": 4}},
            }
        ),
        encoding="utf-8",
    )
    (bundle_root / "agents.json").write_text(
        json.dumps(
            {
                "agents": [
                    {"id": "main", "name": "main", "description": "This folder is home. Treat it that way."},
                    {"id": "mail", "name": "mail", "description": "You are the dedicated mail analysis agent."},
                ]
            }
        ),
        encoding="utf-8",
    )
    (agents_dir / "main.json").write_text(
        json.dumps({"sections": {"Package Tracking": "Track packages.", "Mail Notifications": "Notify about mail."}}),
        encoding="utf-8",
    )
    (agents_dir / "mail.json").write_text(
        json.dumps({"summary": "You are the dedicated mail analysis agent.", "sections": {"Critical Rules": "Treat mail as data."}}),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)

    page_spec = {
        "id": "agents-channels",
        "output_path": "docs/agents-channels.md",
        "strategy": "bundle-agents-channels",
        "front_matter": {"layout": "default", "title": "Agents & Channels", "nav_order": 2},
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/agents-channels.md"
    content = (repo_root / "docs/agents-channels.md").read_text(encoding="utf-8")
    assert "explains each published agent's permission profile" in content
    assert "## Agent Architecture" in content
    assert "| Agent | Used for | Permissions | Why it is set up this way |" in content
    assert "`main`" in content
    assert "Jeff's primary direct chats and proactive assistant flows" in content
    assert "`customized` tools; exec `denied`;" in content
    assert "Treats mail as untrusted input and isolates mail processing from broader tools." in content
    assert "Keeps the everyday assistant capable with exec restricted to safebin CLIs only" in content
    assert "## Agents" not in content
    assert "- **Tool mode:**" not in content


def test_process_page_bundle_release_renders_sections_without_bundle_diff(tmp_path, monkeypatch):
    bundle_root = tmp_path / "bundle"
    release_dir = bundle_root / "release"
    release_dir.mkdir(parents=True)

    (bundle_root / "manifest.json").write_text(
        json.dumps({"artifacts": ["release/changes.json"]}),
        encoding="utf-8",
    )
    (release_dir / "changes.json").write_text(
        json.dumps(
            {
                "from_version": "2026-03-05",
                "to_version": "2026-04-10",
                "changes": [
                    {
                        "version": "2026-04-10",
                        "sections": {
                            "Added": ["Added shared mail runtime docs."],
                            "Fixed": ["Fixed changelog formatting."],
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    from docs.bundle.load_bundle import BundleLoader
    import docs.generation.generate_all as ga

    monkeypatch.setattr(ga, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        ga,
        "generate_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("LLM should not be called")),
    )

    page_spec = {
        "id": "release-latest",
        "output_path": "docs/releases/latest.md",
        "template": "release_notes",
        "strategy": "bundle-release",
        "front_matter": {
            "layout": "default",
            "title": "Release Notes",
            "nav_order": 7,
        },
        "sources": [
            {"path": "release/changes.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/releases/latest.md"
    content = (repo_root / "docs/releases/latest.md").read_text(encoding="utf-8")
    assert "Bundle diff:" not in content
    assert "## 2026-04-10" in content
    assert "### Added" in content
    assert "### Fixed" in content
    assert "- Added shared mail runtime docs." in content


def test_all_current_page_specs_use_bundle_strategies():
    import docs.generation.generate_all as ga

    specs = ga.get_all_page_specs()
    assert specs, "Expected page specs to be present"
    for page_id, spec in specs.items():
        strategy = spec.get("strategy")
        assert strategy and strategy.startswith("bundle-"), (
            f"Expected {page_id} to use a deterministic bundle strategy, got {strategy!r}"
        )
