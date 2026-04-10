---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page provides an overview of background services available for integration. Each service is designed to solve specific operational challenges, such as real-time email ingestion or notification management. The services are modular and configurable, enabling developers and self-hosters to tailor them to their needs.

## Key Concepts

- Background services operate independently to handle specific tasks.
- Each service has unique features and configuration options.
- Environment variables are used to customize service behavior.
- Services are designed for extensibility and compatibility with future sources.

## FastMail SSE Service 📧

### Description

The FastMail SSE Service is a real-time email ingestion daemon. It connects to FastMail's JMAP EventSource, normalizes incoming messages into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. While currently focused on FastMail, the rule/action runtime is designed to support future sources like Outlook.

### Key Features

- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Per-account legacy rules: Preserve `notify_all`, `notify_meeting_updates`, and `detect_tracking`
- Deterministic mail rules: Top-level `mail_rules` for source/account/sender/subject matching
- Multi-mailbox monitoring: Monitor personal inbox + shared mailboxes simultaneously
- Package tracking detection: Automatically detect and register tracking numbers
- Meeting updates: Notify on calendar accept/decline/tentative responses
- USPS digest processing: Download images/body HTML, process scan vision, send USPS alerts, and structure results for follow-up
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

[Read more →](services/fastmail-sse)

### Environment Variables

| Name                  | Required | Description                                                   |
|-----------------------|----------|---------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN` | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)     |
| `FASTMAIL_INBOX_IDS`  | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`)|
| `FASTMAIL_INBOX_ID`   | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)        |
| `NOTIFY_CHANNEL`      | No       | Notification channel (default: `discord`)                    |
| `NOTIFY_TARGET`       | Yes      | Target ID for the notification channel                       |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.
