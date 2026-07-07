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
| Primary | `github-copilot/claude-sonnet-4.6` | Default model for all agents |
| Fallback | `github-copilot/gpt-5.4` | Used when primary is unavailable |
| Image (vision) | `github-copilot/claude-sonnet-4.6` | Used for image analysis |
| Image fallback | `github-copilot/gpt-5.5` | |
| Image generation | `google/gemini-3-pro-image-preview` | Used for generating images |

### Registered Aliases

| Alias | Model |
|-------|-------|
| `sonnet` | `github-copilot/claude-sonnet-4.6` |

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
| Model | `gpt-realtime-mini` |
| Mode | `realtime` |
| Transport | `webrtc` |
| Brain agent | `agent-consult` |
