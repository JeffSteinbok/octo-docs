---
layout: default
title: ICS Calendar
nav_order: 7
nav_exclude: true
---

# 🗓️ ICS Calendar

Fetch upcoming events from a published ICS calendar feed

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/ics-calendar)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>calendars</code></td><td>object[]</td><td>Optional</td><td>Configured ICS feeds available by id.</td></tr>
    <tr><td><code>calendars[].id</code></td><td>string</td><td>Required</td><td>Stable calendar identifier used by tool calls.</td></tr>
    <tr><td><code>calendars[].label</code></td><td>string</td><td>Optional</td><td>Friendly display name used in output.</td></tr>
    <tr><td><code>calendars[].url</code></td><td>string</td><td>Required</td><td>Published ICS feed URL.</td></tr>
  </tbody>
</table>

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

## Tools

### `ics_calendar_fetch`

Fetch upcoming events from a published ICS calendar feed.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `calendar_id` | string | Optional | Configured calendar id from plugin config. |
| `url` | string | Optional | Direct ICS URL override for one-off fetches. |
| `label` | string | Optional | Optional display label when using a direct URL override. |
| `days` | integer | Optional | Number of days ahead to fetch (default 7). Default: `7`. |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/ics-calendar
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/ics-calendar.js --help

## Fetch upcoming events from a published ICS calendar feed.
node dist/bin/ics-calendar.js ics-calendar-fetch <calendar_id> <url> <label> <days>

## JSON output
node dist/bin/ics-calendar.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `ICS_CALENDAR_CALENDARS` | Configured ICS feeds available by id |
