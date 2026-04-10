---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

OpenClaw uses a set of background services to provide real-time email ingestion, rule-based processing, and provider-agnostic mail workflows. These services enable automated actions such as notifications, package tracking, and calendar event updates across multiple mail sources and accounts.

Each service is designed to be modular and extensible, allowing external developers and self-hosters to configure mail pipelines, define custom rules, and integrate with notification channels.

## Key Concepts

- **Provider-agnostic mail pipeline**: Unified processing flow for emails from different sources.
- **Normalized envelope model**: Standardized message shape for rule matching and actions.
- **Rule engine**: Declarative JSON rules for filtering and triggering actions.
- **Action registry**: Named handlers for notifications, package tracking, and custom workflows.
- **Multi-mailbox monitoring**: Support for personal and shared mailboxes.
- **Notification integration**: Configurable channels and targets for alerts.

## How It Works

1. **Mail Source Connection**: Services connect to mail providers (e.g., FastMail via JMAP SSE) to receive new messages in real time.
2. **Normalization**: Incoming messages are normalized into a provider-agnostic envelope format.
3. **Rule Matching**: Each message is evaluated against configured rules, matching on sender, subject, body, and other fields.
4. **Action Execution**: When a rule matches, corresponding actions (such as notifications or package tracking) are executed.
5. **Notification Dispatch**: Alerts are sent to configured channels and targets.
6. **Package Tracking**: Tracking numbers are extracted and managed automatically.
7. **Multi-account Support**: Multiple accounts and mailboxes can be monitored simultaneously, with per-account rules and labels.

---

## 📧 FastMail SSE Service

Real-time email ingestion daemon. Connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. The rule/action runtime is designed to be shared with future Outlook poll/webhook sources.

[Read more →](services/fastmail-sse)

### Key Features

- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Per-account legacy rules: Preserve `notify_all`, `notify_meeting_updates`, and `detect_tracking`
- Deterministic mail rules: Top-level `mail_rules` for source/account/sender/subject matching
- Multi-mailbox monitoring: Monitor personal inbox + shared mailboxes simultaneously
- Package tracking detection: Automatically detect and register tracking numbers
- Meeting updates: Notify on calendar accept/decline/tentative responses
- USPS digest processing: Download images/body HTML, scan vision, send direct alert, hand structured result to main for memory/follow-up
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

### Environment Variables

| Name                  | Required | Description                                                        |
|-----------------------|----------|--------------------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN   | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)          |
| FASTMAIL_INBOX_IDS    | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`)     |
| FASTMAIL_INBOX_ID     | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)             |
| NOTIFY_CHANNEL        | No       | Notification channel (default: `discord`)                          |
| NOTIFY_TARGET         | Yes      | Target ID for the notification channel                             |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

---

## 🛠️ Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (Fastmail SSE, Outlook, etc.) can plug into.

[Read more →](services/shared_mail_runtime)

### Key Features

- MailEnvelope — Normalized message shape consumed by rules and actions
- Rule engine — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry — Named action handlers with automatic body fetching and attachment downloading
- Provider protocol — `MailProviderClient` interface that sources implement to plug into the pipeline

### Environment Variables

_No environment variables required._

---
