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
| `calendar_id` | string | Optional | Configured calendar id from plugin config. |
| `url` | string | Optional | Direct ICS URL override for one-off fetches. |
| `label` | string | Optional | Optional display label when using a direct URL override. |
