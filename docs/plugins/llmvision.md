---
layout: default
title: "Home Assistant \u2013 LLM Vision"
nav_order: 7
nav_exclude: true
---

# 📷 Home Assistant – LLM Vision

Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events.

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision)

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

Set credentials in `plugins.entries["llmvision"].config`:

```json
{
  "plugins": {
    "entries": {
      "llmvision": {
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

Uses the same Home Assistant credentials as the homeassistant plugin.

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/llmvision
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/llmvision.js --help

## JSON output
node dist/bin/llmvision.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `LLMVISION_SERVER` | Home Assistant server URL |
| `LLMVISION_TOKEN` | Home Assistant long-lived access token |
