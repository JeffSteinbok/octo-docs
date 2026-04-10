---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services Overview

## Overview

OpenClaw provides a set of background services for real-time email ingestion and provider-agnostic mail processing. These services enable automated workflows such as rule-based notifications, package tracking, and calendar event updates. The architecture is designed to support multiple mail sources and shared processing pipelines, making it flexible for both personal and team use.

## Key Concepts

- **Provider-agnostic mail pipeline**: All mail sources are normalized into a common envelope model and processed through shared rules and actions.
- **Rule matching engine**: Declarative rules allow filtering and triggering actions based on sender, subject, body, and attachments.
- **Action registry**: Named actions (such as notifications or package tracking) are executed when rules match.
- **Multi-mailbox monitoring**: Supports monitoring multiple inboxes and shared mailboxes simultaneously.
- **Real-time ingestion**: Services connect to mail providers for immediate processing of new messages.

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
- USPS digest processing: Download images/body HTML, scan vision, send USPS alerts, and hand structured results to main for memory/follow-up
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

## How It Works

1. **Mail Source Connection**: Services connect to mail providers (e.g., FastMail via JMAP SSE) to receive new messages in real time.
2. **Envelope Normalization**: Each incoming message is normalized into a provider-agnostic envelope model.
3. **Rule Evaluation**: The envelope is processed through a rule engine, which matches based on sender, subject, body, and other attributes.
4. **Action Dispatch**: When a rule matches, the corresponding action (such as notification or package tracking) is executed.
5. **Notification and Tracking**: Actions can send notifications, detect package tracking numbers, or process calendar updates.

---

## Example Usage

### FastMail SSE Service Configuration

Create `~/.openclaw/services/fastmail-sse-config.json`:

```json
{
  "accounts": {
    "<account-id-1>": {
      "label": "assistant@example.com",
      "rules": ["notify_meeting_updates", "detect_tracking"]
    },
    "<account-id-2>": {
      "label": "personal@example.com",
      "rules": ["notify_all", "detect_tracking"]
    }
  },
  "mail_rules": [
    {
      "id": "usps-informed-delivery",
      "accounts": ["<account-id-2>"],
      "match": {
        "sender_domain": "usps.com",
        "subject_contains": ["Informed Delivery", "Daily Digest"]
      },
      "actions": [
        {"name": "process_usps_digest", "params": {"agent": "main", "workspace_agent": "mail", "memory_agent": "main", "vision_agent": "mail"}}
      ],
      "continue": true
    },
    {
      "id": "forwarded-usps-informed-delivery",
      "accounts": ["<account-id-2>"],
      "match": {
        "sender_email": "you@example.com",
        "subject_contains": ["Informed Delivery", "Daily Digest"],
        "body_contains": ["USPS", "Informed Delivery"]
      },
      "actions": [
        {"name": "process_usps_digest", "params": {"agent": "main", "workspace_agent": "mail", "memory_agent": "main", "vision_agent": "mail"}}
      ],
      "continue": true
    }
  ]
}
```

**Result**: The daemon downloads USPS digest assets, performs scan-image vision, sends USPS notifications directly, and hands the structured summary to `main` for durable memory and follow-up.

---

### Notification Examples

- **General email** (with `notify_all`):
  ```
  📧 John Doe: Project update for Q1
  ```
- **Meeting response** (with `notify_meeting_updates`):
  ```
  👤 Jane Smith accepted 👍: Team standup meeting
  ```
- **Multi-account** (2+ accounts configured):
  ```
  [Personal] 📧 Amazon: Your order has shipped
  [Work] 👤 Bob declined 👎: All-hands meeting
  ```
- **Package detected** (with `detect_tracking`):
  ```
  [fastmail-sse] 📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
  ```
