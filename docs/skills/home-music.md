---
layout: default
title: Home Music
parent: Skills
nav_order: 1
---

# 🎵 Home Music

Control home speakers and music via the `hass_state_get` and `hass_service_call` plugin tools.

## Key Entities

| Room | Entity ID |
|------|-----------|
| Living Room | `media_player.alexa_living_room` |
| Kitchen | `media_player.alexa_kitchen` |
| Home Theater | `media_player.home_theater` |
| Hallway | `media_player.hallway` |
| Bonus Room | `media_player.bonus_room` |
| Family Room | `media_player.family_room` |
| Main Bedroom | `media_player.main_bedroom` |
| All Speakers | `media_player.all_speakers` |
| Downstairs | `media_player.downstairs_2` |
| Outside | `media_player.alexa_outside` |
| Spotify (Jeff) | `media_player.spotify_jeff_steinbok` |

## Rules

- **Always check current volume before changing it** — use `hass_state_get` first, note the `volume_level` attribute, then set the new value. Report both old and new volume to the user.
- Volume is expressed as a float 0.0–1.0 (e.g. 0.5 = 50%).
- `hass_state_get` now returns full attributes including `volume_level`, `media_title`, `media_artist`.

## Common Operations

### Get current state (volume, track, etc.)
```
hass_state_get(entity_id="media_player.alexa_living_room")
→ check attributes.volume_level, attributes.media_title, attributes.media_artist
```

### Set volume
```
hass_service_call(domain="media_player", service="volume_set",
  entity_id="media_player.alexa_living_room",
  data={"volume_level": 0.4})
```

### Volume up/down (relative)
```
hass_service_call(domain="media_player", service="volume_up", entity_id=...)
hass_service_call(domain="media_player", service="volume_down", entity_id=...)
```

### Mute / unmute
```
hass_service_call(domain="media_player", service="volume_mute",
  entity_id=..., data={"is_volume_muted": true})
```

### Pause / Play / Next / Previous
```
service: media_pause | media_play | media_next_track | media_previous_track
```

### Play a specific playlist or station
```
hass_service_call(domain="media_player", service="play_media",
  entity_id=...,
  data={"media_content_id": "<url or id>", "media_content_type": "music"})
```

## Spotify (future)
Spotify is integrated as `media_player.spotify_jeff_steinbok`. Standard play/pause/skip/volume controls work via the same HA service calls above. Playlist/search support to be added later.

## List All Speaker Volumes

To report speaker status, call `hass_state_get` for each individual room entity (not `all_speakers`) and collect `attributes.volume_level`. **Only report speakers with `state: playing`** — skip idle, unavailable, or off. Present as a list with room name, volume %, and current track/artist.

Entities to query for a full volume report:
- `media_player.alexa_living_room`
- `media_player.alexa_kitchen`
- `media_player.home_theater`
- `media_player.hallway`
- `media_player.bonus_room`
- `media_player.family_room`
- `media_player.main_bedroom`
- `media_player.alexa_outside`

## Room Layout / Zones

| Zone | Rooms | Entities |
|------|-------|----------|
| Downstairs | Living Room, Kitchen, Home Theater | `media_player.alexa_living_room`, `media_player.alexa_kitchen`, `media_player.home_theater` |
| Upstairs | Main Bedroom, Hallway, Bonus Room | `media_player.main_bedroom`, `media_player.hallway`, `media_player.bonus_room` |
| Outside | Outside Speakers | `media_player.alexa_outside` |

When the user says "downstairs", "upstairs", or "outside", apply the command to all entities in that zone. For "everywhere" or "all", use `media_player.all_speakers`.

## Discovery
If unsure which entity to use, run:
```
hass_state_list(domain="media_player")
```
and look for entities with `state: playing` or matching the room name.
