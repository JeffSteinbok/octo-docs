---
layout: default
title: ICS Calendar
parent: Plugins
nav_order: 6
---

# 🗓️ ICS Calendar

Fetch upcoming events from a published ICS calendar feed

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar)

## Tools

### `ics_calendar_fetch`

Fetch upcoming events from a published ICS calendar feed.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days` | integer | Optional | Number of days ahead to fetch (default 7). Default: `7`. |
| `url` | string | Optional | Direct ICS URL to fetch. |
| `env_var` | string | Optional | Environment variable name holding the ICS URL (e.g. CALENDAR_TRIPIT_ICS_URL). |
| `label` | string | Optional | Display name for this calendar in output (e.g. 'Nicole', 'TripIt', 'Family'). |
