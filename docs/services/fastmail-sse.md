---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email ingestion daemon that connects to FastMail's JMAP EventSource. It normalizes each new message into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. The service supports multi-mailbox monitoring, package tracking detection, and meeting update notifications, enabling flexible automation and notification workflows for external developers and self-hosters.

Designed for extensibility, FastMail SSE preserves legacy per-account rules and introduces a shared mail pipeline. It integrates seamlessly with OpenClaw for notifications and package tracking, and is built to support future mail sources beyond FastMail.

## Key Concepts

- Real-time email ingestion via FastMail JMAP SSE endpoint
- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Per-account rules system with legacy and deterministic rule types
- Multi-mailbox monitoring (personal and shared mailboxes)
- Package tracking detection and automatic management
- Meeting update notifications
- Notification delivery via OpenClaw channels

## Features

- **Shared mail pipeline**: Processes emails through a unified flow from source to envelope, rules, and Python actions.
- **Per-account legacy rules**: Supports `notify_all`, `notify_meeting_updates`, and `detect_tracking` for backward compatibility.
- **Deterministic mail rules**: Allows explicit rule matching on source, account, sender, and subject.
- **Multi-mailbox monitoring**: Monitors multiple mailboxes simultaneously, including shared mailboxes.
- **Package tracking detection**: Automatically detects and registers tracking numbers from carrier emails.
- **Meeting updates**: Notifies on calendar accept, decline, or tentative responses.
- **USPS digest processing**: Handles USPS Informed Delivery emails, downloads assets, performs scan vision, and sends structured alerts.
- **Spam/noreply sender filtering**: Skips notifications for spam and noreply senders.
- **Notification delivery**: Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`.

## Configuration

### Account Rules Config File

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

**Account ID**: FastMail JMAP account ID  
**Label**: Human-readable label for the account (displayed in notifications)

#### Legacy `accounts.*.rules`

| Rule                  | Description                                                         |
|-----------------------|---------------------------------------------------------------------|
| `notify_all`          | Notify on all incoming mail (minus spam/unsubscribe filter)         |
| `notify_meeting_updates` | Notify only on calendar accept/decline/tentative responses        |
| `detect_tracking`     | Scan email body for tracking numbers and register via OpenClaw      |

- `notify_all`: All emails trigger notifications (subject to spam filtering)
- `notify_meeting_updates`: Only calendar responses trigger notifications
- `detect_tracking`: Email bodies are scanned for carrier tracking numbers and auto-added to OpenClaw package tracking
- Multiple rules can be combined

### Deterministic `mail_rules`

Rules are evaluated in order; set `"continue": true` to evaluate later rules.

Supported match fields:

| Field                  | Meaning                                      |
|------------------------|----------------------------------------------|
| `sender_email`         | Exact sender address match                   |
| `sender_domain`        | Sender domain or subdomain match             |
| `sender_name_contains` | Case-insensitive sender-name substring       |
| `subject`              | Exact subject match                          |
| `subject_contains`     | Case-insensitive subject substring           |
| `subject_prefix`       | Case-insensitive subject prefix              |
| `subject_regex`        | Case-insensitive regex                       |
| `body_contains`        | Case-insensitive substring across body       |
| `has_attachments`      | Boolean attachment hint                      |

Built-in actions:

| Action                | Behavior                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `notify_email`        | Formats and sends the email notification                                 |
| `detect_tracking`     | Runs the package-tracking extractor/add-remove flow                      |
| `process_usps_digest` | Downloads assets, stages scan vision, sends USPS notifications, forwards summary |

### Environment Variables

| Variable               | Required | Description                                              |
|------------------------|----------|----------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN`  | Yes      | JMAP authentication token (or in `~/.fastmail_token`)    |
| `FASTMAIL_INBOX_IDS`   | Yes*     | Comma-separated mailbox IDs to monitor                   |
| `FASTMAIL_INBOX_ID`    | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)   |
| `NOTIFY_CHANNEL`       | No       | Notification channel (default: `discord`)                |
| `NOTIFY_TARGET`        | Yes      | Target ID for the notification channel                   |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

### Configuration Examples

#### Example 1: Personal + Work Accounts

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

