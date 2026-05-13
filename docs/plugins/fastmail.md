---
layout: default
title: FastMail tools
nav_order: 2
nav_exclude: true
---

# 📧 FastMail tools

Send email and manage calendar events in Fastmail

> **Source:** [JeffSteinbok/openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>accountId</code></td><td>string</td><td>Optional</td><td>JMAP account identifier.</td></tr>
    <tr><td><code>jmapToken</code></td><td>string</td><td>Optional</td><td>JMAP API authentication token.</td></tr>
    <tr><td><code>fromEmail</code></td><td>string</td><td>Optional</td><td>Sender email address.</td></tr>
    <tr><td><code>fromName</code></td><td>string</td><td>Optional</td><td>Sender display name.</td></tr>
    <tr><td><code>identityId</code></td><td>string</td><td>Optional</td><td>JMAP identity ID for sending.</td></tr>
    <tr><td><code>draftsId</code></td><td>string</td><td>Optional</td><td>JMAP mailbox ID for drafts.</td></tr>
    <tr><td><code>sentId</code></td><td>string</td><td>Optional</td><td>JMAP mailbox ID for sent mail.</td></tr>
    <tr><td><code>caldavUrl</code></td><td>string</td><td>Optional</td><td>CalDAV server URL.</td></tr>
    <tr><td><code>caldavUsername</code></td><td>string</td><td>Optional</td><td>CalDAV username.</td></tr>
    <tr><td><code>caldavPassword</code></td><td>string</td><td>Optional</td><td>CalDAV password.</td></tr>
    <tr><td><code>caldavCalendarPath</code></td><td>string</td><td>Optional</td><td>CalDAV calendar path.</td></tr>
  </tbody>
</table>

## Example config

```json
{
  "plugins": {
    "entries": {
      "fastmail": {
        "enabled": true,
        "config": {
          "accountId": "u12345678",
          "jmapToken": "fmu1-your-token-here",
          "fromEmail": "user@fastmail.com",
          "fromName": "Your Name",
          "identityId": "id-1234",
          "draftsId": "mailbox-drafts-id",
          "sentId": "mailbox-sent-id",
          "caldavUrl": "https://caldav.fastmail.com/dav",
          "caldavUsername": "user@fastmail.com",
          "caldavPassword": "app-password-here",
          "caldavCalendarPath": "/dav/calendars/user/default/"
        }
      }
    }
  }
}
```

## Tools

### `fastmail_send`

Send a plain-text email via Fastmail JMAP, with optional file attachments.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `to` | string | Required | Recipient email address(es). |
| `subject` | string | Required | Email subject line. |
| `body` | string | Required | Plain-text email body. |
| `cc` | array | Optional | CC recipient email address(es). |
| `signature` | string | Optional | Signature block appended after body. |
| `attachment` | array | Optional | File path(s) to attach. |

### `fastmail_search`

Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Optional | Full-text search query. |
| `from` | string | Optional | Filter by sender email or domain. |
| `to` | string | Optional | Filter by recipient. |
| `subject` | string | Optional | Filter by subject text. |
| `since` | string | Optional | Emails after this date (YYYY-MM-DD). |
| `before` | string | Optional | Emails before this date (YYYY-MM-DD). |
| `limit` | integer | Optional | Max results (default 20). |
| `account_id` | string | Optional | JMAP account ID override. |

### `fastmail_read`

Read a specific email by its JMAP email ID, returning full headers and body text.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | string | Required | JMAP email ID to read. |
| `account_id` | string | Optional | JMAP account ID override. |

### `fastmail_inbox`

Show recent emails from the Fastmail inbox, optionally filtered to unread only.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `limit` | integer | Optional | Max emails to show (default 10). |
| `unread` | boolean | Optional | Only show unread emails. |
| `account_id` | string | Optional | JMAP account ID override. |

### `fastmail_meeting`

Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `to` | string | Required | Attendee email address(es). |
| `subject` | string | Required | Meeting title. |
| `start` | string | Required | Start datetime in ISO format (e.g. 2026-03-15T14:00). |
| `cc` | array | Optional | CC recipient email address(es). |
| `duration` | string | Optional | Duration: '1h', '30m', '1.5h' (default: 1h). |
| `location` | string | Optional | Meeting location. |
| `description` | string | Optional | Meeting description / agenda. |
| `timezone` | string | Optional | IANA timezone (default: America/Los_Angeles). |
| `signature` | string | Optional | Signature block for the invite email. |

### `fastmail_update_event`

Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `uid` | string | Optional | Exact event UID to target. |
| `find` | string | Optional | Free-text search across event title/description. |
| `new_title` | string | Optional | Replace the event title. |
| `new_start` | string | Optional | New start time (ISO format). |
| `new_duration` | string | Optional | New duration (e.g. '1h', '30m'). |
| `new_location` | string | Optional | Replace location. |
| `new_description` | string | Optional | Replace description/notes. |
| `timezone` | string | Optional | Timezone for new_start (default: America/Los_Angeles). |
| `status` | string | Optional | Update event status. |
| `add_attendee` | array | Optional | Email(s) to add as attendees. |
| `remove_attendee` | array | Optional | Email(s) to remove from attendees. |
| `force` | boolean | Optional | Update all matching events when multiple found. |

### `fastmail_query_events`

Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `after` | string | Optional | Only events starting at or after this date (ISO, e.g. 2026-03-01). |
| `before` | string | Optional | Only events starting before this date (ISO, e.g. 2026-04-01). |
| `text` | string | Optional | Filter by text match on title/description. |
| `attendee` | string | Optional | Filter to events including this attendee email. |
| `uid` | string | Optional | Return the single event with this exact UID. |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/fastmail
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/fastmail.js --help

## Send a plain-text email via Fastmail JMAP, with optional file attachments.
node dist/bin/fastmail.js fastmail-send <to> <subject> <body> <cc...> <signature> <attachment...>

## Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.
node dist/bin/fastmail.js fastmail-search <query> <from> <to> <subject> <since> <before> <limit> <account_id>

## Read a specific email by its JMAP email ID, returning full headers and body text.
node dist/bin/fastmail.js fastmail-read <id> <account_id>

## Show recent emails from the Fastmail inbox, optionally filtered to unread only.
node dist/bin/fastmail.js fastmail-inbox <limit> <unread> <account_id>

## Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.
node dist/bin/fastmail.js fastmail-meeting <to> <subject> <start> <cc...> <duration> <location> <description> <timezone> <signature>

## Find a calendar event by UID or text search and update its title, time, location, attendees, or status.
node dist/bin/fastmail.js fastmail-update-event <uid> <find> <new_title> <new_start> <new_duration> <new_location> <new_description> <timezone> <status> <add_attendee...> <remove_attendee...> <force>

## Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.
node dist/bin/fastmail.js fastmail-query-events <after> <before> <text> <attendee> <uid>

## JSON output
node dist/bin/fastmail.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `FASTMAIL_ACCOUNT_ID` | JMAP account identifier |
| `FASTMAIL_JMAP_TOKEN` | JMAP API authentication token |
| `FASTMAIL_FROM_EMAIL` | Sender email address |
| `FASTMAIL_FROM_NAME` | Sender display name |
| `FASTMAIL_IDENTITY_ID` | JMAP identity ID for sending |
| `FASTMAIL_DRAFTS_ID` | JMAP mailbox ID for drafts |
| `FASTMAIL_SENT_ID` | JMAP mailbox ID for sent mail |
| `FASTMAIL_CALDAV_URL` | CalDAV server URL |
| `FASTMAIL_CALDAV_USERNAME` | CalDAV username |
| `FASTMAIL_CALDAV_PASSWORD` | CalDAV password |
| `FASTMAIL_CALDAV_CALENDAR_PATH` | CalDAV calendar path |
