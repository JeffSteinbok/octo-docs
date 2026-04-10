---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page describes the background services that power OpenClaw's mail pipeline. These services enable real-time email ingestion, provider-agnostic mail processing, rule-based automation, and notification delivery. The architecture is designed to support multiple mail sources and flexible rule/action pipelines, solving the problem of unified mail automation across personal and shared mailboxes.

## Key Concepts

- Real-time email ingestion from FastMail using JMAP SSE
- Provider-agnostic mail envelope model for consistent processing
- Rule matching engine for deterministic and legacy mail rules
- Action registry for executing Python actions on matched emails
- Multi-mailbox monitoring and notification delivery
- Automatic package tracking and meeting update notifications

---

## 📧 FastMail SSE Service

### Description

The FastMail SSE Service is a real-time email ingestion daemon. It connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. The rule/action runtime is designed to be shared with future Outlook poll/webhook sources.

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

| Variable               | Required | Description                                               |
|------------------------|----------|-----------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN    | Yes      | JMAP authentication token (or put in `~/.fastmail_token`) |
| FASTMAIL_INBOX_IDS     | Yes*     | Comma-separated mailbox IDs to monitor                    |
| FASTMAIL_INBOX_ID      | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)    |
| NOTIFY_CHANNEL         | No       | Notification channel (default: `discord`)                 |
| NOTIFY_TARGET          | Yes      | Target ID for the notification channel                    |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

---

## 🛠️ Shared Mail Runtime

### Description

The Shared Mail Runtime is a provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. It provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (FastMail SSE, Outlook, etc.) can plug into.

[Read more →](services/shared_mail_runtime)

### Key Features

- MailEnvelope — Normalized message shape consumed by rules and actions
- Rule engine — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry — Named action handlers with automatic body fetching and attachment downloading
- Provider protocol — `MailProviderClient` interface that sources implement to plug into the pipeline

---

## How It Works

1. **Email Ingestion**  
   FastMail SSE Service connects to FastMail's JMAP SSE endpoint and listens for real-time state changes.

2. **Normalization**  
   Incoming messages are normalized into a provider-agnostic envelope model.

3. **Rule Matching**  
   The shared mail runtime evaluates configured rules (legacy and deterministic) for each envelope. Rules can match on sender, subject, domain, body content, attachments, and more.

4. **Action Execution**  
   When a rule matches, the corresponding Python actions are executed. Actions include sending notifications, detecting package tracking numbers, processing USPS digests, and more.

5. **Notification Delivery**  
   Notifications are sent via the configured channel and target, such as Discord.

6. **Package Tracking**  
   If enabled, package tracking numbers are automatically extracted and registered. Delivery confirmations remove packages from tracking.

---

## Example Usage

### Notification Examples

**General email** (with `notify_all`):
```
📧 John Doe: Project update for Q1
```

**Meeting response** (with `notify_meeting_updates`):
```
👤 Jane Smith accepted 👍: Team standup meeting
```

**Multi-account** (2+ accounts configured):
```
[Personal] 📧 Amazon: Your order has shipped
[Work] 👤 Bob declined 👎: All-hands meeting
```

**Package detected** (with `detect_tracking`):
```
[fastmail-sse] 📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
```
