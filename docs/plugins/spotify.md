---
layout: default
title: Spotify
nav_order: 15
nav_exclude: true
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

## Tools

### `spotify_now_playing`

Get the currently playing item on Spotify, including playback details.

### `spotify_play`

Start or resume Spotify playback. Optionally provide a Spotify URI to play something specific.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `uri` | string | Optional | Spotify URI to play (e.g. spotify:track:..., spotify:album:..., spotify:playlist:...). Omit to resume current playback. |
| `device_id` | string | Optional | Target device ID. Omit to use the active device. |

### `spotify_pause`

Pause Spotify playback.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `device_id` | string | Optional | Target device ID. Omit to use the active device. |

### `spotify_next`

Skip to the next track in the Spotify queue.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `device_id` | string | Optional | Target device ID. Omit to use the active device. |

### `spotify_previous`

Go back to the previous track on Spotify.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `device_id` | string | Optional | Target device ID. Omit to use the active device. |

### `spotify_search`

Search Spotify for tracks, albums, artists, or playlists.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Required | Search query (e.g. 'Daft Punk Digital Love', 'chill jazz playlist'). |
| `type` | string | Optional | Type of result to search for (default: track). |
| `limit` | integer | Optional | Max number of results to return (default: 10, max: 50). |

### `spotify_get_playlists`

List the current user's Spotify playlists with IDs and track counts.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `limit` | integer | Optional | Max number of playlists to return (default: 20, max: 50). |

### `spotify_get_devices`

List available Spotify Connect devices (speakers, phones, computers) with their IDs and active status.

### `spotify_add_to_playlist`

Add a track to a Spotify playlist by playlist ID and track URI.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playlist_id` | string | Required | Spotify playlist ID (from spotify_get_playlists). |
| `track_uri` | string | Required | Spotify track URI to add (e.g. spotify:track:...). |
