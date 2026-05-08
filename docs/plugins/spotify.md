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

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/spotify
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/spotify.js --help

## Get the currently playing item on Spotify, including playback details.
node dist/bin/spotify.js spotify-now-playing

## Start or resume Spotify playback. Optionally provide a Spotify URI to play something specific.
node dist/bin/spotify.js spotify-play <uri> <device_id>

## Pause Spotify playback.
node dist/bin/spotify.js spotify-pause <device_id>

## Skip to the next track in the Spotify queue.
node dist/bin/spotify.js spotify-next <device_id>

## Go back to the previous track on Spotify.
node dist/bin/spotify.js spotify-previous <device_id>

## Search Spotify for tracks, albums, artists, or playlists.
node dist/bin/spotify.js spotify-search <query> <type> <limit>

## List the current user's Spotify playlists with IDs and track counts.
node dist/bin/spotify.js spotify-get-playlists <limit>

## List available Spotify Connect devices (speakers, phones, computers) with their IDs and active status.
node dist/bin/spotify.js spotify-get-devices

## Add a track to a Spotify playlist by playlist ID and track URI.
node dist/bin/spotify.js spotify-add-to-playlist <playlist_id> <track_uri>

## JSON output
node dist/bin/spotify.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `SPOTIFY_CLIENT_ID` | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Spotify app client secret |
| `SPOTIFY_REDIRECT_URI` | Spotify OAuth redirect URI |
