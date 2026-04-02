---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## FastMail SSE Service 📬

The **FastMail SSE Service** is a real-time email notification daemon designed to monitor FastMail mailboxes for new emails and events. It connects to FastMail's JMAP EventSource to detect changes in real time, processes the incoming data, and sends notifications via OpenClaw's messaging system. This service is ideal for users who need timely updates on emails, package tracking, or meeting responses.

[Read more →](services/fastmail-sse)

### Key Features
- Per-account rules for customizable notification behavior.
- Simultaneous monitoring of multiple mailboxes (personal and shared).
- Automatic detection and registration of package tracking numbers.
- Notifications for calendar accept/decline/tentative responses.
- Real-time updates via JMAP SSE endpoint.
- Filters out spam and noreply senders.
- Sends notifications using OpenClaw's messaging system.

### Environment Variables

| Variable               | Required | Description                                                                 |
|------------------------|----------|-----------------------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN`  | Yes      | JMAP authentication token (or put in `~/.fastmail_token`).                  |
| `FASTMAIL_INBOX_IDS`   | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`).             |
| `FASTMAIL_INBOX_ID`    | Yes*     | Single mailbox ID (legacy, use `FASTMAIL_INBOX_IDS` for multiple).          |
| `NOTIFY_CHANNEL`       | No       | Notification channel (default: `telegram`).                                 |
| `NOTIFY_TARGET`        | Yes      | Target ID for the notification channel.                                     |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.
