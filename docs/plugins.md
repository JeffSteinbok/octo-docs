---
layout: default
title: Plugins
nav_order: 3
has_children: true
---

# Plugins

This page lists the plugins used by Octo today.

- **Documented here:** 5
- **External docs:** 4

## Plugins documented here

These plugins have docs-safe source in the bundle, so Octo Docs renders full local pages for them.

| | Plugin | Description | Tools | Source |
|---|--------|-------------|:-----:|--------|
|  | [FastMail tools](plugins/fastmail) | Send email and manage calendar events in Fastmail | 7 | [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail) |
|  | [Home Assistant](plugins/homeassistant) | Control devices, query state, and inspect activity in Home Assistant | 11 | [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant) |
|  | [Home Assistant – LLM Vision](plugins/llmvision) | Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events. | 4 | [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision) |
|  | [Package Tracking](plugins/package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon | 5 | [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/package-tracking) |
|  | [Stock Quotes](plugins/stock-quotes) | Fetch current stock, ETF, and mutual fund quotes | 2 | [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/stock-quotes) |

## External plugins in use

These plugins are part of the live runtime, but their detailed docs live elsewhere.

| | Plugin | Description | Docs | Source |
|---|--------|-------------|------|--------|
| 🌐 | [Browser](https://playwright.dev/docs/intro) | Browser automation capability used when the assistant needs to inspect or act on live web pages. | [External docs](https://playwright.dev/docs/intro) | [Built-in](https://playwright.dev/docs/intro) |
| 🤖 | [GitHub Copilot](https://docs.github.com/en/copilot) | Provider integration that lets the instance use GitHub Copilot-hosted models. | [External docs](https://docs.github.com/en/copilot) | [Built-in](https://docs.github.com/en/copilot) |
| 🔎 | [Google](https://ai.google.dev/gemini-api/docs) | Provider integration for Gemini models and Google-powered web search features. | [External docs](https://ai.google.dev/gemini-api/docs) | [Built-in](https://ai.google.dev/gemini-api/docs) |
| 💬 | [Telegram](https://core.telegram.org/bots) | Chat channel plugin used to talk to the live assistant over Telegram. | [External docs](https://core.telegram.org/bots) | [External](https://core.telegram.org/bots) |
