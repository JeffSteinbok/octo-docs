---
layout: default
title: Outlook Work Calendar
parent: Plugins
nav_order: 11
---

# 📅 Outlook Work Calendar

Fetches published Outlook work calendar via EWS JSON API (no authentication required).

### outlook_work_calendar_fetch

Fetch upcoming events from the published Outlook work calendar. Uses the EWS JSON API — no authentication required. Requires the OUTLOOK_WORK_CALENDAR_URL environment variable.

| Name  | Type    | Description                           |
|-------|---------|---------------------------------------|
| days  | integer | Number of days ahead to fetch (default 7) |