- Personal: Notifications for all emails + auto-track packages
- Work: Notifications only for meeting responses

#### Example 2: Package Tracking Only

```json
{
  "accounts": {
    "<account-id>": {
      "label": "Shopping",
      "rules": ["detect_tracking"]
    }
  }
}
```

- No notifications, but all tracking numbers are auto-registered

#### Example 3: USPS Informed Delivery via action pipeline

```json
{
  "accounts": {
    "<account-id>": {
      "label": "jeff@steinbok.net",
      "rules": ["notify_all"]
    }
  },
  "mail_rules": [
    {
      "id": "usps-informed-delivery",
      "accounts": ["<account-id>"],
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
            "vision_agent": "mail",
            "vision_backend": "auto"
          }
        }
      ],
      "continue": true
    },
    {
      "id": "forwarded-usps-informed-delivery",
      "accounts": ["<account-id>"],
      "match": {
        "sender_email": "jeff@steinbok.net",
        "subject_contains": ["Informed Delivery", "Daily Digest"],
        "body_contains": ["USPS", "Informed Delivery"]
      },
      "actions": [
        {
          "name": "process_usps_digest",
          "params": {
            "agent": "main",
            "workspace_agent": "mail",
            "memory_agent": "main",
            "vision_agent": "mail",
            "vision_backend": "auto"
          }
        }
      ],
      "continue": true
    }
  ]
}
```

- Downloads digest assets, performs scan vision, sends USPS notifications, and forwards structured summary

#### Example 4: Multiple Mailboxes (Personal + Shared)

```json
{
  "accounts": {
    "<account-id>": {
      "label": "john@example.com",
      "rules": ["notify_all", "detect_tracking"]
    }
  }
}
```

Environment variable:

```bash
FASTMAIL_INBOX_IDS=personal_inbox_id,shared_team_inbox_id
```

Notifications include mailbox name:

```
[Inbox] 📧 John Doe: Meeting tomorrow
[Shared Team] 📧 Jane Smith: Project update
```

## Package Tracking

When `detect_tracking` is enabled, the daemon uses a rules-based extraction pipeline:

### Extraction Pipeline

1. **Sender allowlist check**  
   Only scans emails from known carriers and retailers:
   - `ups.com`, `fedex.com`, `usps.com`, `dhl.com`, `amazon.com`, `narvar.com`, `aftership.com`, `shipbob.com`, `shipstation.com`, `easypost.com`, `noreply@nespresso.com`

2. **Inline regex scan**  
   Scans email body for carrier tracking number patterns:
   - **UPS**: `1Z[A-Z0-9]{16}`
   - **FedEx**: 12, 15, or 20-digit numbers
   - **USPS**: 20-22 digit numbers (often starts with 94, 92, 93, or 95)
   - **Amazon**: `TBA[0-9]{12}US`

3. **URL parameter extraction**  
   Extracts tracking numbers from URLs in the email:

   | URL pattern                | Example tracking param         |
   |---------------------------|-------------------------------|
   | `narvar.com/...`          | `?tracking_numbers=1Z...`     |
   | `ups.com/track...`        | `?tracknum=1Z...`             |
   | `fedex.com/...track...`   | `?trknbr=...`                 |
   | `usps.com/...`            | `?qtc_tLabels1=...`           |
   | `amazon.com/...track...`  | `?tracking-id=TBA...`         |

4. **Narvar link following**  
   If a `narvar.com` URL lacks a tracking number, performs HTTP GET and parses tracking from HTML.

### Automatic Package Management

- Packages are added to OpenClaw tracking with descriptive labels.
- Delivery confirmation emails trigger automatic removal from tracking.
- Logs each package addition:
  ```
  📦 added package: 1Z999AA10123456784 (UPS) — Personal: ...
  ```
- View tracked packages:
  ```
  openclaw tool call --plugin package-tracking --tool package_list
  ```

## Systemd Service Setup

- Enable and start:
  ```
  systemctl --user enable fastmail-sse && systemctl --user start fastmail-sse
  ```
- Status:
  ```
  systemctl --user status fastmail-sse
  ```
- Logs:
  ```
  journalctl --user -u fastmail-sse -f
  ```

## Notification Format Examples

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
