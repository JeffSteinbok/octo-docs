---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## FastMail SSE Service 📧

Real-time email ingestion daemon that connects to FastMail's JMAP EventSource. It normalizes incoming messages into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. Designed to support future mail sources like Outlook.

### Key Features
- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Multi-mailbox monitoring: Monitor personal inbox and shared mailboxes simultaneously
- Deterministic mail rules for source/account/sender/subject matching
- Package tracking detection and automatic registration
- Meeting updates: Notify on calendar accept/decline/tentative responses
- USPS digest processing: Download images/body HTML, perform scan vision, and send structured results
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

[Read more →](services/fastmail-sse)

### Environment Variables
| Variable               | Required | Description                                                   |
|------------------------|----------|---------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN`  | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)     |
| `FASTMAIL_INBOX_IDS`   | Yes      | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`)|
| `FASTMAIL_INBOX_ID`    | Yes      | Single mailbox ID (legacy, use `FASTMAIL_INBOX_IDS` for multiple) |
| `NOTIFY_CHANNEL`       | No       | Notification channel (default: `discord`)                    |
| `NOTIFY_TARGET`        | Yes      | Target ID for the notification channel                       |

---

## Shared Mail Runtime 📬

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. It provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source can integrate with.

### Key Features
- **MailEnvelope**: Normalized message shape consumed by rules and actions
- **Rule engine**: Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- **Action registry**: Named action handlers with automatic body fetching and attachment downloading
- **Provider protocol**: `MailProviderClient` interface for mail source integration

[Read more →](services/shared_mail_runtime)
