---
layout: default
title: Services
nav_order: 5
has_children: true
---

# Services

## Overview

OpenClaw's services provide background mail processing and automation. They enable real-time email ingestion, rule-based actions, and provider-agnostic workflows for personal and shared mailboxes. The architecture separates mail source adapters from a shared processing runtime, allowing flexible integration with multiple providers such as FastMail and Outlook.

These services solve the problem of automating email workflows—such as notifications, package tracking, and calendar updates—by normalizing incoming messages, matching deterministic rules, and executing actions. The modular design makes it easy to add new mail sources and customize behaviors.

## Key Concepts

- **Provider-agnostic mail pipeline:** Incoming mail is normalized and processed through shared rules and actions, regardless of the source.
- **MailEnvelope:** Standardized message format used for rule matching and action execution.
- **Rule engine:** Declarative JSON rules filter and trigger actions based on sender, subject, mailbox, and other criteria.
- **Action registry:** Named actions (e.g., notifications, package tracking) are registered and executed against matched messages.
- **Source adapters:** Integrate provider-specific mail sources (FastMail SSE, Outlook, etc.) into the shared runtime.

## How It Works

1. **Mail Source Integration:** Each mail provider (e.g., FastMail) connects via an adapter that streams or polls for new messages.
2. **Normalization:** Incoming messages are converted into a provider-agnostic `MailEnvelope`.
3. **Rule Matching:** The shared runtime evaluates ordered rules to determine which actions to run.
4. **Action Execution:** Actions are executed against the normalized envelope, with lazy fetching of bodies or attachments as needed.
5. **Result Dispatch:** Action results (such as notifications or package tracking updates) are handled by the integrating service.

---

## 📡 FastMail SSE Service

Real-time email ingestion daemon for FastMail accounts. Connects to FastMail's JMAP EventSource, normalizes each new message, matches deterministic rules, and runs Python actions. The rule/action runtime is shared with future Outlook poll/webhook sources.

### Purpose

- Provides real-time mail ingestion and automation for FastMail accounts.
- Supports multi-mailbox monitoring, package tracking, meeting notifications, and USPS digest processing.

### Key Features

- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Deterministic mail rules for source/account/sender/subject matching
- Monitor personal inbox and shared mailboxes simultaneously
- Automatic package tracking detection and registration
- Meeting response notifications (accept/decline/tentative)
- USPS digest processing with scan vision and structured follow-up
- Connects to JMAP SSE endpoint for real-time state changes
- Skips spam/noreply senders
- Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`

[Read more →](services/fastmail-sse)

### Environment Variables

| Variable               | Required | Description                                              |
|------------------------|----------|----------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN    | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)|
| FASTMAIL_INBOX_IDS     | Yes*     | Comma-separated mailbox IDs to monitor                   |
| FASTMAIL_INBOX_ID      | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)   |
| NOTIFY_CHANNEL         | No       | Notification channel (default: `discord`)                |
| NOTIFY_TARGET          | Yes      | Target ID for the notification channel                   |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

---

## 🔄 Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Any mail source (FastMail SSE, Outlook, etc.) can plug into this runtime to leverage normalized envelopes, rule matching, action registry, and dispatch loop.

### Purpose

- Centralizes mail processing logic for all providers.
- Enables consistent rule evaluation and action execution across mail sources.

### Key Features

- MailEnvelope: Normalized message shape consumed by rules and actions
- Rule engine: Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- Action registry: Named action handlers with automatic body fetching and attachment downloading
- Provider protocol: `MailProviderClient` interface for source integration

[Read more →](services/shared_mail_runtime)

### Environment Variables

_No environment variables required._

---
