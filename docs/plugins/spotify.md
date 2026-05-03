---
layout: default
title: Spotify
parent: Plugins
nav_order: 12
---

# 🎵 Spotify

Control Spotify playback, search music, and manage playlists

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/spotify)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Spotify app client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Spotify app client secret.</td></tr>
    <tr><td><code>redirectUri</code></td><td>string</td><td>Optional</td><td>Spotify OAuth redirect URI. Default: `http://127.0.0.1:8888/callback`.</td></tr>
  </tbody>
</table>

## Example config

Set credentials in `plugins.entries["spotify"].config`:

```json
{
  "plugins": {
    "entries": {
      "spotify": {
        "enabled": true,
        "config": {
          "clientId": "your_spotify_client_id",
          "clientSecret": "your_spotify_client_secret",
          "redirectUri": "http://127.0.0.1:8888/callback"
        }
      }
    }
  }
}
```
