---
layout: default
title: Plugins
nav_order: 3
---

# Plugins Overview

| Emoji | Plugin Name | Description | Tool Count |
|-------|-------------|-------------|------------|
| 🗂️ | [Config Backup](#🗂️-config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection | 1 |
| 📧 | [FastMail](#📧-fastmail) | Send email, search/read inbox, manage calendar events via JMAP and CalDAV | 7 |
| 📷 | [Home Assistant Camera Snapshot](#📷-home-assistant-camera-snapshot) | Take snapshots from Home Assistant cameras via hass-cli and save locally | 2 |
| 🏠 | [Home Assistant CLI](#🏠-home-assistant-cli) | Control Home Assistant via hass-cli: get/list entity states, call services, and list events | 4 |
| 📅 | [ICS Calendar](#📅-ics-calendar) | Fetches Nicole's calendar from an ICS feed | 1 |
| 🍽️ | [OpenTable](#🍽️-opentable) | Check restaurant availability on OpenTable | 2 |
| ❤️ | [OpenTable Heartbeat](#❤️-opentable-heartbeat) | Health-check for the OpenTable skill. Alerts on failure via configured notification channel | 1 |
| 📆 | [Outlook Calendar](#📆-outlook-calendar) | Fetch personal and family calendars via Microsoft Graph API | 1 |
| ✉️ | [Outlook Mail](#✉️-outlook-mail) | Search and read Outlook inbox via Microsoft Graph API | 3 |
| 🏢 | [Outlook Work Calendar](#🏢-outlook-work-calendar) | Fetches published Outlook work calendar via EWS JSON API (no auth required) | 1 |
| 🍎 | [WeightWatchers](#🍎-weightwatchers) | Search foods, log meals, view diary and points budget via the unofficial WW API | 5 |

---

## 🗂️ Config Backup

Backs up OpenClaw config to Git with SHA-256 change detection.

### Tools

#### config_backup_run

Back up OpenClaw config and agent workspace to Git. Copies `~/.openclaw` config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| force      | boolean | Force backup even if no changes detected      |
| check_only | boolean | Only check for changes without committing     |
| verbose    | boolean | Include verbose diagnostic output             |

---

## 📧 FastMail

Send email, search/read inbox, manage calendar events via JMAP and CalDAV.

### Tools

#### fastmail_send

Send a plain-text email via Fastmail JMAP, with optional file attachments.

| Name       | Type    | Description                         |
|------------|---------|-------------------------------------|
| to         | string  | Recipient email address(es)         |
| cc         | array   | CC recipient email address(es)      |
| subject    | string  | Email subject line                  |
| body       | string  | Plain-text email body               |
| signature  | string  | Signature block appended after body |
| attachment | array   | File path(s) to attach              |

#### fastmail_search

Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

| Name       | Type    | Description                              |
|------------|---------|------------------------------------------|
| account_id | string  | JMAP account ID (defaults to env value)  |
| query      | string  | Full-text search query                   |
| from       | string  | Filter by sender email or domain         |
| to         | string  | Filter by recipient                      |
| subject    | string  | Filter by subject text                   |
| since      | string  | Emails after this date (YYYY-MM-DD)      |
| before     | string  | Emails before this date (YYYY-MM-DD)     |
| limit      | integer | Max results (default 20)                 |

#### fastmail_read

Read a specific email by its JMAP email ID, returning full headers and body text.

| Name       | Type    | Description                              |
|------------|---------|------------------------------------------|
| account_id | string  | JMAP account ID (defaults to env value)  |
| id         | string  | JMAP email ID to read                    |

#### fastmail_inbox

Show recent emails from the Fastmail inbox, optionally filtered to unread only.

| Name       | Type    | Description                              |
|------------|---------|------------------------------------------|
| account_id | string  | JMAP account ID (defaults to env value)  |
| limit      | integer | Max emails to show (default 10)          |
| unread     | boolean | Only show unread emails                  |

#### fastmail_meeting

Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name         | Type    | Description                                   |
|--------------|---------|-----------------------------------------------|
| to           | string  | Attendee email address(es)                   |
| cc           | array   | CC recipient email address(es)                |
| subject      | string  | Meeting title                                |
| start        | string  | Start datetime in ISO format                 |
| duration     | string  | Duration: '1h', '30m', '1.5h' (default: 1h)  |
| location     | string  | Meeting location                             |
| description  | string  | Meeting description / agenda                 |
| timezone     | string  | IANA timezone (default: America/Los_Angeles) |
| signature    | string  | Signature block for the invite email         |

#### fastmail_update_event

Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name            | Type    | Description                                  |
|-----------------|---------|----------------------------------------------|
| uid             | string  | Exact event UID to target                   |
| find            | string  | Free-text search across event title/description |
| new_title       | string  | Replace the event title                     |
| new_start       | string  | New start time (ISO format)                 |
| new_duration    | string  | New duration (e.g. '1h', '30m')             |
| new_location    | string  | Replace location                            |
| new_description | string  | Replace description/notes                   |
| timezone        | string  | Timezone for --new-start (default: America/Los_Angeles) |
| status          | string  | Update event status (confirmed, tentative, cancelled) |
| add_attendee    | array   | Email(s) to add as attendees                |
| remove_attendee | array   | Email(s) to remove from attendees           |
| no_notify       | boolean | Skip iMIP update notifications              |
| force           | boolean | Update all matching events when multiple found |

#### fastmail_query_events

Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| after     | string  | Only events starting at or after this date (ISO) |
| before    | string  | Only events starting before this date (ISO)      |
| text      | string  | Filter by text match on title/description         |
| attendee  | string  | Filter to events including this attendee email    |
| uid       | string  | Return the single event with this exact UID       |

---

## 📷 Home Assistant Camera Snapshot

Take snapshots from Home Assistant cameras via hass-cli and save locally.

### Tools

#### hass_camera_snapshot

Take a snapshot from a Home Assistant camera. Saves the image locally and returns the file path.

| Name        | Type    | Description                                                                 |
|-------------|---------|-----------------------------------------------------------------------------|
| camera_name | string  | Name of the camera to snapshot. Use 'all' to capture every camera.          |

#### hass_camera_list

List all available Home Assistant cameras and their entity IDs.

---

## 🏠 Home Assistant CLI

Control Home Assistant via hass-cli: get/list entity states, call services, and list events.

### Tools

#### ha_state_get

Get the current state of a Home Assistant entity. Returns attributes, state value, and last-changed timestamp.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| entity_id | string  | The entity ID to query (e.g. light.living_room). |

#### ha_state_list

List all Home Assistant entities, or filter by domain.

| Name   | Type    | Description                                      |
|--------|---------|--------------------------------------------------|
| domain | string  | Optional domain to filter by (e.g. light).       |

#### ha_service_call

Call a Home Assistant service (e.g. turn on a light, activate a scene).

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| domain    | string  | Service domain (e.g. light, switch).             |
| service   | string  | Service name (e.g. turn_on, toggle).             |
| entity_id | string  | Target entity ID (e.g. light.living_room).       |
| data      | object  | Additional service data as key-value pairs.      |

#### ha_event_list

List recent Home Assistant events, optionally filtered by entity_id.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| entity_id | string  | Optional entity ID to filter events for.         |

---

## 📅 ICS Calendar

Fetches Nicole's calendar from an ICS feed.

### Tools

#### ics_calendar_fetch

Fetch upcoming events from Nicole's ICS calendar feed.

| Name  | Type    | Description                                      |
|-------|---------|--------------------------------------------------|
| days  | integer | Number of days ahead to fetch (default 7).       |

---

## 🍽️ OpenTable

Check restaurant availability on OpenTable.

### Tools

#### opentable_lookup

Look up an OpenTable restaurant by its URL slug to get its numeric restaurant ID.

| Name  | Type    | Description                                      |
|-------|---------|--------------------------------------------------|
| slug  | string  | Restaurant URL slug from opentable.com/r/<slug>. |

#### opentable_availability

Check real-time availability for a restaurant on OpenTable.

| Name          | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| restaurant_id | integer | Numeric restaurant ID (from opentable_lookup).   |
| date          | string  | Date in YYYY-MM-DD format.                       |
| party_size    | integer | Number of guests (default: 2).                   |
| time          | string  | Preferred time in HH:MM format (default: 19:00). |

---

## ❤️ OpenTable Heartbeat

Health-check for the OpenTable skill. Alerts on failure via configured notification channel.

### Tools

#### opentable_heartbeat_check

Run OpenTable health check. Returns status (ok or error) and a message.

---

## 📆 Outlook Calendar

Fetch personal and family calendars via Microsoft Graph API.

### Tools

#### outlook_calendar_fetch

Fetch upcoming events from personal and/or family Outlook calendars.

| Name      | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| calendar  | string  | Which calendar to fetch: personal, family, or all (default: all). |
| days      | integer | Number of days ahead to fetch events for (default: 7). |

---

## ✉️ Outlook Mail

Search and read Outlook inbox via Microsoft Graph API.

### Tools

#### outlook_inbox

List recent messages from the Outlook inbox.

| Name   | Type    | Description                                      |
|--------|---------|--------------------------------------------------|
| limit  | integer | Maximum number of messages to return (default 10). |
| unread | boolean | If true, return only unread messages.            |

#### outlook_search

Search Outlook messages by query text, sender, subject, or date range.

| Name   | Type    | Description                                      |
|--------|---------|--------------------------------------------------|
| query  | string  | Full-text search across subject and body.        |
| from   | string  | Filter by sender email address.                  |
| subject| string  | Filter by subject (substring match).             |
| since  | string  | Only messages received on or after this date.    |
| before | string  | Only messages received on or before this date.   |
| limit  | integer | Maximum number of results (default 10).          |

#### outlook_read

Read a specific Outlook message by its ID.

| Name        | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| message_id  | string  | The Microsoft Graph message ID to retrieve.      |

---

## 🏢 Outlook Work Calendar

Fetches published Outlook work calendar via EWS JSON API (no auth required).

### Tools

#### outlook_work_calendar_fetch

Fetch upcoming events from the published Outlook work calendar.

| Name  | Type    | Description                                      |
|-------|---------|--------------------------------------------------|
| days  | integer | Number of days ahead to fetch (default 7).       |

---

## 🍎 WeightWatchers

Search foods, log meals, view diary and points budget via the unofficial WW API.

### Tools

#### ww_daily

Get daily WW food diary. Returns tracked meals and points summary.

| Name  | Type    | Description                                      |
|-------|---------|--------------------------------------------------|
| date  | string  | Date in YYYY-MM-DD format (default: today).      |

#### ww_search

Search the WW food database.

| Name   | Type    | Description                                      |
|--------|---------|--------------------------------------------------|
| query  | string  | Food search query (e.g. 'grilled chicken breast'). |
| limit  | integer | Max results to return (default: 10).             |

#### ww_log

Log a food item to the WW diary.

| Name          | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| food_id       | string  | WW food ID (from ww_search results).             |
| portion_id    | string  | Portion ID (from ww_search results).             |
| version_id    | string  | Food version ID (from ww_search results).        |
| portion_size  | number  | Portion multiplier (default: 1.0).               |
| date          | string  | Date in YYYY-MM-DD format (default: today).      |
| meal_type     | string  | Meal slot to log to (default: snacks).           |
| source_type   | string  | Food source type (default: WWFOOD).              |

#### ww_points

Calculate WW SmartPoints offline from nutrition data.

| Name           | Type    | Description                                      |
|----------------|---------|--------------------------------------------------|
| calories       | number  | Total calories.                                  |
| saturated_fat  | number  | Saturated fat in grams.                          |
| sugar          | number  | Sugar in grams.                                  |
| protein        | number  | Protein in grams.                                |

#### ww_budget

Get remaining WW points budget for a date.

| Name  | Type    | Description                                      |
|-------|---------|--------------------------------------------------|
| date  | string  | Date in YYYY-MM-DD format (default: today).      |
