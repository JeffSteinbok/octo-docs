---
layout: default
title: Plugins
nav_order: 4
---

# Plugins

This page catalogs the plugins available in Octo today and links to the right documentation for each one.

Octo currently exposes **24 plugins** through its runtime.


## 🌐 Built-in

Core capabilities provided by OpenClaw itself.

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🌐 | [Browser](https://playwright.dev/docs/intro) | Browser automation capability used when the assistant needs to inspect or act on live web pages. | [External docs](https://playwright.dev/docs/intro) |
| 🤖 | [GitHub Copilot](https://docs.github.com/en/copilot) | Provider integration that lets the instance use GitHub Copilot-hosted models. | [External docs](https://docs.github.com/en/copilot) |
| 🔎 | [Google](https://ai.google.dev/gemini-api/docs) | Provider integration for Gemini models and Google-powered web search features. | [External docs](https://ai.google.dev/gemini-api/docs) |

## 📦 Open Source

Open-source plugins maintained by [Jeff](https://github.com/JeffSteinbok).

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 📧 | [FastMail tools](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail) | Send email and manage calendar events in Fastmail | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail) |
| 📊 | [Glances](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances) | Read CPU, memory, disk, and summary metrics from a Glances server | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances) |
| 📚 | [Goodreads](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/goodreads) | Read and manage Goodreads shelves via headless Playwright with anti-403 browser context | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/goodreads) |
| 🏠 | [Home Assistant](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant) | Control devices, query state, and inspect activity in Home Assistant | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant) |
| 📷 | [Home Assistant – LLM Vision](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision) | Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision) |
| 📄 | [HTML to PDF](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/html-to-pdf) | Convert HTML files to PDF using Chromium headless | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/html-to-pdf) |
| 🗓️ | [ICS Calendar](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar) | Fetch upcoming events from a published ICS calendar feed | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar) |
| 📝 | [Markdown to HTML](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/md-to-html) | Convert styled Markdown reports to HTML using a CSS template | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/md-to-html) |
| 📓 | [Obsidian Vault](https://github.com/JeffSteinbok/carapace-obsidian) | Read-only access to an Obsidian vault — search, read, and explore notes securely | [GitHub ↗](https://github.com/JeffSteinbok/carapace-obsidian) |
| 🛰️ | [Octo Satellite](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/octo-satellite) | OpenClaw toolset providing structured access to the Octo Satellite service. Exposes Amazon order management and Monarch Money financial tools. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/octo-satellite) |
| 📧 | [Outlook](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook) | Mail and calendar tools for Outlook via Microsoft Graph | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook) |
| 📅 | [Outlook Work Calendar](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar) | Fetch upcoming events from a published Outlook work calendar | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar) |
| 📦 | [Package Tracking](https://github.com/JeffSteinbok/carapace-package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon | [GitHub ↗](https://github.com/JeffSteinbok/carapace-package-tracking) |
| 📸 | [Screenshot Capture](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/screenshot-capture) | Capture screenshots from paired nodes, write to gateway media store | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/screenshot-capture) |
| 🎵 | [Spotify](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/spotify) | Control Spotify playback, search music, and manage playlists | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/spotify) |
| 📈 | [Stock Quotes](https://github.com/JeffSteinbok/carapace-stock-quotes) | Fetch current stock, ETF, and mutual fund quotes | [GitHub ↗](https://github.com/JeffSteinbok/carapace-stock-quotes) |
| 📬 | [USPS Mail Analyzer](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail) | Analyze USPS Informed Delivery digest emails: parse mailpiece scans, vision-classify, apply rules, write memory, send notifications | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail) |
| ❤️ | [Withings](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings) | Fetch health data from Withings devices (weight, body composition, heart rate, sleep, activity) | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings) |

## 🔌 External

Third-party plugins from outside the project.

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🍽️ | [restaurant-cli](https://github.com/omarshahine/restaurant-cli) | Pluggable reservation booking via Resy, OpenTable, Tock, and other providers | [GitHub ↗](https://github.com/omarshahine/restaurant-cli) |

## 🔒 Private (octo)

Source is private (often under active development), but docs are still available below.

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🗄️ | [Config Backup](plugins/config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection | [Read docs](plugins/config-backup) |
| 🐙 | [GitHub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/github) | Manage GitHub issues. Create, read, update, close, comment on, and list issues. | [External docs](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/github) |
