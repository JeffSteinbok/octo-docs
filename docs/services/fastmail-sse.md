---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email ingestion daemon that connects to FastMail's JMAP EventSource. It normalizes each new message into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. The service enables automated workflows such as package tracking, meeting notifications, and multi-mailbox monitoring, providing timely alerts and structured mail processing.

Designed for extensibility, the rule/action runtime is shared across mail sources, allowing future integration with Outlook poll/webhook sources. The FastMail SSE Service streamlines mail handling, reduces manual triage, and automates actionable notifications.

## Key Concepts

- **Mail Pipeline:** Processes incoming mail through a shared pipeline: source → envelope → rules → Python actions.
- **Deterministic Mail Rules:** Uses top-level `mail_rules` for matching by source, account, sender, or subject.
- **Multi-Mailbox Monitoring:** Supports simultaneous monitoring of personal and shared mailboxes.
- **Package Tracking Detection:** Automatically extracts and registers tracking numbers from carrier emails.
- **Meeting Updates:** Notifies on calendar accept, decline, or tentative responses.
- **USPS Digest Processing:** Handles USPS Informed Delivery digests with vision analysis and structured follow-up.
- **Real-Time State Changes:** Connects to FastMail's JMAP SSE endpoint for immediate updates.
- **Notification Dispatch:** Sends notifications via `openclaw message send` to configured channels and targets.

## Features

| Feature | Description |
|---------|-------------|
| Shared mail pipeline | Processes mail through `source → envelope → rules → Python actions` |
| Deterministic mail rules | Top-level `mail_rules` for source/account/sender/subject matching |
| Multi-mailbox monitoring | Monitor personal inbox and shared mailboxes simultaneously |
| Package tracking detection | Automatically detect and register tracking numbers |
| Meeting updates | Notify on calendar accept/decline/tentative responses |
| USPS digest processing | Download images/body HTML, perform scan vision, send direct alerts, and hand off structured results |
| Real-time state changes | Connects to JMAP SSE endpoint for live updates |
| Spam/noreply skipping | Ignores spam and noreply senders |
| Notification dispatch | Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>` |

## Configuration

### FastMail Config File

Create `~/.openclaw/services/fastmail-sse-config.json`:

```json
{
  "accounts": {
    "<account-id-1>": {
      "label": "assistant@example.com"
    },
    "<account-id-2>": {
      "label": "personal@example.com"
    }
  },
  "mail_rules": [
    {
      "id": "notify-all",
      "accounts": ["<account-id-2>"],
      "actions": [{"name": "notify_email"}]
    }
  ]
}
```

- **Account ID:** FastMail JMAP account ID.
- **Label:** Human-readable label for the account (used in notifications).

### Rule Types

- **notify_all:** Sends notifications for all matched emails.
- **notify_meeting_updates:** Notifies on calendar meeting responses.
- **detect_tracking:** Extracts and registers package tracking numbers.

### FastMail-exposed Actions

| Action              | Behavior                                                  |
|---------------------|----------------------------------------------------------|
| `notify_email`      | Formats and sends the email notification                  |
| `detect_tracking`   | Runs the package-tracking extractor/add-remove flow       |
| `process_usps_digest` | Downloads image attachments and body HTML, performs USPS scan vision, sends USPS notifications, and forwards structured output |

### USPS Digest Example

```json
{
  "accounts": {
    "<account-id>": {
      "label": "personal@example.com"
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
        "sender_email": "you@example.com",
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
    },
    {
      "id": "notify-all",
      "accounts": ["<account-id>"],
      "actions": [{"name": "notify_email"}]
    }
  ]
}
```

### Multiple Mailboxes Example

```json
{
  "accounts": {
    "<account-id>": {
      "label": "john@example.com"
    }
  },
  "mail_rules": [
    {
      "id": "track-packages",
      "accounts": ["<account-id>"],
      "actions": [{"name": "detect_tracking"}],
      "continue": true
    },
    {
      "id": "notify-all",
      "accounts": ["<account-id>"],
      "actions": [{"name": "notify_email"}]
    }
  ]
}
```

Set environment variable:

```bash
FASTMAIL_INBOX_IDS=personal_inbox_id,shared_team_inbox_id
```

Notifications include mailbox name:

```
[Inbox] 📧 John Doe: Meeting tomorrow
[Shared Team] 📧 Jane Smith: Project update
```

## Environment Variables

| Variable               | Required | Description                                               |
|------------------------|----------|-----------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN    | Yes      | JMAP authentication token (or put in `~/.fastmail_token`) |
| FASTMAIL_INBOX_IDS     | Yes*     | Comma-separated mailbox IDs to monitor                    |
| FASTMAIL_INBOX_ID      | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)    |
| NOTIFY_CHANNEL         | No       | Notification channel (default: `discord`)                 |
| NOTIFY_TARGET          | Yes      | Target ID for the notification channel                    |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

## Package Tracking

When the `detect_tracking` rule is active, the daemon uses a rules-based extraction pipeline for package tracking:

### Extraction Pipeline

1. **Sender Allowlist Check:** Only scans emails from known carriers and retailers:
   - `ups.com`, `fedex.com`, `usps.com`, `dhl.com`, `amazon.com`, `narvar.com`, `aftership.com`, `shipbob.com`, `shipstation.com`, `easypost.com`, `noreply@nespresso.com`
2. **Inline Regex Scan:** Searches for carrier tracking number patterns:
   - **UPS:** `1Z[A-Z0-9]{16}`
   - **FedEx:** 12, 15, or 20-digit numbers
   - **USPS:** 20-22 digit numbers (often starts with 94, 92, 93, or 95)
   - **Amazon:** `TBA[0-9]{12}US`
3. **URL Parameter Extraction:** Extracts tracking numbers from URLs in email bodies:

   | URL Pattern                | Tracking Parameter         |
   |----------------------------|---------------------------|
   | `narvar.com/...`           | `?tracking_numbers=1Z...` |
   | `ups.com/track...`         | `?tracknum=1Z...`         |
   | `fedex.com/...track...`    | `?trknbr=...`             |
   | `usps.com/...`             | `?qtc_tLabels1=...`       |
   | `amazon.com/...track...`   | `?tracking-id=TBA...`     |

4. **Narvar Link Following:** If a `narvar.com` URL lacks a tracking number, performs HTTP GET and parses tracking from HTML.

### Automatic Package Management

- Packages are added to OpenClaw tracking with descriptive labels.
- Delivery confirmation emails trigger automatic removal from tracking.
- Each added package is logged.

View tracked packages:

```
openclaw tool call --plugin package-tracking --tool package_list
```

## Multi-Mailbox Monitoring

Supports monitoring multiple mailboxes. Notifications include mailbox prefixes for clarity:

```
[Inbox] 📧 John Doe: Meeting tomorrow
[Shared Team] 📧 Jane Smith: Project update
```

## Notification Format Examples

**General email** (from a catch-all `notify_email` rule):

```
📧 John Doe: Project update for Q1
```

**Meeting response** (from a meeting-only `notify_email` rule):

```
👤 Jane Smith accepted 👍: Team standup meeting
```

**Multi-account** (2+ accounts configured):

```
[Personal] 📧 Amazon: Your order has shipped
[Work] 👤 Bob declined 👎: All-hands meeting
```

**Package detected** (from a `detect_tracking` rule):

```
[fastmail-sse] 📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
```

## Systemd Service Setup

Enable and start the service:

```
systemctl --user enable fastmail-sse && systemctl --user start fastmail-sse
```

Check service status:

```
systemctl --user status fastmail-sse
```

View logs:

```
journalctl --user -u fastmail-sse -f
```
