---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email ingestion daemon that connects to FastMail's JMAP EventSource. It normalizes incoming messages into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. This service supports multi-mailbox monitoring, package tracking detection, meeting updates, and real-time notifications.

## Features

- **Shared mail pipeline**: `source -> envelope -> rules -> Python actions`
- **Per-account legacy rules**: Preserve `notify_all`, `notify_meeting_updates`, and `detect_tracking`
- **Deterministic mail rules**: Top-level `mail_rules` for source/account/sender/subject matching
- **Multi-mailbox monitoring**: Monitor personal inbox and shared mailboxes simultaneously
- **Package tracking detection**: Automatically detect and register tracking numbers
- **Meeting updates**: Notify on calendar accept/decline/tentative responses
- **USPS digest processing**: Download images/body HTML, perform scan vision, send USPS alerts, and forward structured results
- **Connects to JMAP SSE endpoint**: Real-time state changes
- **Spam/noreply filtering**: Skips irrelevant senders
- **Notification delivery**: Sends notifications via `openclaw message send`

## Configuration

### Account Rules Config File

Create a configuration file at `~/.openclaw/services/fastmail-sse-config.json`:

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
        {
          "name": "process_usps_digest",
          "params": {
            "agent": "main",
            "workspace_agent": "mail",
            "memory_agent": "main",
            "vision_agent": "mail"
          }
        }
      ],
      "continue": true
    }
  ]
}
```

#### Legacy Rules

| Rule                  | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `notify_all`          | Notify on all incoming mail (excluding spam/unsubscribe filter)            |
| `notify_meeting_updates` | Notify only on calendar accept/decline/tentative responses               |
| `detect_tracking`     | Scan email body for tracking numbers and register via OpenClaw package tracking |

#### Deterministic `mail_rules`

Supported match fields:

| Field                | Meaning                                   |
|----------------------|-------------------------------------------|
| `sender_email`       | Exact sender address match               |
| `sender_domain`      | Sender domain or subdomain match         |
| `subject_contains`   | Case-insensitive subject substring       |
| `body_contains`      | Case-insensitive substring across body   |
| `has_attachments`    | Boolean attachment hint                  |

Built-in actions:

| Action               | Behavior                                 |
|----------------------|-------------------------------------------|
| `notify_email`       | Formats and sends the email notification |
| `detect_tracking`    | Runs the package-tracking extractor flow |
| `process_usps_digest`| Processes USPS digest emails             |

### Environment Variables

| Variable              | Required | Description                                      |
|-----------------------|----------|--------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN` | Yes      | JMAP authentication token                       |
| `FASTMAIL_INBOX_IDS`  | Yes*     | Comma-separated mailbox IDs to monitor          |
| `FASTMAIL_INBOX_ID`   | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple) |
| `NOTIFY_CHANNEL`      | No       | Notification channel (default: `discord`)       |
| `NOTIFY_TARGET`       | Yes      | Target ID for the notification channel          |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

## Package Tracking

When the `detect_tracking` rule is active, the daemon applies a rules-based extraction pipeline to identify and manage package tracking numbers.

### Extraction Pipeline

1. **Sender allowlist check**: Scans emails from known shipping carriers and retailers.
2. **Inline regex scan**: Detects tracking numbers using carrier-specific patterns:
   - **UPS**: `1Z[A-Z0-9]{16}`
   - **FedEx**: 12, 15, or 20-digit numbers
   - **USPS**: 20-22 digit numbers
   - **Amazon**: `TBA[0-9]{12}US`
3. **URL parameter extraction**: Extracts tracking numbers from shipping/tracking URLs.
4. **Narvar link following**: Parses tracking numbers from `narvar.com` pages when necessary.

### Automatic Package Management

- **Add on detect**: Automatically adds detected packages to OpenClaw tracking.
- **Auto-remove on delivery confirmation**: Removes packages upon delivery confirmation.

## Systemd Service

Install and manage the FastMail SSE service using systemd:

- Enable and start:  
  ```bash
  systemctl --user enable fastmail-sse && systemctl --user start fastmail-sse
  ```
- Check status:  
  ```bash
  systemctl --user status fastmail-sse
  ```
- View logs:  
  ```bash
  journalctl --user -u fastmail-sse -f
  ```

## Notification Examples

**General email**:  
```
📧 John Doe: Project update for Q1
```

**Meeting response**:  
```
👤 Jane Smith accepted 👍: Team standup meeting
```

**Multi-account**:  
```
[Personal] 📧 Amazon: Your order has shipped  
[Work] 👤 Bob declined 👎: All-hands meeting
```

**Package detected**:  
```
[fastmail-sse] 📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
```
