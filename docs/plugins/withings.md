---
layout: default
title: Withings
parent: Plugins
nav_order: 18
nav_exclude: true
---

# Withings

Fetch health data from Withings devices (weight, body composition, heart rate, sleep, activity)

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Withings OAuth2 App Client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Withings OAuth2 App Client Secret (use env var WITHINGS_CLIENT_SECRET).</td></tr>
    <tr><td><code>redirectUri</code></td><td>string</td><td>Optional</td><td>OAuth redirect URI registered with the Withings developer app.</td></tr>
  </tbody>
</table>

## Example config

Set Withings under `plugins.entries["withings"].config`:

```json
{
  "plugins": {
    "entries": {
      "withings": {
        "enabled": true,
        "config": {
          "clientId": "${WITHINGS_CLIENT_ID}",
          "clientSecret": "${WITHINGS_CLIENT_SECRET}",
          "redirectUri": "${WITHINGS_REDIRECT_URI}"
        }
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WITHINGS_CLIENT_ID` | No | Backing value for plugin config `clientId |
| `WITHINGS_CLIENT_SECRET` | No | Backing value for plugin config `clientSecret |
| `WITHINGS_REDIRECT_URI` | No | Backing value for plugin config `redirectUri |
