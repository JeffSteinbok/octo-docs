---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page provides an introduction to the background services powering OpenClaw's mail pipeline. These services enable real-time email ingestion, provider-agnostic mail processing, deterministic rule matching, and automated actions such as notifications and package tracking. The architecture is designed for extensibility, allowing multiple mail sources to plug into a shared runtime.

## Key Concepts

- Real-time email ingestion via FastMail's JMAP EventSource
- Provider-agnostic mail envelope model for consistent processing
- Declarative rule matching for deterministic actions
- Action registry for extensible mail handling
- Multi-mailbox monitoring and notification routing
- Automated package tracking and meeting update detection

## How It Works

1. Incoming emails are ingested in real-time from FastMail (via SSE) or other providers.
2. Each message is normalized into a provider-agnostic envelope.
3. The envelope passes through a rule engine, matching on sender, subject, body, and other fields.
4. Matched rules trigger registered actions, such as sending notifications or extracting tracking numbers.
5. Actions are executed in a shared runtime, enabling consistent behavior across mail sources.
6. Notifications and package tracking updates are dispatched as configured.

---

## 📧 FastMail SSE Service

Real-time email ingestion daemon. Connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. The current source is FastMail SSE, but the rule/action runtime is designed to be shared with future Outlook poll/webhook sources.

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

[Read more →](services/fastmail-sse)

#### Environment Variables

| Variable                | Required | Description                                                        |
|-------------------------|----------|--------------------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN     | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)          |
| FASTMAIL_INBOX_IDS      | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`)     |
| FASTMAIL_INBOX_ID       | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)             |
| NOTIFY_CHANNEL          | No       | Notification channel (default: `discord`)                          |
| NOTIFY_TARGET           | Yes      | Target ID for the notification channel                             |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

---

## 🛠️ Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (Fastmail SSE, Outlook, etc.) can plug into.

### Key Features

- MailEnvelope — Normalized message shape consumed by rules and actions
- Rule engine — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry — Named action handlers with automatic body fetching and attachment downloading
- Provider protocol — `MailProviderClient` interface that sources implement to plug into the pipeline

[Read more →](services/shared_mail_runtime)
