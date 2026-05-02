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
          "server": "http://192.168.1.76:8123",
          "token": "your_long_lived_access_token"
        }
      }
    }
  }
}
```

## Tools

### `hass_state_get`

Get the current state of a Home Assistant entity.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_id` | string | Required | The entity ID to query (e.g. light.living_room, sensor.temperature). |

### `hass_state_list`

List Home Assistant entities, optionally filtered by domain.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `domain` | string | Optional | Optional domain to filter by (e.g. light, switch, sensor). |

### `hass_service_call`

Call a Home Assistant service.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `domain` | string | Required | Service domain (e.g. light, switch, scene, climate). |
| `service` | string | Required | Service name (e.g. turn_on, turn_off, toggle). |
| `entity_id` | string | Optional | Target entity ID (e.g. light.living_room). |
| `data` | object | Optional | Additional service data as key-value pairs (e.g. {"brightness": 128}). |

### `hass_event_list`

List Home Assistant event types.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_id` | string | Optional | Optional keyword to filter event types by string match. |

### `hass_person_find`

Find a Home Assistant person by name or entity ID.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Optional | Name of the person to search for (case-insensitive substring match). |
| `entity_id` | string | Optional | Exact entity ID to look up (e.g. person.john). |

### `hass_speaker_volume_get`

Get the volume level of one speaker or all speakers.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_id` | string | Optional | Optional entity ID of the speaker (e.g. media_player.living_room). |

### `hass_speaker_volume_set`

Set the volume level of a speaker.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_id` | string | Required | Entity ID of the speaker to adjust (e.g. media_player.living_room). |
| `volume_level` | number | Required | Desired volume level between 0.0 (silent) and 1.0 (maximum). |

### `hass_camera_list`

List available Home Assistant cameras.

### `hass_camera_snapshot`

Take a snapshot from a Home Assistant camera.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `camera_name` | string | Required | Name of the camera to snapshot. One of: living-room, front-doorbell, front-doorbell-package, backyard-right, backyard-left, driveway, family-room, garage, all. |

### `hass_logbook`

Get Home Assistant logbook entries with optional filters.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_id` | string | Optional | Filter entries for a specific entity (e.g. binary_sensor.front_doorbell_camera_doorbell). |
| `hours` | number | Optional | Rolling window in hours from now (default: 24). Ignored if start_time is provided. |
| `start_time` | string | Optional | Start of the time range as an ISO 8601 string (e.g. '2026-04-07T00:00:00+00:00'). |
| `end_time` | string | Optional | End of the time range as an ISO 8601 string. Defaults to now. |
| `keyword` | string | Optional | Optional keyword to filter entries by name, message, entity_id, or state. |
| `limit` | integer | Optional | Maximum number of entries to return (default: 100, max: 500). |

### `hass_camera_collage`

Snapshot multiple cameras simultaneously and compose them into a grid collage image. Defaults to all outdoor + garage cameras. Returns a single local file path to the collage image.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `camera_names` | array | Optional | List of camera names to include. Defaults to all outdoor + garage cameras: front-doorbell, front-doorbell-package, driveway, backyard-left, backyard-right, garage. Available: living-room, front-doorbell, front-doorbell-package, backyard-right, backyard-left, driveway, family-room, garage. |
| `label` | boolean | Optional | Draw camera name labels on each cell (default: true). |
