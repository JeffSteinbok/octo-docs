---
layout: default
title: Outlook Work Calendar
parent: Plugins
nav_order: 11
---

# 📅 Outlook Work Calendar

Fetch upcoming events from a published Outlook work calendar

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar)

### `outlook_work_calendar_fetch`

Fetch upcoming events from the published Outlook work calendar. Uses the EWS JSON API — no authentication required. Requires the OUTLOOK_WORK_CALENDAR_URL and OUTLOOK_WORK_FOLDER_ID environment variables.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days` | integer | Optional | Number of days ahead to fetch (default 7). Default: `7`. |
