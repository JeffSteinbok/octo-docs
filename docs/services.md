---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page provides an overview of the background services powering OpenClaw's mail pipeline. These services enable real-time email ingestion, rule-based processing, and provider-agnostic workflows for notifications, package tracking, and calendar updates. Each service is designed to be modular, allowing integration with multiple mail providers and flexible rule/action pipelines.

## Key Concepts

- **Provider-agnostic mail processing**: All mail sources are normalized into a common envelope model for consistent rule evaluation and action handling.
- **Rule matching engine**: Declarative JSON rules allow filtering and processing based on sender, subject, domain, attachments, and more.
- **Action registry**: Named actions (such as notifications or package tracking) are triggered by matched rules.
- **Multi-mailbox monitoring**: Services can monitor multiple inboxes and shared mailboxes simultaneously.
- **Real-time ingestion**: Some services connect to provider event streams for immediate processing.

## How It Works

1. **Mail Source Connection**: Each service connects to its respective mail provider (e.g., FastMail via JMAP SSE).
2. **Message Normalization**: Incoming messages are transformed into a provider-agnostic envelope format.
3. **Rule Evaluation**: Rules are applied to each envelope, matching on sender, subject, body, and other fields.
4. **Action Dispatch**: When a rule matches, the corresponding actions (such as notifications or package tracking) are executed.
5. **Notification and Tracking**: Notifications are sent via configured channels, and package tracking is updated automatically.

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
- USPS digest processing: Download images/body HTML, scan vision, send direct alerts, and hand structured results to main for memory/follow-up
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

### Environment Variables

| Name                  | Required | Description                                               |
|-----------------------|----------|-----------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN   | Yes      | JMAP authentication token (or put in `~/.fastmail_token`) |
| FASTMAIL_INBOX_IDS    | Yes*     | Comma-separated mailbox IDs to monitor                    |
| FASTMAIL_INBOX_ID     | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)    |
| NOTIFY_CHANNEL        | No       | Notification channel (default: `discord`)                 |
| NOTIFY_TARGET         | Yes      | Target ID for the notification channel                    |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

---

## 🛠️ Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (FastMail SSE, Outlook, etc.) can plug into.

[Read more →](services/shared_mail_runtime)

### Key Features

- MailEnvelope — Normalized message shape consumed by rules and actions
- Rule engine — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry — Named action handlers with automatic body fetching and attachment downloading
- Provider protocol — `MailProviderClient` interface that sources implement to plug into the pipeline

### Environment Variables

This service does not require environment variables.

---
