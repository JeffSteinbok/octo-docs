#!/usr/bin/env python3
"""LLM client: sends prompts to an LLM API and returns generated markdown."""

import os
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "gpt-4o"
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_RETRY_DELAY = 2.0


def generate_page(
    prompt: str,
    model: Optional[str] = None,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_delay: float = _DEFAULT_RETRY_DELAY,
) -> str:
    """
    Send a prompt to the GitHub Models LLM API and return the generated markdown.

    Authentication uses the GitHub token (GITHUB_TOKEN environment variable),
    which is automatically available in GitHub Actions with no additional secrets
    configuration. For local use, export a GitHub personal access token.

    Environment variables:
        GITHUB_TOKEN        - GitHub token (required); used with the GitHub Models endpoint
        DOCS_LLM_BASE_URL   - Optional override for the GitHub Models base URL

    Args:
        prompt: The assembled prompt string
        model: Model override (default: claude-sonnet-4-6)
        max_retries: Number of retry attempts on transient failures
        retry_delay: Seconds to wait between retries

    Returns:
        Generated markdown content as a string
    """
    model = model or _DEFAULT_MODEL
    api_key = os.environ.get("GITHUB_TOKEN")
    base_url = os.environ.get("DOCS_LLM_BASE_URL", "https://models.inference.ai.azure.com")

    if not api_key:
        raise EnvironmentError(
            "GITHUB_TOKEN environment variable is required. "
            "In GitHub Actions it is set automatically. "
            "For local use, export a GitHub personal access token: "
            "export GITHUB_TOKEN=ghp_your-token"
        )

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            content = _call_openai_compatible(prompt, model, api_key, base_url)
            logger.info("Generated page using model=%s (attempt %d)", model, attempt)
            return content
        except _TransientError as e:
            last_error = e
            if attempt < max_retries:
                logger.warning(
                    "Transient error on attempt %d/%d: %s — retrying in %.1fs",
                    attempt, max_retries, e, retry_delay,
                )
                time.sleep(retry_delay)
        except Exception:
            raise

    raise RuntimeError(
        f"LLM API failed after {max_retries} attempts"
    ) from last_error


def _call_openai_compatible(
    prompt: str,
    model: str,
    api_key: str,
    base_url: Optional[str],
) -> str:
    """Call an OpenAI-compatible chat completion endpoint."""
    try:
        import openai
    except ImportError:
        raise ImportError(
            "The 'openai' package is required: pip install openai"
        )

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = openai.OpenAI(**client_kwargs)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
    except openai.RateLimitError as e:
        raise _TransientError(str(e)) from e
    except openai.APIConnectionError as e:
        raise _TransientError(str(e)) from e
    except openai.APITimeoutError as e:
        raise _TransientError(str(e)) from e

    choice = response.choices[0]
    content = choice.message.content or ""

    usage = getattr(response, "usage", None)
    if usage:
        logger.info(
            "Token usage — prompt: %d, completion: %d, total: %d",
            usage.prompt_tokens,
            usage.completion_tokens,
            usage.total_tokens,
        )

    return content


class _TransientError(Exception):
    """Marks a retriable API error."""
