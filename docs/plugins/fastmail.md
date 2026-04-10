---
layout: default
title: Fastmail
parent: Plugins
nav_order: 2
---

📧 Fastmail

Send email, search and read inbox, and manage calendar events via JMAP and CalDAV.

### fastmail_send

Send a plain-text email via Fastmail JMAP, with optional file attachments.

| Name       | Type   | Description                       |
|------------|--------|-----------------------------------|
| to         | string | Recipient email address(es)        |
| cc         | array  | CC recipient email address(es)     |
| subject    | string | Email subject line                 |
| body       | string | Plain-text email body              |
| signature  | string | Signature block appended after body|
| attachment | array  | File path(s) to attach             |

### fastmail_search

Search emails in Fastmail inbox by keyword, sender, subject, or date range via JMAP.

| Name      | Type    | Description                                    |
|-----------|---------|------------------------------------------------|
| account_id| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| query     | string  | Full-text search query                         |
| from      | string  | Filter by sender email or domain               |
| to        | string  | Filter by recipient                            |
| subject   | string  | Filter by subject text                         |
| since     | string  | Emails after this date (YYYY-MM-DD)            |
| before    | string  | Emails before this date (YYYY-MM-DD)           |
| limit     | integer | Max results (default 20)                       |

### fastmail_read

Read a specific email by its JMAP email ID, returning full headers and body text.

| Name      | Type   | Description                                    |
|-----------|--------|------------------------------------------------|
| account_id| string | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| id        | string | JMAP email ID to read                          |

### fastmail_inbox

Show recent emails from the Fastmail inbox, optionally filtered to unread only.

| Name      | Type    | Description                                    |
|-----------|---------|------------------------------------------------|
| account_id| string  | JMAP account ID (defaults to FASTMAIL_ACCOUNT_ID env) |
| limit     | integer | Max emails to show (default 10)                |
| unread    | boolean | Only show unread emails                        |

### fastmail_meeting

Create a calendar meeting invite via CalDAV and send iMIP invitations to attendees.

| Name       | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| to         | string | Attendee email address(es)                     |
| cc         | array  | CC recipient email address(es)                 |
| subject    | string | Meeting title                                  |
| start      | string | Start datetime in ISO format (e.g. 2026-03-15T14:00) |
| duration   | string | Duration: '1h', '30m', '1.5h' (default: 1h)   |
| location   | string | Meeting location                               |
| description| string | Meeting description / agenda                   |
| timezone   | string | IANA timezone (default: America/Los_Angeles)   |
| signature  | string | Signature block for the invite email           |

### fastmail_update_event

Find a calendar event by UID or text search and update its title, time, location, attendees, or status.

| Name           | Type    | Description                                    |
|----------------|---------|------------------------------------------------|
| uid            | string  | Exact event UID to target                      |
| find           | string  | Free-text search across event title/description|
| new_title      | string  | Replace the event title                        |
| new_start      | string  | New start time (ISO format)                    |
| new_duration   | string  | New duration (e.g. '1h', '30m')                |
| new_location   | string  | Replace location                               |
| new_description| string  | Replace description/notes                      |
| timezone       | string  | Timezone for --new-start (default: America/Los_Angeles) |
| status         | string  | Update event status (`confirmed`, `tentative`, `cancelled`) |
| add_attendee   | array   | Email(s) to add as attendees                   |
| remove_attendee| array   | Email(s) to remove from attendees              |
| no_notify      | boolean | Skip iMIP update notifications                 |
| force          | boolean | Update all matching events when multiple found |

### fastmail_query_events

Query calendar events by date range, text, attendee email, or UID. Shows attendee RSVP status.

| Name    | Type   | Description                                    |
|---------|--------|------------------------------------------------|
| after   | string | Only events starting at or after this date (ISO, e.g. 2026-03-01) |
| before  | string | Only events starting before this date (ISO, e.g. 2026-04-01)     |
| text    | string | Filter by text match on title/description       |
| attendee| string | Filter to events including this attendee email  |
| uid     | string | Return the single event with this exact UID     |
