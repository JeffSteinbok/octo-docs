---
layout: default
title: FastMail SSE
parent: Services
nav_order: 5
---

# FastMail SSE Service

> **Source:** [openclaw-hub/services/fastmail-sse](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse)

Watches Octo's FastMail mailbox (`openclaw@`) in real time and runs each new message through [Carapace Mail Runtime](https://github.com/JeffSteinbok/carapace-mail-runtime) rules: send a notification, pick up package tracking numbers, or hand a self-sent command to an agent. Rules match plainly on account, sender and subject, so no AI looks at a message unless a rule's gate or action asks for it. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.fastmail-sse` (backed up in `config/macos/launchd/`).

## Features

- Real-time: listens on FastMail's JMAP event stream (server-sent events, hence "SSE") instead of polling
- Watches one account: Octo's own mailbox. The owner's personal Fastmail address only forwards to Outlook, so `m365-webhook` handles the owner's mail; watching it here too logged every forwarded email twice
- Rules hot-reload when the config file changes; adding or removing an account needs a restart
- Package tracking: finds UPS, FedEx, USPS and Amazon tracking numbers in shipping emails from known senders, adds them to package tracking, and removes them when the delivery email arrives
- Skips spam and no-reply senders
- Notifications go out through `openclaw message send`
- Loads extra actions from `action_plugins`: today `libs/ts/mail_actions` for `process_self_email`

## Rules

Octo's rules, from `~/.openclaw/services/fastmail-sse-config.json`:

| Rule | Actions | What it does |
|---|---|---|
| `octo-calendar-responses` | `notify_email` | Tells the owner when someone accepts, declines or tentatively accepts a meeting |
| `self-email-command` | `notify_email`, `process_self_email` | Treats mail the owner sends to Octo as a request for an agent |
| `octo-tracking` | `detect_tracking` | Picks up tracking numbers from any non-GitHub mail, then lets later rules match (`continue`) |
| `octo-notify-all` | `notify_email`, gate `octo-inbox` | Notifies on other non-GitHub mail. The `octo-inbox` decision gate asks "does the owner need to see this?" first; it's log-only, so every email still notifies, a moment later |

### The `octo-inbox` gate

`octo-notify-all` used to text the owner about every non-GitHub email to Octo's mailbox: account and security mail, trial offers, and copies of Octo's own outgoing mail (countdowns, schedules, test sends). The `octo-inbox` [decision gate](https://github.com/JeffSteinbok/carapace-mail-runtime#decision-gates) (`decision_gates` in the config) asks `main`'s decision model one Boolean question, "does the owner need to see this?", through the decisions-bridge Gateway method. It sees the sender, subject, SPF/DKIM/DMARC results, local time and the first 500 characters of the body. Octo's own copies arrive inside Fastmail with no authentication results, so the rubric treats a sender claiming to be Octo with DKIM or DMARC `fail` as a possible spoof worth a text. Each verdict is a line in `~/.openclaw/logs/mail-gates.jsonl` (`gate: "octo-inbox"`), and the Monday decision review asks about the emails it would have skipped.

- **Mode `log`**: the notification goes out whatever the verdict, but it now waits for the verdict first. A call usually takes about half a second. `decisions.timeout_ms` is 5000, so a slow model gives up after 5 s, a Gateway that doesn't answer after 10 s (the CLI's `--timeout`), and a hung CLI is killed after 20 s. Emails are handled one at a time, so the emails queued behind it wait as well. If texts from this mailbox start arriving late, check the gate lines in the service log. Switching to `enforce` makes a `block` skip the text, and `on_unavailable: "pass"` keeps today's behaviour when the model can't answer.
- **Tracking is separate**: `detect_tracking` runs from its own ungated `octo-tracking` rule, so a blocked notification never drops a tracking number. Its "📦 Package registered" message now comes before the email's notification, not after.
- **Gate changes need a restart**: hot reload swaps `mail_rules` but not `decisions` or `decision_gates`, and a rule that names a gate the running service doesn't know skips its actions. Add or change a gate and restart first, then point a rule at it (hot reload picks that up). The rollout follows that order: health-check step `octo-inbox-gate-config`, then `octo-inbox-gate-log`, run straight after it. Otherwise the daily config backup could commit the stage-1 config, which has no gate on the rule.

The [FastMail SSE README](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) covers the rule syntax, the mail pipeline diagram and the tracking-number extraction in full.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `FASTMAIL_JMAP_TOKEN` | yes | FastMail API token |
| `FASTMAIL_INBOX_IDS` | yes | Comma-separated mailbox IDs to watch |
| `NOTIFY_CHANNEL` | no | Channel for notifications (default `discord`) |
| `NOTIFY_TARGET` | yes | Where notifications go on that channel |

The token and mailbox IDs come from `~/.openclaw/.env` (the token can also be read from `~/.fastmail_token`, and the older `FASTMAIL_INBOX_ID` name still works); the LaunchAgent sets the notification channel and target (on the Mac mini, notifications go to the owner over iMessage).

## Logs

```bash
tail -f ~/Library/Logs/openclaw-fastmail-sse.log
```

Restart after an account change:

```bash
launchctl kickstart -k gui/$(id -u)/com.octo.openclaw.fastmail-sse
```
