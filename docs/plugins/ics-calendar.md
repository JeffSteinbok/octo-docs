---
layout: default
title: ICS Calendar
parent: Plugins
nav_order: 6
---

# 🗓️ ICS Calendar

Fetch upcoming events from a published ICS calendar feed

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar)

## Example config

Set calendars in `plugins.entries["ics-calendar"].config`:

```json
{
  "plugins": {
    "entries": {
      "ics-calendar": {
        "enabled": true,
        "config": {
          "calendars": [
            {
              "id": "personal",
              "label": "Personal",
              "url": "${CALENDAR_PERSONAL_ICS_URL}"
            },
            {
              "id": "family",
              "label": "Family",
              "url": "${CALENDAR_FAMILY_ICS_URL}"
            },
            {
              "id": "travel",
              "label": "Travel",
              "url": "${CALENDAR_TRAVEL_ICS_URL}"
            }
          ]
        }
      }
    }
  }
}
```

Use `${...}` interpolation if you want the actual feed URLs to come from `.env`.

## Configuration Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `calendars` | array<object> | Optional | Configured ICS feeds available by id. |
| `calendars[].id` | string | Required | Stable calendar identifier used by tool calls. |
| `calendars[].label` | string | Optional | Friendly display name used in output. |
| `calendars[].url` | string | Required | Published ICS feed URL. |

## Tools

### `ics_calendar_fetch`

Fetch upcoming events from a published ICS calendar feed.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days` | integer | Optional | Number of days ahead to fetch (default 7). Default: `7`. |
| `calendar_id` | string | Optional | Configured calendar id from plugin config. |
| `url` | string | Optional | Direct ICS URL override for one-off fetches. |
| `label` | string | Optional | Optional display label when using a direct URL override. |
