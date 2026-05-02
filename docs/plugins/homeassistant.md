---
layout: default
title: Home Assistant
parent: Plugins
nav_order: 5
---

# 🏠 Home Assistant

Control devices, query state, and inspect activity in Home Assistant

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/homeassistant)

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
          "server": "http://192.168.1.123:8123",
          "token": "your_long_lived_access_token"
        }
      }
    }
  }
}
```
