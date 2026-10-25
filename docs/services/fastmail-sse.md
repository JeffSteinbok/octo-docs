---
layout: default
title: FastMail SSE
parent: Services
nav_order: 5
---

# FastMail SSE Service

> **Source:** [openclaw-hub/services/fastmail-sse](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse)

Watches Octo's FastMail mailboxes in real time and runs each new message through [Carapace Mail Runtime](https://github.com/JeffSteinbok/carapace-mail-runtime) rules: send a notification, pick up package tracking numbers, or hand a self-sent command to an agent. Rules match plainly on account, sender and subject, so no AI looks at a message unless a rule's action asks for it. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.fastmail-sse` (backed up in `config/macos/launchd/`).

## Features

- Real-time: listens on FastMail's JMAP event stream (server-sent events, hence "SSE") instead of polling
- Watches two accounts: Octo's own mailbox and the owner's personal inbox
- Rules hot-reload when the config file changes; adding or removing an account needs a restart
- Package tracking: finds UPS, FedEx, USPS and Amazon tracking numbers in shipping emails from known senders, adds them to package tracking, and removes them when the delivery email arrives
- Skips spam and no-reply senders
- Notifications go out through `openclaw message send`

## Rules

Octo's rules, from `~/.openclaw/services/fastmail-sse-config.json`:

| Rule | Actions | What it does |
|---|---|---|
| `octo-calendar-responses` | `notify_email` | Tells the owner when someone accepts, declines or tentatively accepts a meeting |
| `self-email-command` | `notify_email`, `process_self_email` | Treats mail the owner sends to Octo as a request for an agent |
| `octo-notify-all` | `notify_email`, `detect_tracking` | Notifies on other new mail and picks up tracking numbers |

The [FastMail SSE README](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) covers the rule syntax, the mail pipeline diagram and the tracking-number extraction in full.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `FASTMAIL_JMAP_TOKEN` | yes | FastMail API token |
| `FASTMAIL_INBOX_IDS` | yes | Comma-separated mailbox IDs to watch |
| `NOTIFY_CHANNEL` | no | Channel for notifications (default `discord`) |
| `NOTIFY_TARGET` | yes | Where notifications go on that channel |

The token and mailbox IDs come from `~/.openclaw/.env`; the LaunchAgent sets the notification channel and target (on the Mac mini, notifications go to the owner over iMessage).

## Logs

```bash
tail -f ~/Library/Logs/openclaw-fastmail-sse.log
```

Restart after an account change:

```bash
launchctl kickstart -k gui/$(id -u)/com.octo.openclaw.fastmail-sse
```
