---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email notification daemon that connects to FastMail's JMAP EventSource. It monitors one or more mailboxes for new emails, formats notifications, and sends them via OpenClaw's messaging system. This service is designed to provide timely updates for general emails, meeting responses, and package tracking, while filtering out spam and irrelevant messages.

## Features

- **Per-account rules**: Configure notification behavior for each account.
- **Multi-mailbox monitoring**: Monitor personal inboxes and shared mailboxes simultaneously.
- **Package tracking detection**: Automatically detect and register tracking numbers from shipping emails.
- **Meeting updates**: Notify on calendar accept/decline/tentative responses.
- **Real-time updates**: Connects to the JMAP SSE endpoint for instant state changes.
- **Spam filtering**: Skips spam and noreply senders.
- **Notification delivery**: Sends notifications via `openclaw message send`.

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
  }
}
```

#### Rules

| Rule                  | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `notify_all`          | Notify on all incoming mail (excluding spam/unsubscribe messages).         |
| `notify_meeting_updates` | Notify only on calendar accept/decline/tentative responses.              |
| `detect_tracking`     | Scan email bodies for tracking numbers and register them for package tracking. |

**Behavior**:
- `notify_all` triggers notifications for all emails (subject to spam filtering).
- `notify_meeting_updates` limits notifications to calendar responses.
- `detect_tracking` scans emails for tracking numbers and registers them automatically.
- Rules can be combined (e.g., `["notify_meeting_updates", "detect_tracking"]`).

### Environment Variables

| Variable               | Required | Description                                                   |
|------------------------|----------|---------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN`  | Yes      | JMAP authentication token (or stored in `~/.fastmail_token`). |
| `FASTMAIL_INBOX_IDS`   | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`).|
| `FASTMAIL_INBOX_ID`    | Yes*     | Single mailbox ID (legacy, use `FASTMAIL_INBOX_IDS` for multiple). |
| `NOTIFY_CHANNEL`       | No       | Notification channel (default: `telegram`).                   |
| `NOTIFY_TARGET`        | Yes      | Target ID for the notification channel.                       |

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

**Result**:
- Personal account: Notifications for all emails + package tracking.
- Work account: Notifications only for meeting responses.

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

**Result**: No notifications, but tracking numbers are automatically registered.

#### Example 3: Multiple Mailboxes

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

Environment variables:

```bash
FASTMAIL_INBOX_IDS=personal_inbox_id,shared_team_inbox_id
```

Notifications include the mailbox name:

```
[Inbox] 📧 John Doe: Meeting tomorrow
[Shared Team] 📧 Jane Smith: Project update
```

## Package Tracking

When the `detect_tracking` rule is active, the service uses a rules-based extraction pipeline to identify and register tracking numbers.

### Extraction Pipeline

1. **Sender allowlist check**: Scans emails only from known shipping carriers and retailers, such as `ups.com`, `fedex.com`, `usps.com`, `amazon.com`, and others.
2. **Inline regex scan**: Identifies tracking numbers using carrier-specific patterns:
   - **UPS**: `1Z[A-Z0-9]{16}`
   - **FedEx**: 12, 15, or 20-digit numbers
   - **USPS**: 20-22 digit numbers
   - **Amazon**: `TBA[0-9]{12}US`
3. **URL parameter extraction**: Extracts tracking numbers from shipping/tracking URLs in email content:
   | URL Pattern          | Example Tracking Parameter         |
   |----------------------|-------------------------------------|
   | `narvar.com/...`     | `?tracking_numbers=1Z...`          |
   | `ups.com/track...`   | `?tracknum=1Z...`                  |
   | `fedex.com/...track` | `?trknbr=...`                      |
   | `usps.com/...`       | `?qtc_tLabels1=...`                |
   | `amazon.com/...track`| `?tracking-id=TBA...`              |
4. **Narvar link following**: For `narvar.com` URLs without tracking numbers, performs an HTTP GET request to extract tracking details.

### Automatic Package Management

- Detected packages are added to OpenClaw package tracking with labels like:
  ```
  Personal: Amazon - Order Shipped - Your package is on the way
  ```
- Packages are automatically removed upon delivery confirmation.
- Logs each package addition:
  ```
  📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
  ```

## Notification Examples

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

## Systemd Service

To manage the FastMail SSE service using systemd:

- **Install and start the service**:
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
