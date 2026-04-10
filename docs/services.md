---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services

## Overview

OpenClaw includes a set of background services that enable real-time email ingestion, rule-based processing, and provider-agnostic mail workflows. These services solve the problem of integrating multiple mail sources (such as FastMail and Outlook) into a unified pipeline, allowing deterministic rule matching, action execution, and notification delivery.

Each service is designed to be modular and extensible, supporting custom rules, actions, and multi-mailbox monitoring. The shared mail runtime ensures consistent processing regardless of the underlying provider, while specialized ingestion daemons handle real-time updates and source-specific features.

## Key Concepts

- **Provider-agnostic mail pipeline**: Unified processing for emails from different sources.
- **Normalized envelope model**: Standardized message structure for rule matching and actions.
- **Rule engine**: Declarative JSON rules for filtering and triggering actions.
- **Action registry**: Named handlers for notifications, tracking, and custom workflows.
- **Multi-mailbox monitoring**: Support for personal and shared mailboxes.
- **Real-time ingestion**: Immediate processing of new messages via streaming endpoints.

## How It Works

1. **Mail Source Connection**: Each ingestion daemon connects to its provider (e.g., FastMail's JMAP EventSource).
2. **Envelope Normalization**: Incoming messages are transformed into a provider-agnostic envelope.
3. **Rule Evaluation**: The shared runtime applies deterministic and legacy rules to each envelope.
4. **Action Execution**: Matching rules trigger registered actions (e.g., notifications, package tracking).
5. **Notification Delivery**: Actions send notifications to configured channels and targets.
6. **Package Tracking**: Emails are scanned for tracking numbers and managed automatically.
7. **Multi-account Support**: Rules and actions can be configured per account and mailbox.

---

## 📧 FastMail SSE Service

Real-time email ingestion daemon for FastMail accounts. Connects to FastMail's JMAP EventSource, normalizes each new message, applies deterministic and legacy rules, and executes Python actions. Designed for extensibility to future mail sources.

**Key Features:**
- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Per-account legacy rules: `notify_all`, `notify_meeting_updates`, `detect_tracking`
- Deterministic mail rules: Match on source/account/sender/subject/body
- Multi-mailbox monitoring: Personal and shared mailboxes
- Package tracking detection: Automatic extraction and registration
- Meeting updates: Notify on calendar responses
- USPS digest processing: Download assets, scan vision, structured follow-up
- Real-time updates via JMAP SSE
- Spam/noreply sender filtering
- Notification delivery via `openclaw message send`

**Environment Variables**

| Name                  | Required | Description                                               |
|-----------------------|----------|-----------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN   | Yes      | JMAP authentication token (or put in `~/.fastmail_token`) |
| FASTMAIL_INBOX_IDS    | Yes*     | Comma-separated mailbox IDs to monitor                    |
| FASTMAIL_INBOX_ID     | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)    |
| NOTIFY_CHANNEL        | No       | Notification channel (default: `discord`)                 |
| NOTIFY_TARGET         | Yes      | Target ID for the notification channel                    |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

[Read more →](services/fastmail-sse)

---

## 🔄 Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Offers a normalized envelope model, rule matching engine, action registry, and dispatch loop. Any mail source (FastMail SSE, Outlook, etc.) can integrate via the provider protocol.

**Key Features:**
- MailEnvelope: Standardized message shape for rules and actions
- Rule engine: Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry: Named action handlers with automatic body fetching and attachment downloading
- Provider protocol: `MailProviderClient` interface for source integration

[Read more →](services/shared_mail_runtime)
