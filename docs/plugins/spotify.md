---
layout: default
title: Spotify
parent: Plugins
nav_order: 13
---

🎵 Spotify

Control Spotify playback, search music, and manage playlists.

### spotify_now_playing

Get the currently playing track on Spotify, including artist, album, and playback device.

### spotify_play

Start or resume Spotify playback. Optionally provide a Spotify URI (track, album, artist, or playlist) to play something specific.

| Name      | Type   | Description                                                                                  |
|-----------|--------|----------------------------------------------------------------------------------------------|
| uri       | string | Spotify URI to play (e.g. spotify:track:..., spotify:album:..., spotify:playlist:...). Omit to resume current playback. |
| device_id | string | Target device ID (from spotify_get_devices). Omit to use the active device.                  |

### spotify_pause

Pause Spotify playback.

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| device_id | string | Target device ID. Omit to use the active device. |

### spotify_next

Skip to the next track in the Spotify queue.

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| device_id | string | Target device ID. Omit to use the active device. |

### spotify_previous

Go back to the previous track on Spotify.

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| device_id | string | Target device ID. Omit to use the active device. |

### spotify_search

Search Spotify for tracks, albums, artists, or playlists. Returns names, URIs, and metadata for use with other Spotify tools.

| Name   | Type    | Description                                                                                  |
|--------|---------|----------------------------------------------------------------------------------------------|
| query  | string  | Search query (e.g. 'Daft Punk Digital Love', 'chill jazz playlist').                         |
| type   | string  | Type of result to search for (default: track).                                               |
| limit  | integer | Max number of results to return (default: 10, max: 50).                                      |

### spotify_add_to_playlist

Add a track to a Spotify playlist by playlist ID and track URI.

| Name        | Type   | Description                                              |
|-------------|--------|----------------------------------------------------------|
| playlist_id | string | Spotify playlist ID (from spotify_get_playlists).        |
| track_uri   | string | Spotify track URI to add (e.g. spotify:track:...).       |

### spotify_get_playlists

List the current user's Spotify playlists with IDs and track counts.

| Name   | Type    | Description                                         |
|--------|---------|-----------------------------------------------------|
| limit  | integer | Max number of playlists to return (default: 20, max: 50). |

### spotify_get_devices

List available Spotify Connect devices (speakers, phones, computers) with their IDs and active status.
