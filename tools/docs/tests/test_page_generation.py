"""Tests for page generation (LLM client and orchestration), with mocked LLM."""

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


def test_generate_page_missing_api_key():
    """generate_page raises EnvironmentError when API key is missing."""
    import os
    with patch.dict(os.environ, {}, clear=False):
        # Remove the key if set
        env_backup = os.environ.pop("DOCS_LLM_API_KEY", None)
        try:
            from docs.generation.generate_page import generate_page
            try:
                generate_page("test prompt")
                assert False, "Should have raised EnvironmentError"
            except EnvironmentError as e:
                assert "DOCS_LLM_API_KEY" in str(e)
        finally:
            if env_backup is not None:
                os.environ["DOCS_LLM_API_KEY"] = env_backup


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

    with patch.dict(os.environ, {"DOCS_LLM_API_KEY": "test-key", "DOCS_LLM_MODEL": "gpt-4o"}):
        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            from importlib import reload
            import docs.generation.generate_page as gp
            reload(gp)
            result = gp.generate_page("test prompt")
            assert "Generated" in result
