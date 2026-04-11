---
layout: default
title: Outlook Calendar
parent: Plugins
nav_order: 9
---

# 📅 Outlook Calendar

Fetch personal and family calendars via Microsoft Graph API.

### outlook_calendar_fetch

Fetch upcoming events from personal and/or family Outlook calendars via Microsoft Graph API.

| Name     | Type    | Description                                                        |
|----------|---------|--------------------------------------------------------------------|
| calendar | string  | Which calendar to fetch: personal, family, or all (default: all).  |
| days     | integer | Number of days ahead to fetch events for (default: 7).             |
