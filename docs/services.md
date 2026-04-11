---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services

OpenClaw services are background processes that keep long-running automations and shared runtimes available between conversations.

## Service Summary

| Service | Description | Docs |
|---------|-------------|------|
| 📡 FastMail SSE Service | Real-time email ingestion daemon. Connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. The current source is FastMail SSE, but the rule/action runtime is designed to be shared with future Outlook poll/webhook sources. | [Read more →](services/fastmail-sse) |
| 🔄 Shared Mail Runtime | Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (Fastmail SSE, Outlook, etc.) can plug into. | [Read more →](services/shared_mail_runtime) |

## 📡 FastMail SSE Service

Real-time email ingestion daemon. Connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. The current source is FastMail SSE, but the rule/action runtime is designed to be shared with future Outlook poll/webhook sources.

### Key Features

- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Deterministic mail rules: Top-level `mail_rules` for source/account/sender/subject matching
- Multi-mailbox monitoring: Monitor personal inbox + shared mailboxes simultaneously
- Package tracking detection: Automatically detect and register tracking numbers
- Meeting updates: Notify on calendar accept/decline/tentative responses
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

## 🔄 Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (Fastmail SSE, Outlook, etc.) can plug into.

### Key Features

- MailEnvelope — Normalized message shape consumed by rules and actions
- Rule engine — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry — Named action handlers with automatic body fetching and attachment downloading
- Provider protocol — `MailProviderClient` interface that sources implement to plug into the pipeline

### Environment Variables

_No environment variables required._

[Read more →](services/shared_mail_runtime)
