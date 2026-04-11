---
layout: default
title: Ics Calendar
parent: Plugins
nav_order: 5
---

# 🗓️ Ics Calendar

Fetches Nicole's calendar from an ICS feed.

### ics_calendar_fetch

Fetch upcoming events from an ICS calendar feed. Specify a calendar by passing either a direct `url`, or an `env_var` name that holds the ICS URL (e.g. CALENDAR_NICOLE_ICS_URL, CALENDAR_TRIPIT_ICS_URL, CALENDAR_FAMILY_ICS_URL, CALENDAR_PERSONAL_ICS_URL). If neither is provided, defaults to CALENDAR_NICOLE_ICS_URL. The `label` parameter sets the calendar name shown in the output.

| Name    | Type     | Description                                                                                   |
|---------|----------|-----------------------------------------------------------------------------------------------|
| days    | integer  | Number of days ahead to fetch (default 7)                                                     |
| url     | string   | Direct ICS URL to fetch                                                                       |
| env_var | string   | Environment variable name holding the ICS URL (e.g. CALENDAR_TRIPIT_ICS_URL)                  |
| label   | string   | Display name for this calendar in output (e.g. 'Nicole', 'TripIt', 'Family')                  |
