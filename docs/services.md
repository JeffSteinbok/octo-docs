---
layout: default
title: Services
nav_order: 5
---

# Services

OpenClaw services are background processes that keep long-running automations available between conversations.

Shared runtime subsystems such as the mail runtime are documented separately under [Mail Runtime](mail-runtime).

## Service Summary

| Service | Description | Docs |
|---------|-------------|------|
| 📡 ⚡ FastMail SSE Service | Real-time email ingestion daemon that acts as the FastMail-specific adapter over the [shared mail runtime](../../libs/ts/mail_runtime_core/README.md). It connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and invokes shared/runtime-registered mail actions. The current source is FastMail SSE, but the underlying mail runtime is designed to be reused by future Outlook poll/webhook sources. | [Read more →](services/fastmail-sse) |

## 📡 ⚡ FastMail SSE Service

Real-time email ingestion daemon that acts as the FastMail-specific adapter over the [shared mail runtime](../../libs/ts/mail_runtime_core/README.md). It connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and invokes shared/runtime-registered mail actions. The current source is FastMail SSE, but the underlying mail runtime is designed to be reused by future Outlook poll/webhook sources.

### Key Features

- Shared mail pipeline: `source -> envelope -> rules -> actions`
- Deterministic mail rules: Top-level `mail_rules` for source/account/sender/subject matching
- Multi-mailbox monitoring: Monitor personal inbox + shared mailboxes simultaneously
- Package tracking detection: Automatically detect and register tracking numbers
- Meeting updates: Notify on calendar accept/decline/tentative responses
- Config hot-reload: Watches config file and hot-reloads `mail_rules` without restart
- USPS digest processing: Download images/body HTML, have the mail agent do scan vision, let the USPS runtime send its direct alert, then hand the structured result to main for memory/follow-up
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FASTMAIL_JMAP_TOKEN` | Yes | JMAP authentication token (or put in `~/.fastmail_token`) |
| `FASTMAIL_INBOX_IDS` | Yes | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`) |
| `FASTMAIL_INBOX_ID` | Yes | Single mailbox ID (legacy, use INBOX_IDS for multiple) |
| `NOTIFY_CHANNEL` | No | Notification channel (default: `discord`) |
| `NOTIFY_TARGET` | Yes | Target ID for the notification channel |

[Read more →](services/fastmail-sse)
