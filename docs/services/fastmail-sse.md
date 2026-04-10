---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email ingestion daemon that connects to FastMail's JMAP EventSource. It normalizes each new message into a provider-agnostic mail envelope, applies deterministic rules, and executes Python actions. Designed for extensibility, its rule/action runtime can be shared with future sources such as Outlook poll or webhook integrations. The service enables real-time notifications, package tracking, and meeting response alerts across multiple mailboxes.

## Key Concepts

- Shared mail pipeline: `source -> envelope -> rules -> Python actions`
- Per-account legacy rules: `notify_all`, `notify_meeting_updates`, `detect_tracking`
- Deterministic mail rules: Explicit matching for source/account/sender/subject
- Multi-mailbox monitoring: Supports personal and shared mailboxes
- Package tracking detection: Automatic extraction and management of tracking numbers
- Meeting updates: Notifications for calendar responses
- USPS digest processing: Structured handling of USPS Informed Delivery emails
- Real-time state changes via JMAP SSE endpoint
- Spam/noreply sender filtering
- Notification delivery via `openclaw message send`

## Features

| Feature | Description |
|---------|-------------|
| Shared mail pipeline | Processes emails through a pipeline: source → envelope → rules → Python actions |
| Per-account legacy rules | Supports `notify_all`, `notify_meeting_updates`, and `detect_tracking` for backward compatibility |
| Deterministic mail rules | Top-level `mail_rules` for explicit matching and action execution |
| Multi-mailbox monitoring | Monitors multiple inboxes simultaneously, including shared mailboxes |
| Package tracking detection | Automatically detects and registers tracking numbers from emails |
| Meeting updates | Notifies on calendar accept/decline/tentative responses |
| USPS digest processing | Downloads images/body HTML, performs scan vision, sends USPS alerts, and forwards structured results |
| Real-time state changes | Connects to JMAP SSE endpoint for instant updates |
| Spam/noreply filtering | Skips notifications from spam and noreply senders |
| Notification delivery | Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>` |

## Configuration

### Account Rules Config File

Create `~/.openclaw/services/fastmail-sse-config.json` for per-account rules and deterministic mail rules.

#### Account Rules

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
  }
}
```

**Account ID**: FastMail JMAP account ID  
**Label**: Displayed in multi-account notifications

| Rule | Description |
|------|-------------|
| `notify_all` | Notify on all incoming mail (excluding spam/unsubscribe) |
| `notify_meeting_updates` | Notify only on calendar responses |
| `detect_tracking` | Scan email body for tracking numbers and register them |

- `notify_all`: All emails trigger notifications (subject to spam filtering)
- `notify_meeting_updates`: Only calendar responses trigger notifications
- `detect_tracking`: Emails scanned for tracking numbers, automatically added to package tracking
- Rules can be combined

#### Deterministic `mail_rules`

Attach explicit Python actions to deterministic matches. Rules are evaluated in order; set `"continue": true` to evaluate subsequent rules.

Supported match fields:

| Field | Meaning |
|-------|---------|
| `sender_email` | Exact sender address |
| `sender_domain` | Sender domain/subdomain |
| `sender_name_contains` | Sender name substring |
| `subject` | Exact subject |
| `subject_contains` | Subject substring |
| `subject_prefix` | Subject prefix |
| `subject_regex` | Regex match |
| `body_contains` | Body substring |
| `has_attachments` | Attachment hint |

Built-in actions:

| Action | Behavior |
|--------|---------|
| `notify_email` | Formats and sends email notification |
| `detect_tracking` | Runs package-tracking extraction and management |
| `process_usps_digest` | Handles USPS digest emails, performs scan vision, sends alerts, and forwards structured output |

#### Configuration Examples

**Personal + Work Accounts**

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

**Package Tracking Only**

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
- No notifications, but tracking numbers are registered

**USPS Informed Delivery via action pipeline**

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
- Downloads digest assets, performs scan vision, sends USPS alerts, and forwards structured summary

**Multiple Mailboxes (Personal + Shared)**

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

### Environment Variables

| Variable                | Required | Description                                              |
|-------------------------|----------|----------------------------------------------------------|
| FASTMAIL_JMAP_TOKEN     | Yes      | JMAP authentication token (or put in `~/.fastmail_token`)|
| FASTMAIL_INBOX_IDS      | Yes*     | Comma-separated mailbox IDs to monitor                   |
| FASTMAIL_INBOX_ID       | Yes*     | Single mailbox ID (legacy, use INBOX_IDS for multiple)   |
| NOTIFY_CHANNEL          | No       | Notification channel (default: `discord`)                |
| NOTIFY_TARGET           | Yes      | Target ID for the notification channel                   |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

## Package Tracking

When the `detect_tracking` rule is active, the daemon applies a rules-based extraction pipeline for package tracking.

### Extraction Pipeline

1. **Sender allowlist check**  
   Only emails from known carriers and retailers are scanned:  
   - `ups.com`, `fedex.com`, `usps.com`, `dhl.com`, `amazon.com`, `narvar.com`, `aftership.com`, `shipbob.com`, `shipstation.com`, `easypost.com`, `noreply@nespresso.com`

2. **Inline regex scan**  
   Scans email body for carrier tracking patterns:
   - UPS: `1Z[A-Z0-9]{16}`
   - FedEx: 12, 15, or 20-digit numbers
   - USPS: 20-22 digit numbers (often starts with 94, 92, 93, or 95)
   - Amazon: `TBA[0-9]{12}US`

3. **URL parameter extraction**  
   Extracts tracking numbers from URLs in email bodies:

   | URL pattern                  | Example tracking param         |
   |-----------------------------|-------------------------------|
   | `narvar.com/...`            | `?tracking_numbers=1Z...`     |
   | `ups.com/track...`          | `?tracknum=1Z...`             |
   | `fedex.com/...track...`     | `?trknbr=...`                 |
   | `usps.com/...`              | `?qtc_tLabels1=...`           |
   | `amazon.com/...track...`    | `?tracking-id=TBA...`         |

4. **Narvar link following**  
   If a `narvar.com` URL is found without a tracking number, performs HTTP GET and parses tracking number from HTML.

### Automatic Package Management

- Packages are added to OpenClaw tracking with descriptive labels:
  ```
  Personal: Amazon - Order Shipped - Your package is on the way
  ```
- Delivery confirmation emails trigger automatic removal from tracking.
- Logs each package addition:
  ```
  📦 added package: 1Z999AA10123456784 (UPS) — Personal: ...
  ```
- View tracked packages:
  ```
  openclaw tool call --plugin package-tracking --tool package_list
  ```

## Multi-Mailbox Monitoring

Supports monitoring multiple mailboxes. Notifications include mailbox prefix for clarity.

Example notification formats:
```
[Inbox] 📧 John Doe: Meeting tomorrow
[Shared Team] 📧 Jane Smith: Project update
```

## Notification Format Examples

**General email** (`notify_all`):
```
📧 John Doe: Project update for Q1
```

**Meeting response** (`notify_meeting_updates`):
```
👤 Jane Smith accepted 👍: Team standup meeting
```

**Multi-account** (2+ accounts):
```
[Personal] 📧 Amazon: Your order has shipped
[Work] 👤 Bob declined 👎: All-hands meeting
```

**Package detected** (`detect_tracking`):
```
[fastmail-sse] 📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
```

## Systemd Service Setup

Enable and start the service:
```bash
systemctl --user enable fastmail-sse && systemctl --user start fastmail-sse
```

Check service status:
```bash
systemctl --user status fastmail-sse
```

View logs:
```bash
journalctl --user -u fastmail-sse -f
```
