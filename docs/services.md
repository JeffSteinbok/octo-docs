---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page provides an introduction to the background services powering OpenClaw's mail pipeline. These services enable real-time email ingestion, provider-agnostic mail processing, rule-based automation, and notification delivery. The architecture is designed for extensibility, allowing multiple mail sources (such as FastMail SSE and Outlook) to plug into a shared runtime.

## Key Concepts

- Real-time email ingestion and processing
- Provider-agnostic mail envelope normalization
- Rule-based automation for mail actions
- Multi-mailbox and multi-account monitoring
- Notification delivery via configurable channels
- Extensible pipeline for future mail sources

## How It Works

1. Mail sources (e.g., FastMail SSE) connect to provider endpoints and ingest new messages in real time.
2. Each message is normalized into a provider-agnostic envelope model.
3. Deterministic rules and legacy per-account rules are evaluated to match incoming messages.
4. Matching rules trigger Python actions, such as sending notifications or extracting package tracking numbers.
5. The shared mail runtime provides the rule engine, action registry, and dispatch loop, enabling any mail source to integrate seamlessly.
6. Notifications and structured outputs are sent to configured channels and targets.

---

## 📧 FastMail SSE Service

Real-time email ingestion daemon. Connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. The rule/action runtime is designed to be shared with future Outlook poll/webhook sources.

### Key Features

- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Per-account legacy rules: Preserve `notify_all`, `notify_meeting_updates`, and `detect_tracking`
- Deterministic mail rules: Top-level `mail_rules` for source/account/sender/subject matching
- Multi-mailbox monitoring: Monitor personal inbox + shared mailboxes simultaneously
- Package tracking detection: Automatically detect and register tracking numbers
- Meeting updates: Notify on calendar accept/decline/tentative responses
- USPS digest processing: Download images/body HTML, scan vision, send USPS alerts, and hand structured results to main for memory/follow-up
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

### Environment Variables

| Variable               | Required | Description                                                    |
|------------------------|----------|----------------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN    | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)      |
| FASTMAIL_INBOX_IDS     | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`) |
| FASTMAIL_INBOX_ID      | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)         |
| NOTIFY_CHANNEL         | No       | Notification channel (default: `discord`)                      |
| NOTIFY_TARGET          | Yes      | Target ID for the notification channel                         |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

[Read more →](services/fastmail-sse)

---

## 🛠️ Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (Fastmail SSE, Outlook, etc.) can plug into.

### Key Features

- MailEnvelope — Normalized message shape consumed by rules and actions
- Rule engine — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry — Named action handlers with automatic body fetching and attachment downloading
- Provider protocol — `MailProviderClient` interface that sources implement to plug into the pipeline

[Read more →](services/shared_mail_runtime)
