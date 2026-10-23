---
layout: default
title: Models
nav_order: 3
---

# Models

This page documents the AI models and voice configuration powering Octo.
All values are derived from live config so they stay accurate.

## Language Models

| Role | Model | Notes |
|------|-------|-------|
| Primary | `anthropic/claude-sonnet-4-6` | Default model for all agents |
| Fallback | `anthropic/claude-haiku-4-5` | Used when primary is unavailable |
| Fallback | `openai/gpt-6-astra` | Used when primary is unavailable |
| Image (vision) | `anthropic/claude-sonnet-4-6` | Used for image analysis |
| Image fallback | `anthropic/claude-haiku-4-5` | |
| Web search | `gemini` | Provider for web search tool |

### Per-Agent Overrides

Agents listed here use their own model instead of the default. Decision models are covered in
[Decision Models](#decision-models) below.

| Agent | Model | Decision model |
|-------|-------|----------------|
| `claude` | `anthropic/claude-opus-5-5` | — |
| `hassonic` | `openai/gpt-5.6-luna` | `typesafe/jev-latest` |

### Registered Aliases

| Alias | Model |
|-------|-------|
| `haiku` | `anthropic/claude-haiku-4-5` |
| `sonnet` | `anthropic/claude-sonnet-4-6` |
| `gpt-mini` | `openai/gpt-5.6-luna` |
| `gpt` | `openai/gpt-5.6-terra` |

## Decision Models

A [decision model](https://docs.openclaw.ai/concepts/decision-models) is a separate model role from the chat model.
It takes a fixed set of facts and a rubric and returns a typed answer — a choice, a score, or a yes/no with a
probability — instead of free text. That makes it fast, cheap and predictable for bounded judgments like
"is this safe to do without asking?", and the caller decides what to do with the probability.

Octo's decision models are served by [TypeSafe AI](https://docs.openclaw.ai/plugins/typesafe)'s hosted Jev models.

| Agent | Decision model |
|-------|----------------|
| `hassonic` | `typesafe/jev-latest` |

### Where they're used

| Where | Question asked | What happens with the answer |
|-------|----------------|------------------------------|
| [Hass Guard](plugins/hass-guard), before each Home Assistant action by [Hassonic](hassonic) | Is this action routine and safe to do immediately without asking? (yes/no) | Runs at 85% or higher; otherwise the action is blocked and the agent explains why |

The `decision_evaluate` tool, which lets an agent ask a decision model directly, is not given to any agent.
OpenClaw's experimental *decision assistance*, which uses a decision model to drop unneeded tools before each turn, is off.

## Voice

Octo supports text-to-speech, real-time voice conversation, and speech-to-text.

### Text-to-Speech (TTS)

| Setting | Value |
|---------|-------|
| Provider | `azure-speech` |
| Region | `eastus2` |
| Voice | `en-US-AndrewMultilingualNeural` |
| Language | `en-US` |
| Output format | `mp3_44100_128` |

### Realtime Voice

| Setting | Value |
|---------|-------|
| Provider | `openai` |
| Model | `gpt-live-1-codex` |
| Mode | `realtime` |
| Transport | `gateway-relay` |
| Brain agent | `agent-consult` |
