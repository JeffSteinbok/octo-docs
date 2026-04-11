---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

This page provides an introduction to the background services powering OpenClaw's mail pipeline. These services enable real-time email ingestion, provider-agnostic mail processing, rule-based automation, and notification delivery. The architecture is designed to support multiple mail sources and flexible rule/action pipelines, solving the problem of unified mail automation across personal and shared inboxes.

## Key Concepts

- Real-time email ingestion and processing
- Provider-agnostic mail envelope normalization
- Rule-based matching and action execution
- Multi-mailbox and multi-account support
- Notification and package tracking automation

---

## 📧 FastMail SSE Service

### Description

The FastMail SSE Service is a real-time email ingestion daemon. It connects to FastMail's JMAP EventSource, normalizes each new message into a provider-agnostic mail envelope, matches deterministic rules, and runs Python actions. While the current source is FastMail SSE, the rule/action runtime is designed to be shared with future Outlook poll/webhook sources.

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

| Name                   | Required | Description                                                        |
|------------------------|----------|--------------------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN    | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)          |
| FASTMAIL_INBOX_IDS     | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`)     |
| FASTMAIL_INBOX_ID      | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)             |
| NOTIFY_CHANNEL         | No       | Notification channel (default: `discord`)                          |
| NOTIFY_TARGET          | Yes      | Target ID for the notification channel                             |

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

1. **Mail Source Connection**  
   Services connect to mail providers (e.g., FastMail via JMAP SSE) to receive new messages in real time.

2. **Envelope Normalization**  
   Incoming messages are normalized into a provider-agnostic envelope format, enabling consistent rule processing regardless of source.

3. **Rule Matching**  
   Each envelope is evaluated against configured rules. Rules can match on sender, subject, domain, body content, attachments, and more.

4. **Action Execution**  
   When a rule matches, the associated actions are executed. Actions include sending notifications, detecting package tracking numbers, processing USPS digests, and more.

5. **Notification & Automation**  
   Notifications are sent via configured channels, and package tracking is automatically managed based on detected tracking numbers and delivery confirmations.

---

## Example Usage

### FastMail SSE Service Configuration

Create `~/.openclaw/services/fastmail-sse-config.json`:

```json
{
  "accounts": {
    "<account-id-1>": {
      "label": "Personal",
      "rules": ["notify_all", "detect_tracking"]
    },
    "<account-id-2>": {
      "label": "Work",
      "rules": ["notify_meeting_updates"]
    }
  }
}
```

**Result**:
- Personal account: Get notified for all emails and auto-track packages.
- Work account: Only get notified for meeting responses.

---

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
