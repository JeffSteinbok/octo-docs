---
layout: default
title: Plugins
nav_order: 3
---

# Plugins

OpenClaw ships with **15 plugins** exposing **55 tools** for home automation, email, calendars, music, tracking, and more.

| | Plugin | Description | Tools |
|---|--------|-------------|:-----:|
| 🛠️ | [Config Backup](#config-backup) | Back up OpenClaw config to Git with SHA-256 change detection | 1 |
| 📧 | [FastMail](#fastmail) | Send email, search/read inbox, manage calendar events via JMAP and CalDAV | 7 |
| 🐙 | [GitHub](#github) | Manage GitHub issues — create, read, update, close, comment on, and list | 6 |
| 📷 | [Home Assistant Camera](#home-assistant-camera) | Take snapshots from Home Assistant cameras via hass-cli | 2 |
| 🏠 | [Home Assistant CLI](#home-assistant-cli) | Control Home Assistant via hass-cli: entity states, services, events, people, and speakers | 7 |
| 📅 | [ICS Calendar](#ics-calendar) | Fetch calendar events from ICS feeds (supports TripIt and custom feeds) | 1 |
| 🍽️ | [OpenTable](#opentable) | Check restaurant availability on OpenTable | 2 |
| ❤️ | [OpenTable Heartbeat](#opentable-heartbeat) | Health-check for the OpenTable skill | 1 |
| 📆 | [Outlook Calendar](#outlook-calendar) | Fetch personal and family calendars via Microsoft Graph API | 1 |
| ✉️ | [Outlook Mail](#outlook-mail) | Read and search Outlook inbox via Microsoft Graph API | 3 |
| 🏢 | [Outlook Work Calendar](#outlook-work-calendar) | Fetch events from a published Outlook work calendar via EWS | 1 |
| 📦 | [Package Tracking](#package-tracking) | Track packages from UPS, FedEx, USPS, and Amazon | 5 |
| 🎵 | [Spotify](#spotify) | Spotify playback, search, playlists, and device control | 9 |
| 📈 | [Stock Quotes](#stock-quotes) | Fetch real-time stock, ETF, and mutual fund prices | 2 |
| 🍎 | [WeightWatchers](#weightwatchers) | WW food diary and points tracking | 7 |

---

<a id="config-backup"></a>

## 🛠️ Config Backup

Backs up OpenClaw config to Git with SHA-256 change detection.

#### `config_backup_run`
Back up OpenClaw config and agent workspace to Git.

---

<a id="fastmail"></a>

## 📧 FastMail

Send email, search/read inbox, manage calendar events via JMAP and CalDAV.

#### `fastmail_send`
Send a plain-text email via Fastmail JMAP, with optional file attachments.

#### `fastmail_search`
Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

#### `fastmail_read`
Read a specific email by its JMAP email ID, returning full headers and body text.

#### `fastmail_inbox`
Show recent emails from the Fastmail inbox, optionally filtered to unread only.

#### `fastmail_meeting`
Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

#### `fastmail_update_event`
Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

#### `fastmail_query_events`
Query calendar events by date range, text, attendee email, or UID.

---

<a id="github"></a>

## 🐙 GitHub

Manage GitHub issues — create, read, update, close, comment on, and list.

#### `github_create_issue`
Create a new issue in a GitHub repository.

#### `github_get_issue`
Get a single GitHub issue by its number.

#### `github_edit_issue`
Edit an existing GitHub issue (title, body, state, labels, assignees, milestone).

#### `github_close_issue`
Close or reopen a GitHub issue.

#### `github_comment_issue`
Add a comment to a GitHub issue.

#### `github_list_issues`
List GitHub issues with optional filters.

---

<a id="home-assistant-camera"></a>

## 📷 Home Assistant Camera

Take snapshots from Home Assistant cameras via hass-cli.

#### `hass_camera_snapshot`
Take a snapshot from a Home Assistant camera.

#### `hass_camera_list`
List all available Home Assistant cameras and their entity IDs.

---

<a id="home-assistant-cli"></a>

## 🏠 Home Assistant CLI

Control Home Assistant via hass-cli: entity states, services, events, people, and speakers.

#### `ha_state_get`
Get the current state of a Home Assistant entity.

#### `ha_state_list`
List all Home Assistant entities, or filter by domain.

#### `ha_service_call`
Call a Home Assistant service (e.g. turn on a light, activate a scene).

#### `ha_event_list`
List recent Home Assistant events, optionally filtered by entity_id.

#### `ha_person_find`
Find a specific person tracked in Home Assistant.

#### `ha_speaker_volume_get`
Get the current volume level of one or all speakers.

#### `ha_speaker_volume_set`
Set the volume of a speaker (media_player entity).

---

<a id="ics-calendar"></a>

## 📅 ICS Calendar

Fetch calendar events from ICS feeds (supports TripIt and custom feeds).

#### `ics_calendar_fetch`
Fetch upcoming events from an ICS calendar feed (by url, env_var, or label).

---

<a id="opentable"></a>

## 🍽️ OpenTable

Check restaurant availability on OpenTable.

#### `opentable_lookup`
Look up an OpenTable restaurant by its URL slug.

#### `opentable_availability`
Check real-time availability for a restaurant on OpenTable.

---

<a id="opentable-heartbeat"></a>

## ❤️ OpenTable Heartbeat

Health-check for the OpenTable skill.

#### `opentable_heartbeat_check`
Run OpenTable health check.

---

<a id="outlook-calendar"></a>

## 📆 Outlook Calendar

Fetch personal and family calendars via Microsoft Graph API.

#### `outlook_calendar_fetch`
Fetch upcoming events from personal and/or family Outlook calendars.

---

<a id="outlook-mail"></a>

## ✉️ Outlook Mail

Read and search Outlook inbox via Microsoft Graph API.

#### `outlook_inbox`
List recent messages from the Outlook inbox.

#### `outlook_search`
Search Outlook messages by query text, sender, subject, or date range.

#### `outlook_read`
Read a specific Outlook message by its ID.

---

<a id="outlook-work-calendar"></a>

## 🏢 Outlook Work Calendar

Fetch events from a published Outlook work calendar via EWS.

#### `outlook_work_calendar_fetch`
Fetch upcoming events from the published Outlook work calendar.

---

<a id="package-tracking"></a>

## 📦 Package Tracking

Track packages from UPS, FedEx, USPS, and Amazon.

#### `package_track`
Get tracking information for a package by tracking number (auto-detects carrier).

#### `package_add`
Add a package to the tracking list for easy access later.

#### `package_remove`
Remove a package from the tracking list.

#### `package_list`
List all packages currently being tracked.

#### `package_scan`
Scan text (email body, message) for tracking numbers.

---

<a id="spotify"></a>

## 🎵 Spotify

Spotify playback, search, playlists, and device control.

#### `spotify_now_playing`
Get the currently playing track on Spotify.

#### `spotify_play`
Start or resume Spotify playback (supports track, album, artist, playlist URIs).

#### `spotify_pause`
Pause Spotify playback.

#### `spotify_next`
Skip to the next track in the Spotify queue.

#### `spotify_previous`
Go back to the previous track on Spotify.

#### `spotify_search`
Search Spotify for tracks, albums, artists, or playlists.

#### `spotify_add_to_playlist`
Add a track to a Spotify playlist.

#### `spotify_get_playlists`
List the current user's Spotify playlists.

#### `spotify_get_devices`
List available Spotify Connect devices.

---

<a id="stock-quotes"></a>

## 📈 Stock Quotes

Fetch real-time stock, ETF, and mutual fund prices.

#### `stock_quote`
Get current stock price, change, and percent change for a single ticker symbol.

#### `stock_quotes`
Get current stock prices for multiple ticker symbols in a single batch request.

---

<a id="weightwatchers"></a>

## 🍎 WeightWatchers

WW food diary and points tracking.

#### `ww_daily`
Get daily WW food diary.

#### `ww_search`
Search the WW food database.

#### `ww_log`
Log a food item to the WW diary.

#### `ww_points`
Calculate WW SmartPoints offline from nutrition data.

#### `ww_budget`
Get remaining WW points budget for a date.

#### `ww_quick_add`
Quick-add a points value to the WW diary.

#### `ww_delete`
Delete a tracked food entry from the WW diary.
