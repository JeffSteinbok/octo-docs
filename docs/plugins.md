---
layout: default
title: Plugins
nav_order: 3
---

# Plugins Overview

## Available Plugins

- 🎛 **[Config Backup](#config-backup)**: Backs up OpenClaw config to Git with SHA-256 change detection.
- 📧 **[FastMail](#fastmail)**: Send email, search/read inbox, manage calendar events via JMAP and CalDAV.
- 🐙 **[GitHub](#github)**: Manage GitHub issues. Create, read, update, close, comment on, and list issues.
- 📷 **[Hass Camera Snapshot](#hass-camera-snapshot)**: Take snapshots from Home Assistant cameras via hass-cli and save locally.
- 🏠 **[Home Assistant CLI](#home-assistant-cli)**: Control Home Assistant via hass-cli: get/list entity states, call services, and list events.
- 📅 **[ICS Calendar](#ics-calendar)**: Fetches Nicole's calendar from an ICS feed.
- 🍽 **[OpenTable](#opentable)**: Check restaurant availability on OpenTable.
- ❤️ **[OpenTable Heartbeat](#opentable-heartbeat)**: Health-check for the OpenTable skill. Alerts on failure via configured notification channel.
- 📅 **[Outlook Calendar](#outlook-calendar)**: Fetch personal and family calendars via Microsoft Graph API.
- 📧 **[Outlook Mail](#outlook-mail)**: Search and read Outlook inbox via Microsoft Graph API.
- 🏢 **[Outlook Work Calendar](#outlook-work-calendar)**: Fetches published Outlook work calendar via EWS JSON API (no auth required).
- 🎵 **[Spotify](#spotify)**: Control Spotify playback, search music, and manage playlists.
- 🍎 **[WeightWatchers](#weightwatchers)**: Search foods, log meals, view diary and points budget via the unofficial WW API.

---

<a id="config-backup"></a>

## 🎛 Config Backup

### Tools

#### config_backup_run
Back up OpenClaw config and agent workspace to Git. Copies `~/.openclaw` config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name       | Type    | Description                                   |
|------------|---------|-----------------------------------------------|
| `force`    | boolean | Force backup even if no changes detected      |
| `check_only` | boolean | Only check for changes without committing     |
| `verbose`  | boolean | Include verbose diagnostic output             |

---

<a id="fastmail"></a>

## 📧 FastMail

### Tools

#### fastmail_send
Send a plain-text email via FastMail JMAP, with optional file attachments.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `to`        | string  | Recipient email address(es)          |
| `cc`        | array   | CC recipient email address(es)       |
| `subject`   | string  | Email subject line                  |
| `body`      | string  | Plain-text email body               |
| `signature` | string  | Signature block appended after body |
| `attachment`| array   | File path(s) to attach              |

#### fastmail_search
Search emails in FastMail inbox by keyword, sender, subject, or date range via JMAP.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `account_id`| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| `query`     | string  | Full-text search query              |
| `from`      | string  | Filter by sender email or domain    |
| `to`        | string  | Filter by recipient                 |
| `subject`   | string  | Filter by subject text              |
| `since`     | string  | Emails after this date (YYYY-MM-DD) |
| `before`    | string  | Emails before this date (YYYY-MM-DD)|
| `limit`     | integer | Max results (default 20)            |

#### fastmail_read
Read a specific email by its JMAP email ID, returning full headers and body text.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `account_id`| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| `id`        | string  | JMAP email ID to read               |

#### fastmail_inbox
Show recent emails from the FastMail inbox, optionally filtered to unread only.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `account_id`| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| `limit`     | integer | Max emails to show (default 10)      |
| `unread`    | boolean | Only show unread emails             |

#### fastmail_meeting
Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `to`        | string  | Attendee email address(es)           |
| `cc`        | array   | CC recipient email address(es)       |
| `subject`   | string  | Meeting title                       |
| `start`     | string  | Start datetime in ISO format         |
| `duration`  | string  | Duration: '1h', '30m', '1.5h'        |
| `location`  | string  | Meeting location                    |
| `description`| string | Meeting description / agenda        |
| `timezone`  | string  | IANA timezone                       |
| `signature` | string  | Signature block for the invite email|

#### fastmail_update_event
Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `uid`       | string  | Exact event UID to target            |
| `find`      | string  | Free-text search across event title/description |
| `new_title` | string  | Replace the event title             |
| `new_start` | string  | New start time (ISO format)         |
| `new_duration`| string| New duration (e.g. '1h', '30m')     |
| `new_location`| string| Replace location                    |
| `new_description`| string| Replace description/notes        |
| `timezone`  | string  | Timezone for --new-start            |
| `status`    | string  | Update event status                 |
| `add_attendee`| array | Email(s) to add as attendees        |
| `remove_attendee`| array| Email(s) to remove from attendees |
| `no_notify` | boolean | Skip iMIP update notifications      |
| `force`     | boolean | Update all matching events when multiple found |

#### fastmail_query_events
Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `after`     | string  | Only events starting at or after this date |
| `before`    | string  | Only events starting before this date|
| `text`      | string  | Filter by text match on title/description |
| `attendee`  | string  | Filter to events including this attendee email |
| `uid`       | string  | Return the single event with this exact UID |

---

<a id="github"></a>

## 🐙 GitHub

### Tools

#### github_create_issue
Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `owner`     | string  | Repository owner (user or organisation name) |
| `repo`      | string  | Repository name                     |
| `title`     | string  | Issue title                         |
| `body`      | string  | Issue body (Markdown supported)     |
| `labels`    | array   | Labels to apply to the issue         |
| `assignees` | array   | GitHub usernames to assign the issue|
| `milestone` | integer | Milestone number to associate       |

#### github_get_issue
Get a single GitHub issue by its number. Returns issue details including title, body, state, labels, and assignees.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `owner`     | string  | Repository owner (user or organisation name) |
| `repo`      | string  | Repository name                     |
| `issue_number`| integer| Issue number                       |

#### github_edit_issue
Edit an existing GitHub issue. Update title, body, state, labels, assignees, or milestone. At least one field to update must be provided.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `owner`     | string  | Repository owner (user or organisation name) |
| `repo`      | string  | Repository name                     |
| `issue_number`| integer| Issue number                       |
| `title`     | string  | New issue title                     |
| `body`      | string  | New issue body                      |
| `state`     | string  | Issue state (open or closed)        |
| `labels`    | array   | Labels to apply                     |
| `assignees` | array   | Assignees                           |
| `milestone` | integer | Milestone number                    |

#### github_close_issue
Close or reopen a GitHub issue. By default closes the issue, set reopen=true to reopen it.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `owner`     | string  | Repository owner (user or organisation name) |
| `repo`      | string  | Repository name                     |
| `issue_number`| integer| Issue number                       |
| `reopen`    | boolean | Set to true to reopen the issue     |

#### github_comment_issue
Add a comment to a GitHub issue. Returns the comment ID, body, user, and URL.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `owner`     | string  | Repository owner (user or organisation name) |
| `repo`      | string  | Repository name                     |
| `issue_number`| integer| Issue number                       |
| `body`      | string  | Comment body                        |

#### github_list_issues
List GitHub issues with optional filters. Filter by state (open/closed/all), labels, assignee, and milestone. Returns a list of issues and the total count.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `owner`     | string  | Repository owner (user or organisation name) |
| `repo`      | string  | Repository name                     |
| `state`     | string  | Filter by state                     |
| `labels`    | string  | Comma-separated list of labels       |
| `assignee`  | string  | Filter by assignee username         |
| `milestone` | string  | Filter by milestone number          |
| `per_page`  | integer | Results per page                    |
| `page`      | integer | Page number for pagination          |

---

The documentation continues with similar structure for each plugin.
