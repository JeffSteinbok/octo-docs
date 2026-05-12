---
layout: default
title: FastMail tools
nav_order: 2
nav_exclude: true
---

# 📧 FastMail tools

Send email and manage calendar events in Fastmail

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail)

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
