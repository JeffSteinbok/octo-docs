---
layout: default
title: Plugins
nav_order: 4
---

# Plugins

Plugins add tools and other capabilities to OpenClaw agents, such as reading mail, controlling the house or tracking a package. This page lists the plugins Octo runs and links to each one's documentation. For instruction files that tell agents how to use these tools, see [Skills](skills).

Octo publishes **26 plugins**, grouped by where they come from.


## 🌐 Built-in

Plugins that ship with OpenClaw.

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🔗 | [ACPX Runtime](https://docs.openclaw.ai/tools/acp-agents) | Runs external coding agents over the Agent Client Protocol (ACP); Octo uses it to run Claude Code as the `claude` agent. | [External docs](https://docs.openclaw.ai/tools/acp-agents) |
| 🌐 | [Browser](https://playwright.dev/docs/intro) | Browser automation capability used when the assistant needs to inspect or act on live web pages. | [External docs](https://playwright.dev/docs/intro) |
| 🔎 | [Google](https://ai.google.dev/gemini-api/docs) | Provider integration for Gemini models and Google-powered web search features. | [External docs](https://ai.google.dev/gemini-api/docs) |
| 🧮 | [TypeSafe AI](https://docs.openclaw.ai/plugins/typesafe) | Decision-model provider (TypeSafe's Jev models). Rates whether a Home Assistant action requested through Hassonic is safe to run without asking. | [External docs](https://docs.openclaw.ai/plugins/typesafe) |

## 📦 Open Source

Plugins the owner maintains in public repos ([JeffSteinbok](https://github.com/JeffSteinbok) on GitHub).

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 📧 | [FastMail](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail) | Send email and manage calendar events in FastMail | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail) |
| 📁 | [Filesystem Utilities](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fs-utils) | Core filesystem utility tools for reading, writing, copying, and moving files | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fs-utils) |
| 📊 | [Glances](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances) | Read CPU, memory, disk, and summary metrics from a Glances server | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances) |
| 📚 | [Goodreads](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/goodreads) | Read and manage Goodreads shelves through a headless browser (Goodreads has no public API) | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/goodreads) |
| 🏠 | [Home Assistant](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant) | Control devices, query state, and inspect activity in Home Assistant | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant) |
| 📷 | [Home Assistant – LLM Vision](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision) | Analyze camera images with AI, query the LLM Vision event timeline, and add timeline events, through Home Assistant's LLM Vision integration. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision) |
| 🗓️ | [ICS Calendar](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar) | Fetch upcoming events from a published ICS calendar feed | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar) |
| 📧 | [Microsoft 365](https://github.com/JeffSteinbok/carapace-m365) | Mail, calendar, tasks, and OneDrive tools via Microsoft Graph | [GitHub ↗](https://github.com/JeffSteinbok/carapace-m365) |
| 📓 | [Obsidian Vault](https://github.com/JeffSteinbok/carapace-obsidian) | Read-only search and reading of an Obsidian vault | [GitHub ↗](https://github.com/JeffSteinbok/carapace-obsidian) |
| 🛰️ | [Octo Satellite](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/octo-satellite) | Amazon order and Monarch Money finance tools, served through the Octo Satellite service so the Gateway never holds those passwords. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/octo-satellite) |
| 📅 | [Outlook Work Calendar](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar) | Fetch upcoming events from a published Outlook work calendar | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar) |
| 📦 | [Package Tracking](https://github.com/JeffSteinbok/carapace-package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon | [GitHub ↗](https://github.com/JeffSteinbok/carapace-package-tracking) |
|  | [Reporting](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/reporting) | Turn Markdown into HTML and PDF reports, from a single file or several sections | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/reporting) |
| 📸 | [Screenshot Capture](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/screenshot-capture) | Capture screenshots from paired devices and save them to the Gateway's media store | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/screenshot-capture) |
| 🎵 | [Spotify](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/spotify) | Control Spotify playback, search music, and manage playlists | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/spotify) |
| 📈 | [Stock Quotes](https://github.com/JeffSteinbok/carapace-stock-quotes) | Fetch current stock, ETF, and mutual fund quotes | [GitHub ↗](https://github.com/JeffSteinbok/carapace-stock-quotes) |
| 📬 | [USPS Mail Analyzer](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail) | Read USPS Informed Delivery digest emails: classify each scanned mailpiece, apply rules, note it in memory and send notifications | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail) |
| ❤️ | [Withings](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings) | Fetch health data from Withings devices (weight, body composition, heart rate, sleep, activity) | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings) |

## 🔌 External

Third-party plugins written by other people.

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🍽️ | [restaurant-cli](https://github.com/omarshahine/restaurant-cli) | Pluggable reservation booking via Resy, OpenTable, Tock, and other providers | [GitHub ↗](https://github.com/omarshahine/restaurant-cli) |

## 🔒 Private (octo)

Plugins whose source is private to the `octo` repo, often because they are still under active development. Their docs are published here.

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🗄️ | [Config Backup](plugins/config-backup) | Commits OpenClaw's config and the agent workspaces to Git, only when something has changed. | [Read docs](plugins/config-backup) |
| 🐙 | [GitHub](plugins/github) | Create, read, update, comment on, close and list GitHub issues. | [Read docs](plugins/github) |
| 🛡️ | [Hass Guard](plugins/hass-guard) | Limits the agents behind Hassonic and the Octo MCP (`hassonic` and `external`) to an allowlist of Home Assistant actions, and blocks any action their decision model doesn't rate safe. | [Read docs](plugins/hass-guard) |
