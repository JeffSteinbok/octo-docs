---
layout: default
title: Home Assistant
nav_order: 4
nav_exclude: true
---

# 🏠 Home Assistant

Control devices, query state, and inspect activity in Home Assistant

> **Source:** [JeffSteinbok/openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>server</code></td><td>string</td><td>Optional</td><td>Home Assistant server URL.</td></tr>
    <tr><td><code>token</code></td><td>string</td><td>Optional</td><td>Home Assistant long-lived access token.</td></tr>
  </tbody>
</table>

## Example config

Set credentials in `plugins.entries["homeassistant"].config`:

```json
{
  "plugins": {
    "entries": {
      "homeassistant": {
        "enabled": true,
        "config": {
          "server": "<redacted-private-ip-url>",
          "token": "your_long_lived_access_token"
        }
      }
    }
  }
}
```

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/homeassistant
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/homeassistant.js --help

## JSON output
node dist/bin/homeassistant.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `HOMEASSISTANT_SERVER` | Home Assistant server URL |
| `HOMEASSISTANT_TOKEN` | Home Assistant long-lived access token |
