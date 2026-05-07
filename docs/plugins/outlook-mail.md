---
layout: default
title: Outlook Mail
parent: Plugins
nav_order: 10
---

# 📧 Outlook Mail

Search and read messages from Outlook inboxes

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-mail)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 client secret.</td></tr>
    <tr><td><code>refreshToken</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 refresh token.</td></tr>
  </tbody>
</table>

## Example config

Set Outlook Mail under `plugins.entries["outlook-mail"].config`:

```json
{
  "plugins": {
    "entries": {
      "outlook-mail": {
        "enabled": true,
        "config": {
          "clientId": "${OUTLOOK_CLIENT_ID}",
          "clientSecret": "${OUTLOOK_CLIENT_SECRET}",
          "refreshToken": "${OUTLOOK_REFRESH_TOKEN}"
        }
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OUTLOOK_CLIENT_ID` | No | Backing value for plugin config `clientId |
| `OUTLOOK_CLIENT_SECRET` | No | Backing value for plugin config `clientSecret |
| `OUTLOOK_REFRESH_TOKEN` | No | Backing value for plugin config `refreshToken |
