---
layout: default
title: Plugins
nav_order: 3
has_children: true
---

# Plugins

Plugins are self-contained capabilities that Octo's agents can invoke — sending email, checking restaurant availability, controlling smart home devices, tracking packages, and more. Each plugin is independently developed and declares its own tools, parameters, and dependencies.

Unlike [skills](skills), which provide knowledge through markdown prompts, plugins execute real code and interact with external APIs. Think of plugins as _tools_ and skills as _knowledge_.

Octo currently has **16 plugins** providing **67 tools** in total.

| | Plugin | Description | Tools |
|---|--------|-------------|:-----:|
| 🗄️ | [Config Backup](plugins/config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection | 1 |
| 📧 | [Fastmail](plugins/fastmail) | Send email and manage calendar events in Fastmail | 7 |
| 🐙 | [GitHub](plugins/github) | Manage GitHub issues. Create, read, update, close, comment on, and list issues. | 6 |
| 🏠 | [Home Assistant](plugins/homeassistant) | Control devices, query state, and inspect activity in Home Assistant | 10 |
| 🗓️ | [ICS Calendar](plugins/ics-calendar) | Fetch upcoming events from a published ICS calendar feed | 1 |
| 🖼️ | [LLMVision](plugins/llmvision) | Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events. | 4 |
| 🩺 | [OpenTable Heartbeat](plugins/opentable-heartbeat) | Check whether the OpenTable integration is working and alert on failure | 1 |
| 🍽️ | [OpenTable](plugins/opentable) | Check restaurant availability on OpenTable | 2 |
| 📅 | [Outlook Calendar](plugins/outlook-calendar) | Fetch upcoming events from Outlook personal and family calendars | 1 |
| 📧 | [Outlook Mail](plugins/outlook-mail) | Search and read messages from Outlook inboxes | 4 |
| 📅 | [Outlook Work Calendar](plugins/outlook-work-calendar) | Fetch upcoming events from a published Outlook work calendar | 1 |
| 📦 | [Package Tracking](plugins/package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon | 5 |
| 🎵 | [Spotify](plugins/spotify) | Control Spotify playback, search music, and manage playlists | 9 |
| 📈 | [Stock Quotes](plugins/stock-quotes) | Fetch current stock, ETF, and mutual fund quotes | 2 |
| 📬 | [USPS Mail](plugins/usps-mail) | Analyze USPS Informed Delivery digest emails: parse mailpiece scans, vision-classify, apply rules, write memory, send notifications | 6 |
| 🍽️ | [WeightWatchers](plugins/weightwatchers) | Search foods, log meals, view diary and points budget via the unofficial WW API | 7 |
