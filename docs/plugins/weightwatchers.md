---
layout: default
title: WeightWatchers
nav_order: 17
nav_exclude: true
---

# 🍽️ WeightWatchers

Search foods, log meals, view diary and points budget via the unofficial WW API

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>jwt</code></td><td>string</td><td>Optional</td><td>WW API JWT token (preferred auth method).</td></tr>
    <tr><td><code>email</code></td><td>string</td><td>Optional</td><td>WW account email used for fallback login.</td></tr>
    <tr><td><code>password</code></td><td>string</td><td>Optional</td><td>WW account password used for fallback login.</td></tr>
    <tr><td><code>tld</code></td><td>string</td><td>Optional</td><td>WW regional TLD (for example `com`). Default: `com`.</td></tr>
  </tbody>
</table>

## Example config

Set WeightWatchers under `plugins.entries["weightwatchers"].config`:

```json
{
  "plugins": {
    "entries": {
      "weightwatchers": {
        "enabled": true,
        "config": {
          "jwt": "${WW_JWT}",
          "email": "${WW_EMAIL}",
          "password": "${WW_PASSWORD}",
          "tld": "${WW_TLD}"
        }
      }
    }
  }
}
```

`jwt` is preferred. `email` and `password` are only needed when the plugin has to log in and refresh auth automatically. If `tld` is omitted, the plugin defaults to `com`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WW_JWT` | No | Backing value for plugin config `jwt |
| `WW_EMAIL` | No | Backing value for plugin config `email |
| `WW_PASSWORD` | No | Backing value for plugin config `password |
| `WW_TLD` | No | Backing value for plugin config `tld |
