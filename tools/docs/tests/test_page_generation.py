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
    assert "### `github_list_issues`" in child_content
    assert "| Name | Type | Required | Description |" in child_content
    assert "| `owner` | string | Required | Repository owner. |" in child_content
    assert "Allowed: `open`, `closed`." in child_content
    assert "Default: `open`." in child_content


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
        "front_matter": {
            "layout": "default",
            "title": "Hooks",
            "nav_order": 6,
        },
        "sources": [
            {"path": "agents/hass-hooks.json"},
        ],
    }

    output = ga.process_page(page_spec, BundleLoader(str(bundle_root)))

    assert output == "docs/hooks.md"
    content = (repo_root / "docs/hooks.md").read_text(encoding="utf-8")
    assert "# Hooks" in content
    assert "React to Home Assistant webhooks." in content
    assert "## What arrives" in content
    assert "## Step 1" in content


def test_all_current_page_specs_use_bundle_strategies():
    import docs.generation.generate_all as ga

    specs = ga.get_all_page_specs()
    assert specs, "Expected page specs to be present"
    for page_id, spec in specs.items():
        strategy = spec.get("strategy")
        assert strategy and strategy.startswith("bundle-"), (
            f"Expected {page_id} to use a deterministic bundle strategy, got {strategy!r}"
        )
