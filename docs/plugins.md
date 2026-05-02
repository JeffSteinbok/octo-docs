---
layout: default
title: Plugins
nav_order: 4
has_children: true
---

# Plugins

This page catalogs the plugins available in Octo today and links to the right documentation for each one.

Octo currently exposes **20 plugins** through its runtime.

## Plugin Catalog

| | Plugin | Description | Docs |
|---|--------|-------------|------|
| 🌐 | [Browser](https://playwright.dev/docs/intro) | Browser automation capability used when the assistant needs to inspect or act on live web pages. | [External docs](https://playwright.dev/docs/intro) |
| 🗄️ | [Config Backup](plugins/config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection | [Read docs](plugins/config-backup) |
| 📧 | [FastMail tools](plugins/fastmail) | Send email and manage calendar events in Fastmail | [Read docs](plugins/fastmail) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail) |
| 🐙 | [GitHub](plugins/github) | Manage GitHub issues. Create, read, update, close, comment on, and list issues. | [Read docs](plugins/github) |
| 🤖 | [GitHub Copilot](https://docs.github.com/en/copilot) | Provider integration that lets the instance use GitHub Copilot-hosted models. | [External docs](https://docs.github.com/en/copilot) |
| 📊 | [Glances](plugins/glances) | Read CPU, memory, disk, and summary metrics from a Glances server | [Read docs](plugins/glances) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances) |
| 🔎 | [Google](https://ai.google.dev/gemini-api/docs) | Provider integration for Gemini models and Google-powered web search features. | [External docs](https://ai.google.dev/gemini-api/docs) |
| 🏠 | [Home Assistant](plugins/homeassistant) | Control devices, query state, and inspect activity in Home Assistant | [Read docs](plugins/homeassistant) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant) |
| 🖼️ | [Home Assistant – LLM Vision](plugins/llmvision) | Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events. | [Read docs](plugins/llmvision) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision) |
| 🗓️ | [ICS Calendar](plugins/ics-calendar) | Fetch upcoming events from a published ICS calendar feed | [Read docs](plugins/ics-calendar) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar) |
| 🍽️ | [OpenTable](plugins/opentable) | Look up restaurants, check availability, and monitor health on OpenTable | [Read docs](plugins/opentable) |
| 📅 | [Outlook Calendar](plugins/outlook-calendar) | Fetch upcoming events from Outlook personal and family calendars | [Read docs](plugins/outlook-calendar) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-calendar) |
| 📧 | [Outlook Mail](plugins/outlook-mail) | Search and read messages from Outlook inboxes | [Read docs](plugins/outlook-mail) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-mail) |
| 📅 | [Outlook Work Calendar](plugins/outlook-work-calendar) | Fetch upcoming events from a published Outlook work calendar | [Read docs](plugins/outlook-work-calendar) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar) |
| 📦 | [Package Tracking](plugins/package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon | [Read docs](plugins/package-tracking) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/package-tracking) |
| 🎵 | [Spotify](plugins/spotify) | Control Spotify playback, search music, and manage playlists | [Read docs](plugins/spotify) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/spotify) |
| 📈 | [Stock Quotes](plugins/stock-quotes) | Fetch current stock, ETF, and mutual fund quotes | [Read docs](plugins/stock-quotes) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/stock-quotes) |
| 📬 | [USPS Mail Analyzer](plugins/usps-mail) | Analyze USPS Informed Delivery digest emails: parse mailpiece scans, vision-classify, apply rules, write memory, send notifications | [Read docs](plugins/usps-mail) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail) |
| 🍽️ | [WeightWatchers](plugins/weightwatchers) | Search foods, log meals, view diary and points budget via the unofficial WW API | [Read docs](plugins/weightwatchers) |
| ❤️ | [Withings](plugins/withings) | Fetch health data from Withings devices (weight, body composition, heart rate, sleep, activity) | [Read docs](plugins/withings) · [Source ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings) |
