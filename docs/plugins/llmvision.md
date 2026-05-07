---
layout: default
title: "Home Assistant \u2013 LLM Vision"
parent: Plugins
nav_order: 8
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
          "server": "http://192.168.1.123:8123",
          "token": "your_long_lived_access_token"
        }
      }
    }
  }
}
```

Uses the same Home Assistant credentials as the homeassistant plugin.
