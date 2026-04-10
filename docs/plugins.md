---
layout: default
title: Plugins
nav_order: 3
---

- 🗄️ [Config Backup](#config-backup)
- 📧 [Fastmail](#fastmail)
- 🐙 [Github](#github)
- 🏠 [Homeassistant](#homeassistant)
- 📅 [Ics Calendar](#ics-calendar)
- 👁️ [Llmvision](#llmvision)
- ❤️ [Opentable Heartbeat](#opentable-heartbeat)
- 🍽️ [Opentable](#opentable)
- 📅 [Outlook Calendar](#outlook-calendar)
- 📧 [Outlook Mail](#outlook-mail)
- 📅 [Outlook Work Calendar](#outlook-work-calendar)
- 📦 [Package Tracking](#package-tracking)
- 🎵 [Spotify](#spotify)
- 📈 [Stock Quotes](#stock-quotes)
- 📬 [Usps Mail](#usps-mail)
- 🥗 [Weightwatchers](#weightwatchers)



<a id="config-backup"></a>

## 🗄️ Config Backup

Backs up OpenClaw config to Git with SHA-256 change detection.

#### config_backup_run

Back up OpenClaw config and agent workspace to Git. Copies ~/.openclaw config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name        | Type    | Description                                 |
|-------------|---------|---------------------------------------------|
| force       | boolean | Force backup even if no changes detected    |
| check_only  | boolean | Only check for changes without committing   |
| verbose     | boolean | Include verbose diagnostic output           |

<a id="fastmail"></a>

## 📧 Fastmail

Send email, search and read inbox, and manage calendar events via JMAP and CalDAV.

#### fastmail_send

Send a plain-text email via Fastmail JMAP, with optional file attachments.

| Name       | Type    | Description                       |
|------------|---------|-----------------------------------|
| to         | string  | Recipient email address(es)       |
| cc         | array   | CC recipient email address(es)    |
| subject    | string  | Email subject line                |
| body       | string  | Plain-text email body             |
| signature  | string  | Signature block appended after body|
| attachment | array   | File path(s) to attach            |

#### fastmail_search

Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| account_id| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| query     | string  | Full-text search query                           |
| from      | string  | Filter by sender email or domain                 |
| to        | string  | Filter by recipient                              |
| subject   | string  | Filter by subject text                           |
| since     | string  | Emails after this date (YYYY-MM-DD)              |
| before    | string  | Emails before this date (YYYY-MM-DD)             |
| limit     | integer | Max results (default 20)                         |

#### fastmail_read

Read a specific email by its JMAP email ID, returning full headers and body text.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| account_id| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| id        | string  | JMAP email ID to read                            |

#### fastmail_inbox

Show recent emails from the Fastmail inbox, optionally filtered to unread only.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| account_id| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| limit     | integer | Max emails to show (default 10)                  |
| unread    | boolean | Only show unread emails                          |

#### fastmail_meeting

Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name       | Type    | Description                                     |
|------------|---------|-------------------------------------------------|
| to         | string  | Attendee email address(es)                      |
| cc         | array   | CC recipient email address(es)                  |
| subject    | string  | Meeting title                                   |
| start      | string  | Start datetime in ISO format (e.g. 2026-03-15T14:00) |
| duration   | string  | Duration: '1h', '30m', '1.5h' (default: 1h)    |
| location   | string  | Meeting location                                |
| description| string  | Meeting description / agenda                    |
| timezone   | string  | IANA timezone (default: America/Los_Angeles)    |
| signature  | string  | Signature block for the invite email            |

#### fastmail_update_event

Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name           | Type    | Description                                   |
|----------------|---------|-----------------------------------------------|
| uid            | string  | Exact event UID to target                     |
| find           | string  | Free-text search across event title/description|
| new_title      | string  | Replace the event title                       |
| new_start      | string  | New start time (ISO format)                   |
| new_duration   | string  | New duration (e.g. '1h', '30m')               |
| new_location   | string  | Replace location                              |
| new_description| string  | Replace description/notes                     |
| timezone       | string  | Timezone for --new-start (default: America/Los_Angeles) |
| status         | string  | Update event status ('confirmed', 'tentative', 'cancelled') |
| add_attendee   | array   | Email(s) to add as attendees                  |
| remove_attendee| array   | Email(s) to remove from attendees             |
| no_notify      | boolean | Skip iMIP update notifications                |
| force          | boolean | Update all matching events when multiple found|

#### fastmail_query_events

Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name     | Type    | Description                                        |
|----------|---------|----------------------------------------------------|
| after    | string  | Only events starting at or after this date (ISO, e.g. 2026-03-01) |
| before   | string  | Only events starting before this date (ISO, e.g. 2026-04-01)      |
| text     | string  | Filter by text match on title/description          |
| attendee | string  | Filter to events including this attendee email     |
| uid      | string  | Return the single event with this exact UID        |

<a id="github"></a>

## 🐙 Github

Manage GitHub issues. Create, read, update, close, comment on, and list issues.

#### github_create_issue

Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.

| Name      | Type     | Description                                                  |
|-----------|----------|--------------------------------------------------------------|
| owner     | string   | Repository owner (user or organisation name)                 |
| repo      | string   | Repository name                                              |
| title     | string   | Issue title                                                  |
| body      | string   | Issue body (Markdown supported). Defaults to empty string.   |
| labels    | array    | Labels to apply to the issue (must already exist in the repo)|
| assignees | array    | GitHub usernames to assign the issue to                      |
| milestone | integer  | Milestone number to associate with the issue                 |

#### github_get_issue

Get a single GitHub issue by its number. Returns issue details including title, body, state, labels, and assignees.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |

#### github_edit_issue

Edit an existing GitHub issue. Update title, body, state, labels, assignees, or milestone. At least one field to update must be provided.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |
| title        | string  | New issue title                             |
| body         | string  | New issue body (Markdown supported)         |
| state        | string  | Issue state (open or closed)                |
| labels       | array   | Labels to apply (replaces existing labels)  |
| assignees    | array   | Assignees (replaces existing assignees)     |
| milestone    | integer | Milestone number                            |

#### github_close_issue

Close or reopen a GitHub issue. By default closes the issue, set reopen=true to reopen it.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |
| reopen       | boolean | Set to true to reopen the issue instead of closing it |

#### github_comment_issue

Add a comment to a GitHub issue. Returns the comment ID, body, user, and URL.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |
| body         | string  | Comment body (Markdown supported)           |

#### github_list_issues

List GitHub issues with optional filters. Filter by state (open/closed/all), labels, assignee, and milestone. Returns a list of issues and the total count.

| Name      | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| owner     | string  | Repository owner (user or organisation name)        |
| repo      | string  | Repository name                                     |
| state     | string  | Filter by state (default: open)                     |
| labels    | string  | Comma-separated list of labels to filter by         |
| assignee  | string  | Filter by assignee username                         |
| milestone | string  | Filter by milestone number or '*' for any milestone |
| per_page  | integer | Results per page (default: 30, max: 100)            |
| page      | integer | Page number for pagination (default: 1)             |

<a id="homeassistant"></a>

## 🏠 Homeassistant

Control Home Assistant via REST API: get/list entity states, call services, query logbook, and more.

#### hass_state_get

Get the current state of a Home Assistant entity. Returns attributes, state value, and last-changed timestamp.

| Name      | Type   | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| entity_id | string | The entity ID to query (e.g. light.living_room, sensor.temperature) |

#### hass_state_list

List all Home Assistant entities, or filter by domain (e.g. light, switch, sensor, camera, person).

| Name   | Type   | Description                                         |
|--------|--------|-----------------------------------------------------|
| domain | string | Optional domain to filter by (e.g. light, switch, sensor) |

#### hass_service_call

Call a Home Assistant service (e.g. turn on a light, activate a scene). Specify domain, service, and optionally an entity_id and extra data.

| Name      | Type   | Description                                                                                  |
|-----------|--------|----------------------------------------------------------------------------------------------|
| domain    | string | Service domain (e.g. light, switch, scene, climate)                                          |
| service   | string | Service name (e.g. turn_on, turn_off, toggle)                                                |
| entity_id | string | Target entity ID (e.g. light.living_room)                                                    |
| data      | object | Additional service data as key-value pairs (e.g. {"brightness": 128})                        |

#### hass_event_list

List Home Assistant event types with listener counts.

| Name      | Type   | Description                                             |
|-----------|--------|---------------------------------------------------------|
| entity_id | string | Optional keyword to filter event types by string match. |

#### hass_person_find

Find a specific person tracked in Home Assistant. Search by the person's name (friendly name) or supply an exact entity_id. Returns the person's current state (home/away/zone) and attributes.

| Name      | Type   | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| name      | string | Name of the person to search for (case-insensitive substring match) |
| entity_id | string | Exact entity ID to look up (e.g. person.john)                      |

#### hass_speaker_volume_get

Get the current volume level of one or all speakers (media_player entities). If entity_id is omitted, returns volume info for all media_player entities.

| Name      | Type   | Description                                         |
|-----------|--------|-----------------------------------------------------|
| entity_id | string | Optional entity ID of the speaker (e.g. media_player.living_room) |

#### hass_speaker_volume_set

Set the volume of a speaker (media_player entity). volume_level must be a value between 0.0 (silent) and 1.0 (full volume).

| Name        | Type   | Description                                                      |
|-------------|--------|------------------------------------------------------------------|
| entity_id   | string | Entity ID of the speaker to adjust (e.g. media_player.living_room)|
| volume_level| number | Desired volume level between 0.0 (silent) and 1.0 (maximum)      |

#### hass_camera_list

List all available Home Assistant cameras and their entity IDs.

#### hass_camera_snapshot

Take a snapshot from a Home Assistant camera. Saves the image locally and returns the file path. Use camera_name 'all' to capture every camera.

| Name        | Type   | Description                                                                                 |
|-------------|--------|---------------------------------------------------------------------------------------------|
| camera_name | string | Name of the camera to snapshot. One of: living-room, front-doorbell, front-doorbell-package, backyard-right, backyard-left, driveway, family-room, garage, all |

#### hass_logbook

Get Home Assistant logbook entries with optional filters. Supports filtering by entity_id, date range (start_time/end_time as ISO strings, or hours for a rolling window), keyword search, and result limit. Useful for 'last time X happened' queries or activity history.

| Name      | Type    | Description                                                                                      |
|-----------|---------|--------------------------------------------------------------------------------------------------|
| entity_id | string  | Filter entries for a specific entity (e.g. binary_sensor.front_doorbell_camera_doorbell)         |
| hours     | number  | Rolling window in hours from now (default: 24). Ignored if start_time is provided.               |
| start_time| string  | Start of the time range as an ISO 8601 string (e.g. '2026-04-07T00:00:00+00:00').                |
| end_time  | string  | End of the time range as an ISO 8601 string. Defaults to now.                                    |
| keyword   | string  | Optional keyword to filter entries by name, message, entity_id, or state.                        |
| limit     | integer | Maximum number of entries to return (default: 100, max: 500).                                   |

<a id="ics-calendar"></a>

## 📅 Ics Calendar

Fetches Nicole's calendar from an ICS feed.

#### ics_calendar_fetch

Fetch upcoming events from an ICS calendar feed. Specify a calendar by passing either a direct `url`, or an `env_var` name that holds the ICS URL (e.g. CALENDAR_NICOLE_ICS_URL, CALENDAR_TRIPIT_ICS_URL, CALENDAR_FAMILY_ICS_URL, CALENDAR_PERSONAL_ICS_URL). If neither is provided, defaults to CALENDAR_NICOLE_ICS_URL. The `label` parameter sets the calendar name shown in the output.

| Name    | Type     | Description                                                                                  |
|---------|----------|----------------------------------------------------------------------------------------------|
| days    | integer  | Number of days ahead to fetch (default 7)                                                    |
| url     | string   | Direct ICS URL to fetch                                                                      |
| env_var | string   | Environment variable name holding the ICS URL (e.g. CALENDAR_TRIPIT_ICS_URL)                 |
| label   | string   | Display name for this calendar in output (e.g. 'Nicole', 'TripIt', 'Family')                 |

<a id="llmvision"></a>

## 👁️ Llmvision

Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events.

#### llmvision_timeline_get

Get events from the LLM Vision timeline (calendar.llm_vision_timeline). Returns a list of AI-generated observation events with timestamps, summaries, and descriptions. Useful for reviewing what the cameras have seen recently.

| Name        | Type     | Description                                                                                  |
|-------------|----------|----------------------------------------------------------------------------------------------|
| start_time  | string   | Start of the query window as ISO 8601 (e.g. '2026-04-09T00:00:00+00:00'). Defaults to now.   |
| end_time    | string   | End of the query window as ISO 8601. Defaults to start_time + days.                          |
| days        | integer  | Number of days ahead to include when end_time is not set (default: 7).                       |
| limit       | integer  | Maximum number of events to return (default: 50, max: 200).                                  |

#### llmvision_analyze_image

Trigger an AI image analysis on a Home Assistant camera entity using LLM Vision. Sends the current camera snapshot to the specified AI provider with a custom prompt and returns the AI-generated description. Can optionally store the result in the timeline.

| Name              | Type     | Description                                                                                  |
|-------------------|----------|----------------------------------------------------------------------------------------------|
| camera_entity     | string   | Camera entity ID to analyze (e.g. camera.front_door).                                        |
| message           | string   | Prompt / question to send to the AI about the image.                                         |
| provider          | string   | LLM Vision provider to use (e.g. 'anthropic', 'openai', 'ollama').                           |
| model             | string   | Specific model override (optional, uses provider default if omitted).                        |
| store_in_timeline | boolean  | Whether to save the result as a timeline event (default: false).                             |
| expose_images     | boolean  | Whether to expose the captured image in the timeline event.                                  |
| generate_title    | boolean  | Whether to auto-generate a title for the timeline event.                                     |
| response_format   | string   | Response format from the AI: 'text' (default) or 'json'.                                     |
| max_tokens        | integer  | Maximum tokens for the AI response.                                                          |

#### llmvision_create_event

Create a new event in the LLM Vision timeline. Use this to manually log observations or detections with optional camera image, label category, and time range.

<a id="opentable-heartbeat"></a>

## ❤️ Opentable Heartbeat

Health-check for the OpenTable skill. Alerts on failure via configured notification channel.

#### opentable_heartbeat_check

Run OpenTable health check. Returns status (ok or error) and a message.

<a id="opentable"></a>

## 🍽️ Opentable

Check restaurant availability on OpenTable.

#### opentable_lookup

Look up an OpenTable restaurant by its URL slug (e.g. 'carbone-new-york' from opentable.com/r/carbone-new-york) to get its numeric restaurant ID.

| Name  | Type   | Description                                      |
|-------|--------|--------------------------------------------------|
| slug  | string | Restaurant URL slug from opentable.com/r/<slug>  |

#### opentable_availability

Check real-time availability for a restaurant on OpenTable. Returns available time slots with booking URLs.

| Name          | Type    | Description                                 |
|---------------|---------|---------------------------------------------|
| restaurant_id | integer | Numeric restaurant ID (from opentable_lookup)|
| date          | string  | Date in YYYY-MM-DD format                   |
| party_size    | integer | Number of guests (default: 2)               |
| time          | string  | Preferred time in HH:MM format (default: 19:00) |

<a id="outlook-calendar"></a>

## 📅 Outlook Calendar

Fetch personal and family calendars via Microsoft Graph API.

#### outlook_calendar_fetch

Fetch upcoming events from personal and/or family Outlook calendars via Microsoft Graph API.

| Name     | Type    | Description                                                        |
|----------|---------|--------------------------------------------------------------------|
| calendar | string  | Which calendar to fetch: personal, family, or all (default: all).  |
| days     | integer | Number of days ahead to fetch events for (default: 7).             |

<a id="outlook-mail"></a>

## 📧 Outlook Mail

Search and read Outlook inbox messages using the Microsoft Graph API.

#### outlook_inbox

List recent messages from the Outlook inbox.

| Name   | Type    | Description                                      |
|--------|---------|--------------------------------------------------|
| limit  | integer | Maximum number of messages to return (default 10).|
| unread | boolean | If true, return only unread messages.             |

#### outlook_search

Search Outlook messages by query text, sender, subject, or date range.

| Name    | Type    | Description                                                    |
|---------|---------|----------------------------------------------------------------|
| query   | string  | Full-text search across subject and body.                      |
| from    | string  | Filter by sender email address.                                |
| subject | string  | Filter by subject (substring match).                           |
| since   | string  | Only messages received on or after this date (YYYY-MM-DD).     |
| before  | string  | Only messages received on or before this date (YYYY-MM-DD).    |
| limit   | integer | Maximum number of results (default 10).                        |

#### outlook_read

Read a specific Outlook message by its ID, including full body content.

| Name       | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| message_id | string | The Microsoft Graph message ID to retrieve. |

#### outlook_save_attachments

Download attachments from an Outlook message to a local directory. Also saves the message body as body.html. Useful for processing emails that contain inline images (e.g., USPS Informed Delivery).

| Name          | Type   | Description                                                        |
|---------------|--------|--------------------------------------------------------------------|
| message_id    | string | The Microsoft Graph message ID.                                    |
| output_dir    | string | Local directory path to save attachments to (created if needed).   |
| content_types | array  | Content type filters (e.g. ['image/*']). Defaults to ['image/*'].  |

<a id="outlook-work-calendar"></a>

## 📅 Outlook Work Calendar

Fetches published Outlook work calendar via EWS JSON API (no authentication required).

#### outlook_work_calendar_fetch

Fetch upcoming events from the published Outlook work calendar. Uses the EWS JSON API — no authentication required. Requires the OUTLOOK_WORK_CALENDAR_URL environment variable.

| Name  | Type    | Description                           |
|-------|---------|---------------------------------------|
| days  | integer | Number of days ahead to fetch (default 7) |

<a id="package-tracking"></a>

## 📦 Package Tracking

Track packages from UPS, FedEx, USPS, and Amazon using direct carrier URLs.

#### package_track

Get tracking information for a package by tracking number. Automatically detects carrier (UPS, FedEx, USPS, Amazon) from tracking number format. Returns tracking URL that can be opened in a browser. If the package is saved in the tracking list, returns saved info. Otherwise, generates tracking info on-the-fly.

| Name            | Type   | Description                                                                                  |
|-----------------|--------|----------------------------------------------------------------------------------------------|
| tracking_number | string | Package tracking number (e.g., 1Z999AA10123456784, 940000000000000000000, TBA012345678901US) |
| carrier         | string | Optional carrier override: UPS, FedEx, USPS, or Amazon                                      |

#### package_add

Add a package to the tracking list for easy access later. Automatically detects carrier from tracking number format. Optionally add a label/description for the package (e.g., 'iPhone case', 'Birthday gift'). Saved packages can be listed with package_list and tracked with package_track.

| Name            | Type   | Description                                               |
|-----------------|--------|-----------------------------------------------------------|
| tracking_number | string | Package tracking number                                   |
| carrier         | string | Optional carrier override: UPS, FedEx, USPS, or Amazon    |
| label           | string | Optional label/description for the package                |

#### package_remove

Remove a package from the tracking list. Use this when a package has been delivered and you no longer need to track it.

| Name            | Type   | Description                              |
|-----------------|--------|------------------------------------------|
| tracking_number | string | Package tracking number to remove         |

#### package_list

List all packages currently being tracked. Returns tracking numbers, carriers, URLs, labels, and when each package was added. Use this to see all your active shipments at a glance.

#### package_scan

Scan text (email body, message, etc.) for tracking numbers. Automatically detects UPS, FedEx, USPS, and Amazon tracking numbers. Returns list of found tracking numbers with carrier and tracking URL. Useful for extracting tracking info from shipping notifications.

| Name | Type   | Description                                    |
|------|--------|------------------------------------------------|
| text | string | Text to scan for tracking numbers (e.g., email body) |

<a id="spotify"></a>

## 🎵 Spotify

Control Spotify playback, search music, and manage playlists.

#### spotify_now_playing

Get the currently playing track on Spotify, including artist, album, and playback device.

#### spotify_play

Start or resume Spotify playback. Optionally provide a Spotify URI (track, album, artist, or playlist) to play something specific.

| Name      | Type   | Description                                                                                 |
|-----------|--------|---------------------------------------------------------------------------------------------|
| uri       | string | Spotify URI to play (e.g. spotify:track:..., spotify:album:..., spotify:playlist:...). Omit to resume current playback. |
| device_id | string | Target device ID (from spotify_get_devices). Omit to use the active device.                 |

#### spotify_pause

Pause Spotify playback.

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| device_id | string | Target device ID. Omit to use the active device. |

#### spotify_next

Skip to the next track in the Spotify queue.

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| device_id | string | Target device ID. Omit to use the active device. |

#### spotify_previous

Go back to the previous track on Spotify.

| Name      | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| device_id | string | Target device ID. Omit to use the active device. |

#### spotify_search

Search Spotify for tracks, albums, artists, or playlists. Returns names, URIs, and metadata for use with other Spotify tools.

| Name   | Type    | Description                                                                                  |
|--------|---------|----------------------------------------------------------------------------------------------|
| query  | string  | Search query (e.g. 'Daft Punk Digital Love', 'chill jazz playlist').                         |
| type   | string  | Type of result to search for (default: track).                                               |
| limit  | integer | Max number of results to return (default: 10, max: 50).                                      |

#### spotify_add_to_playlist

Add a track to a Spotify playlist by playlist ID and track URI.

| Name        | Type   | Description                                              |
|-------------|--------|----------------------------------------------------------|
| playlist_id | string | Spotify playlist ID (from spotify_get_playlists).        |
| track_uri   | string | Spotify track URI to add (e.g. spotify:track:...).       |

#### spotify_get_playlists

List the current user's Spotify playlists with IDs and track counts.

| Name   | Type    | Description                                         |
|--------|---------|-----------------------------------------------------|
| limit  | integer | Max number of playlists to return (default: 20, max: 50). |

#### spotify_get_devices

List available Spotify Connect devices (speakers, phones, computers) with their IDs and active status.

<a id="stock-quotes"></a>

## 📈 Stock Quotes

Fetch real-time stock, ETF, and mutual fund prices server-side.

#### stock_quote

Get current stock price, change, and percent change for a single ticker symbol. Works for stocks, ETFs, and mutual funds (e.g., MSFT, QQQ, FXAIX). Uses Yahoo Finance by default (no auth required). If FINNHUB_API_KEY is set, uses Finnhub API as primary source with Yahoo Finance fallback.

| Name   | Type   | Description                                              |
|--------|--------|----------------------------------------------------------|
| symbol | string | Stock ticker symbol (e.g., AAPL, GOOGL, QQQ, FXAIX)      |

#### stock_quotes

Get current stock prices for multiple ticker symbols in a single batch request. Works for stocks, ETFs, and mutual funds. Returns all successful quotes plus any errors for failed symbols. Uses Yahoo Finance by default (no auth required). If FINNHUB_API_KEY is set, uses Finnhub API as primary source with Yahoo Finance fallback.

| Name    | Type  | Description                                                        |
|---------|-------|--------------------------------------------------------------------|
| symbols | array | Array of stock ticker symbols (e.g., ['MSFT', 'QQQ', 'FXAIX'])     |

<a id="usps-mail"></a>

## 📬 Usps Mail

Analyze USPS Informed Delivery digest emails by parsing mailpiece scans, vision-classifying images, applying importance rules, writing memory, and sending notifications.

#### usps_process_digest

Process a USPS Informed Delivery digest email. Given a folder containing body.html and mailpiece scan images, parses the HTML, vision-analyzes each image via the configured vision agent, applies importance rules, optionally writes memory, and sends routed notifications. Use vision_backend='provided' and pass an analysis array if you have already analyzed the images yourself.

| Name            | Type    | Description                                                                                                                                                                                                                 |
|-----------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| folder          | string  | Path to directory containing body.html and image files.                                                                                                                                                                      |
| analysis        | array   | Optional pre-computed analysis. Array of objects, one per image (in filename sort order), each with: sender, addressee, description, type, importance, mail_class, address_method.                                          |
| date            | string  | Override delivery date (YYYY-MM-DD). Auto-detected if omitted.                                                                                                                        |
| dry_run         | boolean | If true, skip sending notifications (print instead).                                                                                                                                                                        |
| vision_backend  | string  | 'auto' (configured agent, default), 'provided' (use analysis arg), 'skip' (parsing only, no vision).                                                                                                                        |
| message_id      | string  | Outlook Graph API message ID of this digest. Used for state tracking and deduplication across runs.                                                                                                                         |
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                                                                                                   |
| memory_agent    | string  | Agent workspace that owns long-term mail memory markdown.                                                                                                                             |
| vision_agent    | string  | Agent that performs USPS scan-image vision analysis.                                                                                                                                                                        |

#### usps_lookup

Search past USPS mailpiece analysis history. Find mail by partial GUID, date, or text search across all fields (sender, addressee, description).

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| guid            | string  | Partial GUID to match (first 8 chars is typical).                                                             |
| date            | string  | Date or partial date to match (YYYY-MM-DD or YYYY-MM).                                                        |
| search          | string  | Text to search for in any field.                                                                              |
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

#### usps_update_rule

Add, remove, or test importance rules for USPS mail classification. Use action='add' with conditions and importance to create a new rule. Use action='remove' with index or comment_match. Use action='test' with a mailpiece dict to see which rule would match.

| Name           | Type    | Description                                                                                                   |
|----------------|---------|---------------------------------------------------------------------------------------------------------------|
| action         | string  | What to do. ('add', 'remove', 'test')                                                                         |
| conditions     | object  | Rule conditions (for 'add'). Keys like sender_contains, addressee_contains, description_not_contains, etc.     |
| importance     | string  | Target importance level (for 'add'). ('urgent', 'high', 'medium', 'low', 'junk', 'ad')                        |
| comment        | string  | Human-readable description of the rule (for 'add').                                                           |
| index          | integer | Rule index to remove (for 'remove').                                                                          |
| comment_match  | string  | Remove rule whose comment contains this text (for 'remove').                                                  |
| mailpiece      | object  | Mailpiece info dict to test against rules (for 'test').                                                       |
| workspace_agent| string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

#### usps_rules

List all USPS mail importance rules, or test which rule matches a specific mailpiece.

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| test_mailpiece  | object  | Optional mailpiece to test. Provide sender, addressee, etc. Returns which rule matches and the resulting importance. |
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

#### usps_stats

Show statistics for all analyzed USPS mail: total pieces, delivery days, breakdown by importance, top senders, and top addressees.

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

#### usps_status

Check the USPS mail workflow state: when mail was last checked, the last processed message ID, and how many digests have been processed. Use this before polling to determine the 'since' date.

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

<a id="weightwatchers"></a>

## 🥗 Weightwatchers

Search foods, log meals, view diary, and manage points budget via the unofficial WW API.

#### ww_daily

Get daily WW food diary. Returns tracked meals and points summary.

| Name  | Type   | Description                                 |
|-------|--------|---------------------------------------------|
| date  | string | Date in YYYY-MM-DD format (default: today)  |

#### ww_search

Search the WW food database. Returns food IDs, points, and portion options needed for logging.

| Name  | Type    | Description                                              |
|-------|---------|----------------------------------------------------------|
| query | string  | Food search query (e.g. 'grilled chicken breast')        |
| limit | integer | Max results to return (default: 10)                      |

#### ww_log

Log a food item to the WW diary. Requires food_id, version_id, and portion_id from ww_search results.

| Name         | Type    | Description                                                                                  |
|--------------|---------|----------------------------------------------------------------------------------------------|
| food_id      | string  | WW food ID (from ww_search results)                                                          |
| portion_id   | string  | Portion ID (from ww_search results)                                                          |
| version_id   | string  | Food version ID (from ww_search results)                                                     |
| portion_size | number  | Portion multiplier (default: 1.0)                                                            |
| date         | string  | Date in YYYY-MM-DD format (default: today)                                                   |
| meal_type    | string  | Meal slot to log to (default: snacks). Options: breakfast, lunch, dinner, snacks             |
| source_type  | string  | Food source type: WWFOOD, WWRECIPE, MEMBERFOOD, etc. (default: WWFOOD)                      |

#### ww_points

Calculate WW SmartPoints offline from nutrition data. No authentication required.

| Name          | Type   | Description                |
|---------------|--------|----------------------------|
| calories      | number | Total calories             |
| saturated_fat | number | Saturated fat in grams     |
| sugar         | number | Sugar in grams             |
| protein       | number | Protein in grams           |

#### ww_budget

Get remaining WW points budget for a date. Shows daily and weekly allowances.

| Name  | Type   | Description                                 |
|-------|--------|---------------------------------------------|
| date  | string | Date in YYYY-MM-DD format (default: today)  |

#### ww_quick_add

Quick-add a points value to the WW diary without specifying a food item. Useful when you know the points but not the exact food.

| Name      | Type    | Description                                                                |
|-----------|---------|----------------------------------------------------------------------------|
| points    | integer | Number of SmartPoints to add                                               |
| name      | string  | Label for the diary entry (default: 'Quick Add')                           |
| meal_type | string  | Meal slot to log to (default: snacks). Options: breakfast, lunch, dinner, snacks |
| date      | string  | Date in YYYY-MM-DD format (default: today)                                 |

#### ww_delete

Delete a tracked food entry from the WW diary by its tracking ID. Use ww_daily to get tracking IDs.

| Name        | Type   | Description                                                      |
|-------------|--------|------------------------------------------------------------------|
| tracking_id | string | Tracking ID of the diary entry to delete (from ww_daily results) |
| date        | string | Date of the entry in YYYY-MM-DD format (default: today)          |
