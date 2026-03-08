# Plugins Overview

This document provides an overview of the available plugins, their functionality, and the tools they provide.

| Emoji | Plugin Name | Description | Tool Count |
|-------|-------------|-------------|------------|
| 🛠️   | [Config Backup](#-config-backup) | Backs up OpenClaw config to Git with SHA-256 change detection | 1 |
| 📧   | [FastMail](#-fastmail) | Send email, search/read inbox, manage calendar events via JMAP and CalDAV | 7 |
| 📷   | [Home Assistant Camera Snapshot](#-home-assistant-camera-snapshot) | Take snapshots from Home Assistant cameras via hass-cli and save locally | 2 |
| 🏠   | [Home Assistant CLI](#-home-assistant-cli) | Control Home Assistant via hass-cli: get/list entity states, call services, and list events | 4 |
| 📅   | [ICS Calendar](#-ics-calendar) | Fetches Nicole's calendar from an ICS feed | 1 |
| 🍽️   | [OpenTable](#-opentable) | Check restaurant availability on OpenTable | 0 |
| ❤️   | [OpenTable Heartbeat](#-opentable-heartbeat) | Health-check for the OpenTable skill. Alerts on failure via configured notification channel | 1 |
| 📅   | [Outlook Calendar](#-outlook-calendar) | Fetch personal and family calendars via Microsoft Graph API | 1 |
| 📧   | [Outlook Mail](#-outlook-mail) | Search and read Outlook inbox via Microsoft Graph API | 3 |
| 🗓️   | [Outlook Work Calendar](#-outlook-work-calendar) | Fetches published Outlook work calendar via EWS JSON API (no auth required) | 1 |
| 🍎   | [WeightWatchers](#-weightwatchers) | Search foods, log meals, view diary and points budget via the unofficial WW API | 5 |

---

## 🛠️ Config Backup

**Summary:** Backs up OpenClaw config to Git with SHA-256 change detection.

### Tools
- **config_backup_run**: Back up OpenClaw config and agent workspace to Git. Copies `~/.openclaw` config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

---

## 📧 FastMail

**Summary:** Send email, search/read inbox, manage calendar events via JMAP and CalDAV.

### Tools
- **fastmail_send**: Send a plain-text email via Fastmail JMAP, with optional file attachments.
- **fastmail_search**: Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.
- **fastmail_read**: Read a specific email by its JMAP email ID, returning full headers and body text.
- **fastmail_inbox**: Show recent emails from the Fastmail inbox, optionally filtered to unread only.
- **fastmail_meeting**: Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.
- **fastmail_update_event**: Find a calendar event by UID or text search and update its title, time, location, attendees, or status.
- **fastmail_query_events**: Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

---

## 📷 Home Assistant Camera Snapshot

**Summary:** Take snapshots from Home Assistant cameras via hass-cli and save locally.

### Tools
- **hass_camera_snapshot**: Take a snapshot from a Home Assistant camera. Saves the image locally and returns the file path. Use `camera_name` "all" to capture every camera.
- **hass_camera_list**: List all available Home Assistant cameras and their entity IDs.

---

## 🏠 Home Assistant CLI

**Summary:** Control Home Assistant via hass-cli: get/list entity states, call services, and list events.

### Tools
- **ha_state_get**: Get the current state of a Home Assistant entity. Returns attributes, state value, and last-changed timestamp.
- **ha_state_list**: List all Home Assistant entities, or filter by domain (e.g. light, switch, sensor, camera, person).
- **ha_service_call**: Call a Home Assistant service (e.g. turn on a light, activate a scene). Specify domain, service, and optionally an entity_id and extra data.
- **ha_event_list**: List recent Home Assistant events, optionally filtered by entity_id.

---

## 📅 ICS Calendar

**Summary:** Fetches Nicole's calendar from an ICS feed.

### Tools
- **ics_calendar_fetch**: Fetch upcoming events from Nicole's ICS calendar feed. Requires the `CALENDAR_NICOLE_ICS_URL` environment variable.

---

## 🍽️ OpenTable

**Summary:** Check restaurant availability on OpenTable.

### Tools
- No tools available.

---

## ❤️ OpenTable Heartbeat

**Summary:** Health-check for the OpenTable skill. Alerts on failure via configured notification channel.

### Tools
- **opentable_heartbeat_check**: Run OpenTable health check. Returns status (`ok` or `error`) and a message.

---

## 📅 Outlook Calendar

**Summary:** Fetch personal and family calendars via Microsoft Graph API.

### Tools
- **outlook_calendar_fetch**: Fetch upcoming events from personal and/or family Outlook calendars via Microsoft Graph API.

---

## 📧 Outlook Mail

**Summary:** Search and read Outlook inbox via Microsoft Graph API.

### Tools
- **outlook_inbox**: List recent messages from the Outlook inbox.
- **outlook_search**: Search Outlook messages by query text, sender, subject, or date range.
- **outlook_read**: Read a specific Outlook message by its ID, including full body content.

---

## 🗓️ Outlook Work Calendar

**Summary:** Fetches published Outlook work calendar via EWS JSON API (no auth required).

### Tools
- **outlook_work_calendar_fetch**: Fetch upcoming events from the published Outlook work calendar. Uses the EWS JSON API — no authentication required. Requires the `OUTLOOK_WORK_CALENDAR_URL` environment variable.

---

## 🍎 WeightWatchers

**Summary:** Search foods, log meals, view diary and points budget via the unofficial WW API.

### Tools
- **ww_daily**: Get daily WW food diary. Returns tracked meals and points summary.
- **ww_search**: Search the WW food database. Returns food IDs, points, and portion options needed for logging.
- **ww_log**: Log a food item to the WW diary. Requires `food_id`, `version_id`, and `portion_id` from `ww_search` results.
- **ww_points**: Calculate WW SmartPoints offline from nutrition data. No authentication required.
- **ww_budget**: Get remaining WW points budget for a date. Shows daily and weekly allowances.
