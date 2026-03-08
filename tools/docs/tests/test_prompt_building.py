"""Tests for prompt building."""

import json
import sys
from pathlib import Path

# Add tools root to path
_TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_ROOT))

from docs.generation.build_prompt import build_prompt


def test_build_prompt_contains_base_and_template():
    page_spec = {
        "id": "auth-overview",
        "output_path": "docs/auth/overview.md",
        "template": "overview",
        "instructions": {
            "audience": "external developers",
            "include": ["overview", "auth flow"],
            "exclude": ["internal names"],
        },
    }
    selected = {
        "page_id": "auth-overview",
        "template": "overview",
        "source_material": {
            "modules/auth.json": {"summary": "Auth module", "endpoints": ["/login"]},
        },
    }
    prompt = build_prompt(page_spec, selected)
    assert "auth-overview" in prompt
    assert "external developers" in prompt
    assert "overview" in prompt.lower()
    assert "modules/auth.json" in prompt
    assert "Auth module" in prompt


def test_build_prompt_includes_include_and_exclude():
    page_spec = {
        "id": "test-page",
        "output_path": "docs/test.md",
        "template": "overview",
        "instructions": {
            "audience": "admins",
            "include": ["thing a", "thing b"],
            "exclude": ["secret stuff"],
        },
    }
    selected = {
        "page_id": "test-page",
        "template": "overview",
        "source_material": {},
    }
    prompt = build_prompt(page_spec, selected)
    assert "thing a" in prompt
    assert "thing b" in prompt
    assert "secret stuff" in prompt


def test_build_prompt_injects_json_source():
    page_spec = {
        "id": "api-page",
        "output_path": "docs/api.md",
        "template": "api_reference",
        "instructions": {},
    }
    selected = {
        "page_id": "api-page",
        "template": "api_reference",
        "source_material": {
            "modules/api.json": {"endpoint": "/v1/test"},
        },
    }
    prompt = build_prompt(page_spec, selected)
    assert "/v1/test" in prompt
    assert "modules/api.json" in prompt
