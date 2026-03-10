---
layout: default
title: Plugins
nav_order: 3
---

# Plugins

| Emoji | Plugin Name | Description | Tool Count |
|-------|-------------|-------------|------------|
| 🛠️ | [Config Backup](#config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection | 1 |
| 📧 | [FastMail](#fastmail) | Send email, search/read inbox, manage calendar events via JMAP and CalDAV | 7 |
| 🐙 | [GitHub](#github) | Create issues in GitHub repositories as the OpenClaw user | 1 |
| 📷 | [Home Assistant Camera Snapshot](#hass-camera-snapshot) | Take snapshots from Home Assistant cameras via hass-cli and save locally | 2 |
| 🏠 | [Home Assistant CLI](#homeassistant-cli) | Control Home Assistant via hass-cli: get/list entity states, call services, and list events | 7 |
| 📅 | [ICS Calendar](#ics-calendar) | Fetches Nicole's calendar from an ICS feed | 1 |
| 🍽️ | [OpenTable](#opentable) | Check restaurant availability on OpenTable | 2 |
| ❤️ | [OpenTable Heartbeat](#opentable-heartbeat) | Health-check for the OpenTable skill | 1 |
| 📅 | [Outlook Calendar](#outlook-calendar) | Fetch personal and family calendars via Microsoft Graph API | 1 |
| 📧 | [Outlook Mail](#outlook-mail) | Search and read Outlook inbox via Microsoft Graph API | 3 |
| 🏢 | [Outlook Work Calendar](#outlook-work-calendar) | Fetches published Outlook work calendar via EWS JSON API (no auth required) | 1 |
| 🎵 | [Spotify](#spotify) | Control Spotify playback, search music, and manage playlists | 9 |
| 🍎 | [WeightWatchers](#weightwatchers) | Search foods, log meals, view diary and points budget via the unofficial WW API | 7 |

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

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| to         | string  | Recipient email address(es)           |
| cc         | array   | CC recipient email address(es)        |
| subject    | string  | Email subject line                    |
| body       | string  | Plain-text email body                 |
| signature  | string  | Signature block appended after body   |
| attachment | array   | File path(s) to attach               |

#### fastmail_search
Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| account_id | string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| query      | string  | Full-text search query               |
| from       | string  | Filter by sender email or domain     |
| to         | string  | Filter by recipient                  |
| subject    | string  | Filter by subject text               |
| since      | string  | Emails after this date (YYYY-MM-DD)  |
| before     | string  | Emails before this date (YYYY-MM-DD) |
| limit      | integer | Max results (default 20)             |

#### fastmail_read
Read a specific email by its JMAP email ID, returning full headers and body text.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| account_id | string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| id         | string  | JMAP email ID to read                |

#### fastmail_inbox
Show recent emails from the Fastmail inbox, optionally filtered to unread only.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| account_id | string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| limit      | integer | Max emails to show (default 10)       |
| unread     | boolean | Only show unread emails              |

#### fastmail_meeting
Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| to         | string  | Attendee email address(es)           |
| cc         | array   | CC recipient email address(es)        |
| subject    | string  | Meeting title                        |
| start      | string  | Start datetime in ISO format         |
| duration   | string  | Duration: '1h', '30m', '1.5h'        |
| location   | string  | Meeting location                     |
| description| string  | Meeting description / agenda         |
| timezone   | string  | IANA timezone                        |
| signature  | string  | Signature block for the invite email |

#### fastmail_update_event
Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name           | Type    | Description                           |
|----------------|---------|---------------------------------------|
| uid            | string  | Exact event UID to target            |
| find           | string  | Free-text search across event title/description |
| new_title      | string  | Replace the event title              |
| new_start      | string  | New start time (ISO format)          |
| new_duration   | string  | New duration                         |
| new_location   | string  | Replace location                     |
| new_description| string  | Replace description/notes            |
| timezone       | string  | Timezone for --new-start             |
| status         | string  | Update event status                  |
| add_attendee   | array   | Email(s) to add as attendees         |
| remove_attendee| array   | Email(s) to remove from attendees    |
| no_notify      | boolean | Skip iMIP update notifications       |
| force          | boolean | Update all matching events when multiple found |

#### fastmail_query_events
Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| after      | string  | Only events starting at or after this date |
| before     | string  | Only events starting before this date |
| text       | string  | Filter by text match on title/description |
| attendee   | string  | Filter to events including this attendee email |
| uid        | string  | Return the single event with this exact UID |

---

<a id="github"></a>

## 🐙 GitHub

### Tools

#### github_create_issue
Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| owner      | string  | Repository owner                     |
| repo       | string  | Repository name                      |
| title      | string  | Issue title                          |
| body       | string  | Issue body (Markdown supported)      |
| labels     | array   | Labels to apply to the issue         |
| assignees  | array   | GitHub usernames to assign the issue to |
| milestone  | integer | Milestone number to associate with the issue |

---

<a id="hass-camera-snapshot"></a>

## 📷 Home Assistant Camera Snapshot

### Tools

#### hass_camera_snapshot
Take a snapshot from a Home Assistant camera. Saves the image locally and returns the file path. Use `camera_name` 'all' to capture every camera.

| Name        | Type    | Description                           |
|-------------|---------|---------------------------------------|
| camera_name | string  | Name of the camera to snapshot        |

#### hass_camera_list
List all available Home Assistant cameras and their entity IDs.

---

<a id="homeassistant-cli"></a>

## 🏠 Home Assistant CLI

### Tools

#### ha_state_get
Get the current state of a Home Assistant entity. Returns attributes, state value, and last-changed timestamp.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| entity_id  | string  | The entity ID to query               |

#### ha_state_list
List all Home Assistant entities, or filter by domain.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| domain     | string  | Optional domain to filter by         |

#### ha_service_call
Call a Home Assistant service.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| domain     | string  | Service domain                       |
| service    | string  | Service name                         |
| entity_id  | string  | Target entity ID                     |
| data       | object  | Additional service data              |

#### ha_event_list
List recent Home Assistant events, optionally filtered by entity_id.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| entity_id  | string  | Optional entity ID to filter events  |

#### ha_person_find
Find a specific person tracked in Home Assistant.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| name       | string  | Name of the person to search for      |
| entity_id  | string  | Exact entity ID to look up            |

#### ha_speaker_volume_get
Get the current volume level of one or all speakers.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| entity_id  | string  | Optional entity ID of the speaker     |

#### ha_speaker_volume_set
Set the volume of a speaker.

| Name         | Type    | Description                           |
|--------------|---------|---------------------------------------|
| entity_id    | string  | Entity ID of the speaker to adjust   |
| volume_level | number  | Desired volume level                 |

---

<a id="ics-calendar"></a>

## 📅 ICS Calendar

### Tools

#### ics_calendar_fetch
Fetch upcoming events from Nicole's ICS calendar feed.

| Name  | Type    | Description                           |
|-------|---------|---------------------------------------|
| days  | integer | Number of days ahead to fetch         |

---

<a id="opentable"></a>

## 🍽️ OpenTable

### Tools

#### opentable_lookup
Look up an OpenTable restaurant by its URL slug.

| Name | Type   | Description                           |
|------|--------|---------------------------------------|
| slug | string | Restaurant URL slug                  |

#### opentable_availability
Check real-time availability for a restaurant on OpenTable.

| Name          | Type    | Description                           |
|---------------|---------|---------------------------------------|
| restaurant_id | integer | Numeric restaurant ID                |
| date          | string  | Date in YYYY-MM-DD format            |
| party_size    | integer | Number of guests                     |
| time          | string  | Preferred time in HH:MM format       |

---

<a id="opentable-heartbeat"></a>

## ❤️ OpenTable Heartbeat

### Tools

#### opentable_heartbeat_check
Run OpenTable health check. Returns status (ok or error) and a message.

---

<a id="outlook-calendar"></a>

## 📅 Outlook Calendar

### Tools

#### outlook_calendar_fetch
Fetch upcoming events from personal and/or family Outlook calendars via Microsoft Graph API.

| Name     | Type    | Description                           |
|----------|---------|---------------------------------------|
| calendar | string  | Which calendar to fetch              |
| days     | integer | Number of days ahead to fetch events |

---

<a id="outlook-mail"></a>

## 📧 Outlook Mail

### Tools

#### outlook_inbox
List recent messages from the Outlook inbox.

| Name   | Type    | Description                           |
|--------|---------|---------------------------------------|
| limit  | integer | Maximum number of messages to return |
| unread | boolean | If true, return only unread messages |

#### outlook_search
Search Outlook messages by query text, sender, subject, or date range.

| Name   | Type    | Description                           |
|--------|---------|---------------------------------------|
| query  | string  | Full-text search across subject/body |
| from   | string  | Filter by sender email address       |
| subject| string  | Filter by subject                   |
| since  | string  | Messages received on or after date  |
| before | string  | Messages received on or before date |
| limit  | integer | Maximum number of results           |

#### outlook_read
Read a specific Outlook message by its ID.

| Name       | Type    | Description                           |
|------------|---------|---------------------------------------|
| message_id | string  | The Microsoft Graph message ID       |

---

<a id="outlook-work-calendar"></a>

## 🏢 Outlook Work Calendar

### Tools

#### outlook_work_calendar_fetch
Fetch upcoming events from the published Outlook work calendar.

| Name  | Type    | Description                           |
|-------|---------|---------------------------------------|
| days  | integer | Number of days ahead to fetch        |

---

<a id="spotify"></a>

## 🎵 Spotify

### Tools

#### spotify_now_playing
Get the currently playing track on Spotify.

#### spotify_play
Start or resume Spotify playback.

| Name      | Type    | Description                           |
|-----------|---------|---------------------------------------|
| uri       | string  | Spotify URI to play                  |
| device_id | string  | Target device ID                     |

#### spotify_pause
Pause Spotify playback.

| Name      | Type    | Description                           |
|-----------|---------|---------------------------------------|
| device_id | string  | Target device ID                     |

#### spotify_next
Skip to the next track in the Spotify queue.

| Name      | Type    | Description                           |
|-----------|---------|---------------------------------------|
| device_id | string  | Target device ID                     |

#### spotify_previous
Go back to the previous track on Spotify.

| Name      | Type    | Description                           |
|-----------|---------|---------------------------------------|
| device_id | string  | Target device ID                     |

#### spotify_search
Search Spotify for tracks, albums, artists, or playlists.

| Name   | Type    | Description                           |
|--------|---------|---------------------------------------|
| query  | string  | Search query                         |
| type   | string  | Type of result to search for         |
| limit  | integer | Max number of results to return      |

#### spotify_add_to_playlist
Add a track to a Spotify playlist.

| Name         | Type    | Description                           |
|--------------|---------|---------------------------------------|
| playlist_id  | string  | Spotify playlist ID                  |
| track_uri    | string  | Spotify track URI to add             |

#### spotify_get_playlists
List the current user's Spotify playlists.

| Name   | Type    | Description                           |
|--------|---------|---------------------------------------|
| limit  | integer | Max number of playlists to return    |

#### spotify_get_devices
List available Spotify Connect devices.

---

<a id="weightwatchers"></a>

## 🍎 WeightWatchers

### Tools

#### ww_daily
Get daily WW food diary.

| Name  | Type    | Description                           |
|-------|---------|---------------------------------------|
| date  | string  | Date in YYYY-MM-DD format            |

#### ww_search
Search the WW food database.

| Name   | Type    | Description                           |
|--------|---------|---------------------------------------|
| query  | string  | Food search query                    |
| limit  | integer | Max results to return               |

#### ww_log
Log a food item to the WW diary.

| Name         | Type    | Description                           |
|--------------|---------|---------------------------------------|
| food_id      | string  | WW food ID                           |
| portion_id   | string  | Portion ID                          |
| version_id   | string  | Food version ID                     |
| portion_size | number  | Portion multiplier                  |
| date         | string  | Date in YYYY-MM-DD format           |
| meal_type    | string  | Meal slot to log to                 |
| source_type  | string  | Food source type                    |

#### ww_points
Calculate WW SmartPoints offline from nutrition data.

| Name          | Type    | Description                           |
|---------------|---------|---------------------------------------|
| calories      | number  | Total calories                      |
| saturated_fat | number  | Saturated fat in grams              |
| sugar         | number  | Sugar in grams                      |
| protein       | number  | Protein in grams                    |

#### ww_budget
Get remaining WW points budget for a date.

| Name  | Type    | Description                           |
|-------|---------|---------------------------------------|
| date  | string  | Date in YYYY-MM-DD format            |

#### ww_quick_add
Quick-add a points value to the WW diary.

| Name      | Type    | Description                           |
|-----------|---------|---------------------------------------|
| points    | integer | Number of SmartPoints to add         |
| name      | string  | Label for the diary entry            |
| meal_type | string  | Meal slot to log to                  |
| date      | string  | Date in YYYY-MM-DD format           |

#### ww_delete
Delete a tracked food entry from the WW diary.

| Name         | Type    | Description                           |
|--------------|---------|---------------------------------------|
| tracking_id  | string  | Tracking ID of the diary entry       |
| date         | string  | Date of the entry                   |
