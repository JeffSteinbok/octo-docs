---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page provides an overview of the available background services that can be used to enhance your system's functionality. Each service is designed to address specific use cases, such as real-time notifications or data processing, and integrates seamlessly with OpenClaw's ecosystem.

## Key Concepts

- Background services operate independently to perform specific tasks.
- Each service has configurable features tailored to different use cases.
- Environment variables are used to configure service behavior and authentication.
- Services can be monitored and managed using system tools like `systemctl`.

## FastMail SSE Service 📧

The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource, monitors new emails in one or more mailboxes, formats notifications, and sends them via OpenClaw's message system.

### Key Features

- Per-account rules: Configure notification behavior per account.
- Multi-mailbox monitoring: Monitor personal inbox and shared mailboxes simultaneously.
- Package tracking detection: Automatically detect and register tracking numbers.
- Meeting updates: Notify on calendar accept/decline/tentative responses.
- Connects to JMAP SSE endpoint for real-time state changes.
- Skips spam/noreply senders.
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`.

[Read more →](services/fastmail-sse)

### Environment Variables

| Variable              | Required | Description                                                                 |
|-----------------------|----------|-----------------------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN` | Yes      | JMAP authentication token (or put in `~/.fastmail_token`).                  |
| `FASTMAIL_INBOX_IDS`  | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`).             |
| `FASTMAIL_INBOX_ID`   | Yes*     | Single mailbox ID (legacy, use `FASTMAIL_INBOX_IDS` for multiple).          |
| `NOTIFY_CHANNEL`      | No       | Notification channel (default: `telegram`).                                 |
| `NOTIFY_TARGET`       | Yes      | Target ID for the notification channel.                                     |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.
