---
layout: default
title: Plugins
nav_order: 3
---

# Plugins

- 🛠️ [Config Backup](#config-backup): Backs up OpenClaw config to Git with SHA-256 change detection.
- 📧 [FastMail](#fastmail): Send email, search/read inbox, manage calendar events via JMAP and CalDAV.
- 🐙 [GitHub](#github): Create issues in GitHub repositories as the OpenClaw user.
- 📷 [Home Assistant Camera Snapshot](#hass-camera-snapshot): Take snapshots from Home Assistant cameras via hass-cli and save locally.
- 🏠 [Home Assistant CLI](#homeassistant-cli): Control Home Assistant via hass-cli: get/list entity states, call services, and list events.
- 📅 [ICS Calendar](#ics-calendar): Fetches Nicole's calendar from an ICS feed.
- 🍽️ [OpenTable](#opentable): Check restaurant availability on OpenTable.
- ❤️ [OpenTable Heartbeat](#opentable-heartbeat): Health-check for the OpenTable skill. Alerts on failure via configured notification channel.
- 📅 [Outlook Calendar](#outlook-calendar): Fetch personal and family calendars via Microsoft Graph API.
- 📧 [Outlook Mail](#outlook-mail): Search and read Outlook inbox via Microsoft Graph API.
- 🏢 [Outlook Work Calendar](#outlook-work-calendar): Fetches published Outlook work calendar via EWS JSON API (no auth required).
- 🎵 [Spotify](#spotify): Control Spotify playback, search music, and manage playlists.
- 🍎 [WeightWatchers](#weightwatchers): Search foods, log meals, view diary and points budget via the unofficial WW API.

---

<a id="config-backup"></a>

## 🛠️ Config Backup

### Tools

#### config_backup_run
Back up OpenClaw config and agent workspace to Git. Copies `~/.openclaw` config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| force      | boolean | Force backup even if no changes detected      |
| check_only | boolean | Only check for changes without committing     |
| verbose    | boolean | Include verbose diagnostic output             |

---

<a id="fastmail"></a>

## 📧 FastMail

### Tools

#### fastmail_send
Send a plain-text email via Fastmail JMAP, with optional file attachments.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| to         | string  | Recipient email address(es)                  |
| cc         | array   | CC recipient email address(es)               |
| subject    | string  | Email subject line                           |
| body       | string  | Plain-text email body                        |
| signature  | string  | Signature block appended after body          |
| attachment | array   | File path(s) to attach                       |

#### fastmail_search
Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| account_id | string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| query      | string  | Full-text search query                       |
| from       | string  | Filter by sender email or domain             |
| to         | string  | Filter by recipient                          |
| subject    | string  | Filter by subject text                       |
| since      | string  | Emails after this date (YYYY-MM-DD)          |
| before     | string  | Emails before this date (YYYY-MM-DD)         |
| limit      | integer | Max results (default 20)                     |

#### fastmail_read
Read a specific email by its JMAP email ID, returning full headers and body text.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| account_id | string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| id         | string  | JMAP email ID to read                        |

#### fastmail_inbox
Show recent emails from the Fastmail inbox, optionally filtered to unread only.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| account_id | string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| limit      | integer | Max emails to show (default 10)              |
| unread     | boolean | Only show unread emails                      |

#### fastmail_meeting
Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| to         | string  | Attendee email address(es)                   |
| cc         | array   | CC recipient email address(es)               |
| subject    | string  | Meeting title                                |
| start      | string  | Start datetime in ISO format (e.g. 2026-03-15T14:00) |
| duration   | string  | Duration: '1h', '30m', '1.5h' (default: 1h)  |
| location   | string  | Meeting location                             |
| description| string  | Meeting description / agenda                 |
| timezone   | string  | IANA timezone (default: America/Los_Angeles) |
| signature  | string  | Signature block for the invite email         |

#### fastmail_update_event
Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name           | Type    | Description                                   |
|----------------|---------|-----------------------------------------------|
| uid            | string  | Exact event UID to target                    |
| find           | string  | Free-text search across event title/description |
| new_title      | string  | Replace the event title                      |
| new_start      | string  | New start time (ISO format)                  |
| new_duration   | string  | New duration (e.g. '1h', '30m')              |
| new_location   | string  | Replace location                             |
| new_description| string  | Replace description/notes                    |
| timezone       | string  | Timezone for --new-start (default: America/Los_Angeles) |
| status         | string  | Update event status                          |
| add_attendee   | array   | Email(s) to add as attendees                 |
| remove_attendee| array   | Email(s) to remove from attendees            |
| no_notify      | boolean | Skip iMIP update notifications               |
| force          | boolean | Update all matching events when multiple found |

#### fastmail_query_events
Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| after      | string  | Only events starting at or after this date (ISO, e.g. 2026-03-01) |
| before     | string  | Only events starting before this date (ISO, e.g. 2026-04-01) |
| text       | string  | Filter by text match on title/description     |
| attendee   | string  | Filter to events including this attendee email |
| uid        | string  | Return the single event with this exact UID   |

---

<a id="github"></a>

## 🐙 GitHub

### Tools

#### github_create_issue
Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| owner      | string  | Repository owner (user or organisation name) |
| repo       | string  | Repository name                              |
| title      | string  | Issue title                                  |
| body       | string  | Issue body (Markdown supported). Defaults to empty string. |
| labels     | array   | Labels to apply to the issue (must already exist in the repo) |
| assignees  | array   | GitHub usernames to assign the issue to       |
| milestone  | integer | Milestone number to associate with the issue |

---

<a id="hass-camera-snapshot"></a>

## 📷 Home Assistant Camera Snapshot

### Tools

#### hass_camera_snapshot
Take a snapshot from a Home Assistant camera. Saves the image locally and returns the file path. Use `camera_name` 'all' to capture every camera.

| Name        | Type    | Description                                   |
|-------------|---------|-----------------------------------------------|
| camera_name | string  | Name of the camera to snapshot. One of: living-room, front-doorbell, front-doorbell-package, backyard-right, backyard-left, driveway, family-room, garage, all |

#### hass_camera_list
List all available Home Assistant cameras and their entity IDs.

---

<a id="homeassistant-cli"></a>

## 🏠 Home Assistant CLI

### Tools

#### ha_state_get
Get the current state of a Home Assistant entity. Returns attributes, state value, and last-changed timestamp.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| entity_id | string  | The entity ID to query (e.g. light.living_room, sensor.temperature). |

#### ha_state_list
List all Home Assistant entities, or filter by domain (e.g. light, switch, sensor, camera, person).

| Name   | Type    | Description                                   |
|--------|---------|-----------------------------------------------|
| domain | string  | Optional domain to filter by (e.g. light, switch, sensor). |

#### ha_service_call
Call a Home Assistant service (e.g. turn on a light, activate a scene). Specify domain, service, and optionally an `entity_id` and extra data.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| domain    | string  | Service domain (e.g. light, switch, scene, climate). |
| service   | string  | Service name (e.g. turn_on, turn_off, toggle). |
| entity_id | string  | Target entity ID (e.g. light.living_room).    |
| data      | object  | Additional service data as key-value pairs (e.g. {"brightness": 128}). |

#### ha_event_list
List recent Home Assistant events, optionally filtered by `entity_id`.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| entity_id | string  | Optional entity ID to filter events for.      |

#### ha_person_find
Find a specific person tracked in Home Assistant. Search by the person's name (friendly name) or supply an exact `entity_id`. Returns the person's current state (home/away/zone) and attributes.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| name      | string  | Name of the person to search for (case-insensitive substring match). |
| entity_id | string  | Exact entity ID to look up (e.g. person.john). |

#### ha_speaker_volume_get
Get the current volume level of one or all speakers (media_player entities). If `entity_id` is omitted, returns volume info for all media_player entities.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| entity_id | string  | Optional entity ID of the speaker (e.g. media_player.living_room). |

#### ha_speaker_volume_set
Set the volume of a speaker (media_player entity). `volume_level` must be a value between 0.0 (silent) and 1.0 (full volume).

| Name         | Type    | Description                                   |
|--------------|---------|-----------------------------------------------|
| entity_id    | string  | Entity ID of the speaker to adjust (e.g. media_player.living_room). |
| volume_level | number  | Desired volume level between 0.0 (silent) and 1.0 (maximum). |

---

<a id="ics-calendar"></a>

## 📅 ICS Calendar

### Tools

#### ics_calendar_fetch
Fetch upcoming events from Nicole's ICS calendar feed. Requires the `CALENDAR_NICOLE_ICS_URL` environment variable.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| days  | integer | Number of days ahead to fetch (default 7)     |

---

<a id="opentable"></a>

## 🍽️ OpenTable

### Tools

#### opentable_lookup
Look up an OpenTable restaurant by its URL slug (e.g. 'carbone-new-york' from opentable.com/r/carbone-new-york) to get its numeric restaurant ID.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| slug  | string  | Restaurant URL slug from opentable.com/r/<slug> |

#### opentable_availability
Check real-time availability for a restaurant on OpenTable. Returns available time slots with booking URLs.

| Name          | Type    | Description                                   |
|---------------|---------|-----------------------------------------------|
| restaurant_id | integer | Numeric restaurant ID (from opentable_lookup) |
| date          | string  | Date in YYYY-MM-DD format                     |
| party_size    | integer | Number of guests (default: 2)                 |
| time          | string  | Preferred time in HH:MM format (default: 19:00) |

---

<a id="opentable-heartbeat"></a>

## ❤️ OpenTable Heartbeat

### Tools

#### opentable_heartbeat_check
Run OpenTable health check. Returns status (`ok` or `error`) and a message.

---

<a id="outlook-calendar"></a>

## 📅 Outlook Calendar

### Tools

#### outlook_calendar_fetch
Fetch upcoming events from personal and/or family Outlook calendars via Microsoft Graph API.

| Name     | Type    | Description                                   |
|----------|---------|-----------------------------------------------|
| calendar | string  | Which calendar to fetch: personal, family, or all (default: all). |
| days     | integer | Number of days ahead to fetch events for (default: 7). |

---

<a id="outlook-mail"></a>

## 📧 Outlook Mail

### Tools

#### outlook_inbox
List recent messages from the Outlook inbox.

| Name   | Type    | Description                                   |
|--------|---------|-----------------------------------------------|
| limit  | integer | Maximum number of messages to return (default 10). |
| unread | boolean | If true, return only unread messages.         |

#### outlook_search
Search Outlook messages by query text, sender, subject, or date range.

| Name   | Type    | Description                                   |
|--------|---------|-----------------------------------------------|
| query  | string  | Full-text search across subject and body.     |
| from   | string  | Filter by sender email address.               |
| subject| string  | Filter by subject (substring match).          |
| since  | string  | Only messages received on or after this date (YYYY-MM-DD). |
| before | string  | Only messages received on or before this date (YYYY-MM-DD). |
| limit  | integer | Maximum number of results (default 10).       |

#### outlook_read
Read a specific Outlook message by its ID, including full body content.

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| message_id | string  | The Microsoft Graph message ID to retrieve.  |

---

<a id="outlook-work-calendar"></a>

## 🏢 Outlook Work Calendar

### Tools

#### outlook_work_calendar_fetch
Fetch upcoming events from the published Outlook work calendar. Uses the EWS JSON API — no authentication required. Requires the `OUTLOOK_WORK_CALENDAR_URL` environment variable.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| days  | integer | Number of days ahead to fetch (default 7)     |

---

<a id="spotify"></a>

## 🎵 Spotify

### Tools

#### spotify_now_playing
Get the currently playing track on Spotify, including artist, album, and playback device.

#### spotify_play
Start or resume Spotify playback. Optionally provide a Spotify URI (track, album, artist, or playlist) to play something specific.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| uri       | string  | Spotify URI to play (e.g. spotify:track:..., spotify:album:..., spotify:playlist:...). Omit to resume current playback. |
| device_id | string  | Target device ID (from spotify_get_devices). Omit to use the active device. |

#### spotify_pause
Pause Spotify playback.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| device_id | string  | Target device ID. Omit to use the active device. |

#### spotify_next
Skip to the next track in the Spotify queue.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| device_id | string  | Target device ID. Omit to use the active device. |

#### spotify_previous
Go back to the previous track on Spotify.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| device_id | string  | Target device ID. Omit to use the active device. |

#### spotify_search
Search Spotify for tracks, albums, artists, or playlists. Returns names, URIs, and metadata for use with other Spotify tools.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| query | string  | Search query (e.g. 'Daft Punk Digital Love', 'chill jazz playlist'). |
| type  | string  | Type of result to search for (default: track). |
| limit | integer | Max number of results to return (default: 10, max: 50). |

#### spotify_add_to_playlist
Add a track to a Spotify playlist by playlist ID and track URI.

| Name         | Type    | Description                                   |
|--------------|---------|-----------------------------------------------|
| playlist_id  | string  | Spotify playlist ID (from spotify_get_playlists). |
| track_uri    | string  | Spotify track URI to add (e.g. spotify:track:...). |

#### spotify_get_playlists
List the current user's Spotify playlists with IDs and track counts.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| limit | integer | Max number of playlists to return (default: 20, max: 50). |

#### spotify_get_devices
List available Spotify Connect devices (speakers, phones, computers) with their IDs and active status.

---

<a id="weightwatchers"></a>

## 🍎 WeightWatchers

### Tools

#### ww_daily
Get daily WW food diary. Returns tracked meals and points summary.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| date  | string  | Date in YYYY-MM-DD format (default: today)    |

#### ww_search
Search the WW food database. Returns food IDs, points, and portion options needed for logging.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| query | string  | Food search query (e.g. 'grilled chicken breast') |
| limit | integer | Max results to return (default: 10)           |

#### ww_log
Log a food item to the WW diary. Requires `food_id`, `version_id`, and `portion_id` from `ww_search` results.

| Name         | Type    | Description                                   |
|--------------|---------|-----------------------------------------------|
| food_id      | string  | WW food ID (from ww_search results)           |
| portion_id   | string  | Portion ID (from ww_search results)           |
| version_id   | string  | Food version ID (from ww_search results)      |
| portion_size | number  | Portion multiplier (default: 1.0)             |
| date         | string  | Date in YYYY-MM-DD format (default: today)    |
| meal_type    | string  | Meal slot to log to (default: snacks)         |
| source_type  | string  | Food source type: WWFOOD, WWRECIPE, MEMBERFOOD, etc. (default: WWFOOD) |

#### ww_points
Calculate WW SmartPoints offline from nutrition data. No authentication required.

| Name           | Type    | Description                                   |
|----------------|---------|-----------------------------------------------|
| calories       | number  | Total calories                               |
| saturated_fat  | number  | Saturated fat in grams                       |
| sugar          | number  | Sugar in grams                               |
| protein        | number  | Protein in grams                             |

#### ww_budget
Get remaining WW points budget for a date. Shows daily and weekly allowances.

| Name  | Type    | Description                                   |
|-------|---------|-----------------------------------------------|
| date  | string  | Date in YYYY-MM-DD format (default: today)    |

#### ww_quick_add
Quick-add a points value to the WW diary without specifying a food item. Useful when you know the points but not the exact food.

| Name      | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| points    | integer | Number of SmartPoints to add                 |
| name      | string  | Label for the diary entry (default: 'Quick Add') |
| meal_type | string  | Meal slot to log to (default: snacks)         |
| date      | string  | Date in YYYY-MM-DD format (default: today)    |

#### ww_delete
Delete a tracked food entry from the WW diary by its tracking ID. Use `ww_daily` to get tracking IDs.

| Name        | Type    | Description                                   |
|-------------|---------|-----------------------------------------------|
| tracking_id | string  | Tracking ID of the diary entry to delete (from ww_daily results) |
| date        | string  | Date of the entry in YYYY-MM-DD format (default: today) |
