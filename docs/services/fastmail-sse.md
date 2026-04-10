---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email ingestion daemon that connects to FastMail's JMAP EventSource. It normalizes incoming messages into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. This service enables real-time email monitoring, notification delivery, and automation for tasks such as package tracking and meeting updates.

## Features

- **Shared mail pipeline**: `source -> envelope -> rules -> Python actions`
- **Per-account legacy rules**: Supports `notify_all`, `notify_meeting_updates`, and `detect_tracking`
- **Deterministic mail rules**: Enables source/account/sender/subject matching with customizable actions
- **Multi-mailbox monitoring**: Simultaneously monitor personal and shared mailboxes
- **Package tracking detection**: Automatically detects and registers tracking numbers
- **Meeting updates**: Sends notifications for calendar accept/decline/tentative responses
- **USPS digest processing**: Handles USPS emails for image and HTML processing, vision analysis, and structured output
- **Real-time updates**: Connects to JMAP SSE endpoint for instant state changes
- **Spam filtering**: Automatically skips spam and noreply senders
- **Custom notifications**: Sends notifications via `openclaw message send` to specified channels and targets

## Configuration

### Account Rules Config File

Create a configuration file at `~/.openclaw/services/fastmail-sse-config.json`. Below is an example configuration:

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

### Legacy Rules

| Rule                  | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `notify_all`          | Notify on all incoming mail (excluding spam/unsubscribe filter)            |
| `notify_meeting_updates` | Notify only on calendar accept/decline/tentative responses                |
| `detect_tracking`     | Scan email body for tracking numbers and register via OpenClaw package tracking |

### Deterministic `mail_rules`

Top-level `mail_rules` allow explicit actions to be attached to deterministic matches. Rules are evaluated in order, and by default, the pipeline stops at the first match unless `continue` is set to `true`.

Supported match fields include:

| Field                | Description                              |
|----------------------|------------------------------------------|
| `sender_email`       | Exact sender address match              |
| `sender_domain`      | Sender domain or subdomain match        |
| `sender_name_contains` | Case-insensitive sender-name substring |
| `subject`            | Exact subject match                     |
| `subject_contains`   | Case-insensitive subject substring      |
| `subject_prefix`     | Case-insensitive subject prefix         |
| `subject_regex`      | Case-insensitive regex                  |
| `body_contains`      | Case-insensitive substring across text and HTML body |
| `has_attachments`    | Boolean attachment hint                 |

Built-in actions include:

| Action               | Description                              |
|----------------------|------------------------------------------|
| `notify_email`       | Formats and sends the email notification |
| `detect_tracking`    | Runs the package-tracking extractor/add-remove flow |
| `process_usps_digest` | Processes USPS digest emails, including image and HTML parsing |

### Environment Variables

| Variable              | Required | Description                                                |
|-----------------------|----------|------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN` | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)  |
| `FASTMAIL_INBOX_IDS`  | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`) |
| `FASTMAIL_INBOX_ID`   | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)     |
| `NOTIFY_CHANNEL`      | No       | Notification channel (default: `discord`)                 |
| `NOTIFY_TARGET`       | Yes      | Target ID for the notification channel                    |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

## Package Tracking

When the `detect_tracking` rule is active, the daemon applies a rules-based extraction pipeline to identify and register tracking numbers.

### Extraction Pipeline

1. **Sender allowlist check**: Only scans emails from known carriers and retailers (e.g., `ups.com`, `fedex.com`, `usps.com`, `amazon.com`).
2. **Inline regex scan**: Identifies tracking numbers using carrier-specific patterns.
3. **URL parameter extraction**: Extracts tracking numbers from embedded URLs.
4. **Narvar link following**: Retrieves tracking numbers from `narvar.com` links by parsing their HTML content.

### Automatic Package Management

- Detected packages are automatically added to OpenClaw package tracking with descriptive labels.
- Packages are automatically removed from tracking upon delivery confirmation.
- Logs each added package for tracking.

## Notification Examples

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

## Systemd Service

To manage the FastMail SSE service using systemd:

- **Enable and start the service**:  
  ```bash
  systemctl --user enable fastmail-sse && systemctl --user start fastmail-sse
  ```

- **Check service status**:  
  ```bash
  systemctl --user status fastmail-sse
  ```

- **View logs**:  
  ```bash
  journalctl --user -u fastmail-sse -f
  ```
