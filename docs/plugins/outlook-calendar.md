---
layout: default
title: Outlook Calendar
parent: Plugins
nav_order: 9
---

# 📅 Outlook Calendar

Fetch upcoming events from Outlook personal and family calendars

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-calendar)

## Tools

### `outlook_calendar_fetch`

Fetch upcoming events from Outlook personal, family, or combined calendars.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `calendar` | string | Optional | Which calendar to fetch: personal, family, or all (default: all). Allowed: `personal`, `family`, `all`. |
| `days` | integer | Optional | Number of days ahead to fetch events for (default: 7). |
