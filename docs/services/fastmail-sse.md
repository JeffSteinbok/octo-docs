---
layout: default
title: FastMail SSE Service
parent: Services
nav_order: 1
---

# FastMail SSE Service

## Overview

The FastMail SSE Service is a real-time email notification daemon that connects to FastMail's JMAP EventSource. It monitors one or more mailboxes for new emails, formats notifications, and sends them via OpenClaw's message system. This service is designed to provide timely updates for incoming emails, meeting responses, and package tracking, while offering flexible configuration options for multi-account and multi-mailbox setups.

## Features

- **Per-account rules**: Configure notification behavior per account.
- **Multi-mailbox monitoring**: Monitor personal inbox and shared mailboxes simultaneously.
- **Package tracking detection**: Automatically detect and register tracking numbers from emails.
- **Meeting updates**: Notify on calendar accept/decline/tentative responses.
- **Real-time state changes**: Connects to JMAP SSE endpoint for immediate updates.
- **Spam filtering**: Skips spam and noreply senders.
- **Notification delivery**: Sends notifications via `openclaw message send --channel <NOTIFY_CHANNEL> --target <NOTIFY_TARGET>`.

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
| `notify_all`          | Notify on all incoming mail (excluding spam/unsubscribe filter).           |
| `notify_meeting_updates` | Notify only on calendar accept/decline/tentative responses.               |
| `detect_tracking`     | Scan email body for tracking numbers and register via OpenClaw package tracking. |

**Behavior**:
- `notify_all`: All emails trigger notifications (subject to spam filtering).
- `notify_meeting_updates`: Only calendar responses trigger notifications.
- `detect_tracking`: Scans email bodies for tracking numbers and automatically adds them to OpenClaw package tracking.
- Multiple rules can be combined (e.g., `["notify_meeting_updates", "detect_tracking"]`).

### Environment Variables

| Variable              | Required | Description                                                                 |
|-----------------------|----------|-----------------------------------------------------------------------------|
| `FASTMAIL_JMAP_TOKEN` | Yes      | JMAP authentication token (or put in `~/.fastmail_token`).                  |
| `FASTMAIL_INBOX_IDS`  | Yes*     | Comma-separated mailbox IDs to monitor (e.g., `inbox1,inbox2`).             |
| `FASTMAIL_INBOX_ID`   | Yes*     | Single mailbox ID (legacy, use `FASTMAIL_INBOX_IDS` for multiple).          |
| `NOTIFY_CHANNEL`      | No       | Notification channel (default: `telegram`).                                 |
| `NOTIFY_TARGET`       | Yes      | Target ID for the notification channel.                                     |

*Either `FASTMAIL_INBOX_IDS` or `FASTMAIL_INBOX_ID` is required.

## Package Tracking

When the `detect_tracking` rule is active, the daemon applies a rules-based extraction pipeline to identify and manage package tracking numbers.

### Extraction Pipeline

1. **Sender allowlist check**: Scans emails only from known shipping carriers and retailers, including:
   - `ups.com`, `fedex.com`, `usps.com`, `dhl.com`, `amazon.com`, `narvar.com`, `aftership.com`, `shipbob.com`, `shipstation.com`, `easypost.com`, and `noreply@nespresso.com`.

2. **Inline regex scan**: Identifies tracking numbers in the email body using carrier-specific patterns:
   - **UPS**: `1Z[A-Z0-9]{16}` (e.g., `1Z999AA10123456784`).
   - **FedEx**: 12, 15, or 20-digit numbers.
   - **USPS**: 20-22 digit numbers (e.g., starting with 94, 92, 93, or 95).
   - **Amazon**: `TBA[0-9]{12}US` (e.g., `TBA012345678901US`).

3. **URL parameter extraction**: Extracts tracking numbers from shipping/tracking URLs embedded in the email:

   | URL pattern          | Example tracking param       |
   |----------------------|------------------------------|
   | `narvar.com/...`     | `?tracking_numbers=1Z...`    |
   | `ups.com/track...`   | `?tracknum=1Z...`            |
   | `fedex.com/...track...` | `?trknbr=...`                |
   | `usps.com/...`       | `?qtc_tLabels1=...`          |
   | `amazon.com/...track...` | `?tracking-id=TBA...`        |

4. **Narvar link following**: If a `narvar.com` URL is found without a tracking number, the daemon fetches the page and extracts the tracking number from the HTML.

### Automatic Package Management

- Detected packages are added to OpenClaw package tracking with a label, e.g.:
  ```
  Personal: Amazon - Order Shipped - Your package is on the way
  ```
- Packages are automatically removed from tracking upon delivery confirmation.
- Logs each added package:
  ```
  📦 added package: 1Z999AA10123456784 (UPS) — Personal: …
  ```

View tracked packages:
```bash
openclaw tool call --plugin package-tracking --tool package_list
```

## Notification Examples

### General Email (with `notify_all`)
```
📧 John Doe: Project update for Q1
```

### Meeting Response (with `notify_meeting_updates`)
```
👤 Jane Smith accepted 👍: Team standup meeting
```

### Multi-Account Notifications
```
[Personal] 📧 Amazon: Your order has shipped
[Work] 👤 Bob declined 👎: All-hands meeting
```

### Package Detected (with `detect_tracking`)
```
[fastmail-sse] 📦 added package: 1Z999AA10123456784 (UPS) — Personal: Amazon - Order Shipped
```

## Systemd Service

Install and start the service:
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
