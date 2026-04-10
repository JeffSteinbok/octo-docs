---
layout: default
title: Homeassistant
parent: Plugins
nav_order: 4
---

🏠 Homeassistant

Control Home Assistant via REST API: get and list entity states, call services, query logbook, and more.

### hass_state_get

Get the current state of a Home Assistant entity. Returns attributes, state value, and last-changed timestamp.

| Name      | Type   | Description                                              |
|-----------|--------|----------------------------------------------------------|
| entity_id | string | The entity ID to query (e.g. light.living_room, sensor.temperature). |

### hass_state_list

List all Home Assistant entities, or filter by domain (e.g. light, switch, sensor, camera, person).

| Name   | Type   | Description                                               |
|--------|--------|-----------------------------------------------------------|
| domain | string | Optional domain to filter by (e.g. light, switch, sensor). |

### hass_service_call

Call a Home Assistant service (e.g. turn on a light, activate a scene). Specify domain, service, and optionally an entity_id and extra data.

| Name      | Type   | Description                                                                 |
|-----------|--------|-----------------------------------------------------------------------------|
| domain    | string | Service domain (e.g. light, switch, scene, climate).                         |
| service   | string | Service name (e.g. turn_on, turn_off, toggle).                               |
| entity_id | string | Target entity ID (e.g. light.living_room).                                   |
| data      | object | Additional service data as key-value pairs (e.g. {"brightness": 128}).       |

### hass_event_list

List Home Assistant event types with listener counts.

| Name      | Type   | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| entity_id | string | Optional keyword to filter event types by string match.            |

### hass_person_find

Find a specific person tracked in Home Assistant. Search by the person's name (friendly name) or supply an exact entity_id. Returns the person's current state (home/away/zone) and attributes.

| Name      | Type   | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| name      | string | Name of the person to search for (case-insensitive substring match).|
| entity_id | string | Exact entity ID to look up (e.g. person.john).                     |

### hass_speaker_volume_get

Get the current volume level of one or all speakers (media_player entities). If entity_id is omitted, returns volume info for all media_player entities.

| Name      | Type   | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| entity_id | string | Optional entity ID of the speaker (e.g. media_player.living_room). |

### hass_speaker_volume_set

Set the volume of a speaker (media_player entity). volume_level must be a value between 0.0 (silent) and 1.0 (full volume).

| Name         | Type   | Description                                                        |
|--------------|--------|--------------------------------------------------------------------|
| entity_id    | string | Entity ID of the speaker to adjust (e.g. media_player.living_room).|
| volume_level | number | Desired volume level between 0.0 (silent) and 1.0 (maximum).      |

### hass_camera_list

List all available Home Assistant cameras and their entity IDs.

### hass_camera_snapshot

Take a snapshot from a Home Assistant camera. Saves the image locally and returns the file path. Use camera_name 'all' to capture every camera.

| Name        | Type   | Description                                                                                  |
|-------------|--------|----------------------------------------------------------------------------------------------|
| camera_name | string | Name of the camera to snapshot. One of: living-room, front-doorbell, front-doorbell-package, backyard-right, backyard-left, driveway, family-room, garage, all |

### hass_logbook

Get Home Assistant logbook entries with optional filters. Supports filtering by entity_id, date range (start_time/end_time as ISO strings, or hours for a rolling window), keyword search, and result limit. Useful for 'last time X happened' queries or activity history.

| Name       | Type    | Description                                                                                  |
|------------|---------|----------------------------------------------------------------------------------------------|
| entity_id  | string  | Filter entries for a specific entity (e.g. binary_sensor.front_doorbell_camera_doorbell).     |
| hours      | number  | Rolling window in hours from now (default: 24). Ignored if start_time is provided.            |
| start_time | string  | Start of the time range as an ISO 8601 string (e.g. '2026-04-07T00:00:00+00:00').             |
| end_time   | string  | End of the time range as an ISO 8601 string. Defaults to now.                                 |
| keyword    | string  | Optional keyword to filter entries by name, message, entity_id, or state.                     |
| limit      | integer | Maximum number of entries to return (default: 100, max: 500).                                |
