---
layout: default
title: Outlook Work Calendar
nav_order: 12
nav_exclude: true
---

# 📅 Outlook Work Calendar

Fetch upcoming events from a published Outlook work calendar

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-work-calendar)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>url</code></td><td>string</td><td>Optional</td><td>Published Outlook work calendar base URL.</td></tr>
    <tr><td><code>folderId</code></td><td>string</td><td>Optional</td><td>EWS folder identifier for the published calendar.</td></tr>
  </tbody>
</table>

## Example config

Set Outlook Work Calendar under `plugins.entries["outlook-work-calendar"].config`:

```json
{
  "plugins": {
    "entries": {
      "outlook-work-calendar": {
        "enabled": true,
        "config": {
          "url": "${OUTLOOK_WORK_CALENDAR_URL}",
          "folderId": "${OUTLOOK_WORK_FOLDER_ID}"
        }
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OUTLOOK_WORK_CALENDAR_URL` | No | Backing value for plugin config `url |
| `OUTLOOK_WORK_FOLDER_ID` | No | Backing value for plugin config `folderId |
