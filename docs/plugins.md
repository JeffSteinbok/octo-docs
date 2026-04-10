---
layout: default
title: Plugins
nav_order: 3
has_children: true
---

# Plugins

Plugins are self-contained capabilities that Octo's agents can invoke — sending email, checking restaurant availability, controlling smart home devices, tracking packages, and more. Each plugin is independently developed and declares its own tools, parameters, and dependencies.

Unlike [skills](skills), which provide knowledge through markdown prompts, plugins execute real code and interact with external APIs. Think of plugins as _tools_ and skills as _knowledge_.

Octo currently has **16 plugins** providing **66 tools** in total.

| | Plugin | Description | Tools |
|---|--------|-------------|:-----:|
| 🗂️ | [Config Backup](plugins/config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection. Only commits and pushes when content has changed. | 1 |
| 📧 | [Fastmail](plugins/fastmail) | Send email, search and read inbox, and manage calendar events via JMAP and CalDAV. | 7 |
| 🐙 | [Github](plugins/github) | Manage GitHub issues. Create, read, update, close, comment on, and list issues. | 6 |
| 🏠 | [Homeassistant](plugins/homeassistant) | Control Home Assistant via REST API: get and list entity states, call services, query logbook, and more. | 10 |
| 🗓️ | [Ics Calendar](plugins/ics-calendar) | Fetches Nicole's calendar from an ICS feed. | 1 |
| 🖼️ | [Llmvision](plugins/llmvision) | Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events. | 3 |
| 🩺 | [Opentable Heartbeat](plugins/opentable-heartbeat) | Health-check for the OpenTable skill. Alerts on failure via configured notification channel. | 1 |
| 🍽️ | [Opentable](plugins/opentable) | Check restaurant availability on OpenTable. | 2 |
| 📅 | [Outlook Calendar](plugins/outlook-calendar) | Fetch personal and family calendars via Microsoft Graph API. | 1 |
| 📧 | [Outlook Mail](plugins/outlook-mail) | Search and read Outlook inbox messages using the Microsoft Graph API. This plugin provides tools to list, search, read, and download attachments from Outlook emails. | 4 |
| 📅 | [Outlook Work Calendar](plugins/outlook-work-calendar) | Fetches published Outlook work calendar via EWS JSON API (no authentication required). | 1 |
| 📦 | [Package Tracking](plugins/package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon using direct carrier URLs. | 5 |
| 🎵 | [Spotify](plugins/spotify) | Control Spotify playback, search music, and manage playlists. | 9 |
| 📈 | [Stock Quotes](plugins/stock-quotes) | Fetch real-time stock, ETF, and mutual fund prices server-side. | 2 |
| 📬 | [Usps Mail](plugins/usps-mail) | Analyze USPS Informed Delivery digest emails by parsing mailpiece scans, performing vision classification, applying importance rules, writing memory, and sending notifications. | 6 |
| 🍽️ | [Weightwatchers](plugins/weightwatchers) | Search foods, log meals, view your diary, and manage your points budget via the unofficial Weightwatchers API. | 7 |
