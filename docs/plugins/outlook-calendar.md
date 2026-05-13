---
layout: default
title: outlook-calendar
nav_order: 11
nav_exclude: true
---

# 📅 outlook-calendar

Fetch upcoming events from Outlook personal and family calendars

> **Source:** [JeffSteinbok/openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-calendar)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Microsoft OAuth client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Microsoft OAuth client secret.</td></tr>
    <tr><td><code>refreshToken</code></td><td>string</td><td>Optional</td><td>Microsoft OAuth refresh token.</td></tr>
  </tbody>
</table>

## Example config

Set Outlook Calendar under `plugins.entries["outlook-calendar"].config`:

```json
{
  "plugins": {
    "entries": {
      "outlook-calendar": {
        "enabled": true,
        "config": {
          "clientId": "${OUTLOOK_CLIENT_ID}",
          "clientSecret": "${OUTLOOK_CLIENT_SECRET}",
          "refreshToken": "${OUTLOOK_REFRESH_TOKEN}",
          "personalCalendarNames": ["calendar", "personal"],
          "familyCalendarNames": ["family v2", "family"]
        }
      }
    }
  }
}
```

The calendar-name arrays are optional overrides. If omitted, the plugin uses its built-in personal/family defaults.

## Tools

### `outlook_calendar_fetch`

Fetch upcoming events from Outlook personal, family, or combined calendars.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `calendar` | string | Optional | Which calendar to fetch: personal, family, or all (default: all). |
| `days` | integer | Optional | Number of days ahead to fetch events for (default: 7). |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/outlook-calendar
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/outlook-calendar.js --help

## Fetch upcoming events from Outlook personal, family, or combined calendars.
node dist/bin/outlook-calendar.js outlook-calendar-fetch <calendar> <days>

## JSON output
node dist/bin/outlook-calendar.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `OUTLOOK_CALENDAR_CLIENT_ID` | Microsoft OAuth client ID |
| `OUTLOOK_CALENDAR_CLIENT_SECRET` | Microsoft OAuth client secret |
| `OUTLOOK_CALENDAR_REFRESH_TOKEN` | Microsoft OAuth refresh token |
