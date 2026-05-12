---
layout: default
title: Outlook Calendar
nav_order: 10
nav_exclude: true
---

# 📅 Outlook Calendar

Fetch upcoming events from Outlook personal and family calendars

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-calendar)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 client secret.</td></tr>
    <tr><td><code>refreshToken</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 refresh token.</td></tr>
    <tr><td><code>personalCalendarNames</code></td><td>string[]</td><td>Optional</td><td>Optional additional Outlook calendar names to try before the built-in personal defaults.</td></tr>
    <tr><td><code>familyCalendarNames</code></td><td>string[]</td><td>Optional</td><td>Optional additional Outlook calendar names to try before the built-in family defaults.</td></tr>
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

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OUTLOOK_CLIENT_ID` | No | Backing value for plugin config `clientId |
| `OUTLOOK_CLIENT_SECRET` | No | Backing value for plugin config `clientSecret |
| `OUTLOOK_REFRESH_TOKEN` | No | Backing value for plugin config `refreshToken |
| `OUTLOOK_PERSONAL_CALENDAR_NAMES` | No | Backing value for plugin config `personalCalendarNames` as a comma-separated list |
| `OUTLOOK_FAMILY_CALENDAR_NAMES` | No | Backing value for plugin config `familyCalendarNames` as a comma-separated list |

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

## JSON output
node dist/bin/outlook-calendar.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `OUTLOOK_CALENDAR_CLIENT_ID` | Microsoft Graph OAuth2 client ID |
| `OUTLOOK_CALENDAR_CLIENT_SECRET` | Microsoft Graph OAuth2 client secret |
| `OUTLOOK_CALENDAR_REFRESH_TOKEN` | Microsoft Graph OAuth2 refresh token |
| `OUTLOOK_CALENDAR_PERSONAL_CALENDAR_NAMES` | Optional additional Outlook calendar names to try before the built-in personal defaults |
| `OUTLOOK_CALENDAR_FAMILY_CALENDAR_NAMES` | Optional additional Outlook calendar names to try before the built-in family defaults |
