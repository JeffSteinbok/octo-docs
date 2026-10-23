---
layout: default
title: Services
nav_order: 7
---

# Services

OpenClaw services are background processes that keep long-running automations available between conversations.


## Service Summary

|    | Service | Description | Docs |
| -- | ------- | ----------- | ---- |
| ⚙️ | Config Watchdog | Watches openclaw.json and auto-recovers the gateway if a bad config is detected — rotating backups, recovery ladder, and GitHub incident filing. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/config-watchdog) |
| 📡 | FastMail SSE Service | Real-time email notification daemon using JMAP EventSource | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) |
| ⚙️ | Glances | Third-party system-monitoring server run outside OpenClaw on each monitored host; the Glances plugin reads CPU, memory, disk, and summary metrics from it | [GitHub ↗](https://github.com/nicolargo/glances) |
| ⚙️ | Microsoft 365 Webhook | Receives Microsoft Graph inbox change notifications, runs new mail through the carapace mail rule pipeline, and brokers Microsoft OAuth tokens for the m365 plugin | [GitHub ↗](https://github.com/JeffSteinbok/carapace-m365/tree/main/services/m365-webhook) |
| 📝 | Obsidian Vault Indexer | Long-running systemd service that watches the Obsidian vault directory and maintains a SQLite FTS5 full-text search index. Part of the [`carapace-obsidian`](https://github.com/JeffSteinbok/carapace-obsidian) plugin. | [Read more →](services/obsidian-indexer) |
| ⚙️ | Octo Satellite | Local secrets broker providing credentialed access to Amazon and Monarch Money without exposing passwords or session cookies to the gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ | OneDrive Sync | Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive using the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) Linux client. | [Read more →](services/onedrive-sync) |
| ⚙️ | Webhook Proxy | Auth-validating proxy between Tailscale Funnel and OpenClaw's hooks endpoint. Each route checks the sender's own auth scheme (HMAC-SHA256 signature or <redacted-bearer-token>), optionally filters out events that shouldn't wake an agent, and forwards what's left to OpenClaw with the hooks <redacted-bearer-token> added. The service source lives in [`openclaw-hub/services/webhook-proxy`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy); this folder holds Octo's systemd unit (Linux) and setup notes. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy`, backed up in this repo at `config/macos/launchd/`. | [Read more →](services/webhook-proxy) |

## 📝 Obsidian Vault Indexer

Long-running systemd service that watches the Obsidian vault directory and maintains a SQLite FTS5 full-text search index. Part of the [`carapace-obsidian`](https://github.com/JeffSteinbok/carapace-obsidian) plugin.

### Key Features

- Watches the vault via `chokidar` for real-time file change detection
- Parses markdown frontmatter, tags, and `[[wikilinks]]`
- Maintains a SQLite FTS5 database in WAL mode for concurrent access
- Plugin opens the DB with `readonly: true` — never conflicts with the indexer
- Supports prefix matching (`wash` → `washer`, `washing`) and OR queries

### Environment Variables

_No environment variables required._

[Read more →](services/obsidian-indexer)

## 🗂️ OneDrive Sync

Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive using the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) Linux client.

### Key Features

- Runs as a user systemd service in `--monitor` mode
- Uses inotify to react to local file changes in near real-time
- Full rescan every 5 minutes as a safety net
- WebSocket support for Microsoft Graph API change notifications

### Environment Variables

_No environment variables required._

[Read more →](services/onedrive-sync)

## ⚙️ Webhook Proxy

Auth-validating proxy between Tailscale Funnel and OpenClaw's hooks endpoint. Each route checks the sender's own auth scheme (HMAC-SHA256 signature or <redacted-bearer-token>), optionally filters out events that shouldn't wake an agent, and forwards what's left to OpenClaw with the hooks <redacted-bearer-token> added. The service source lives in [`openclaw-hub/services/webhook-proxy`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy); this folder holds Octo's systemd unit (Linux) and setup notes. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy`, backed up in this repo at `config/macos/launchd/`.

### Key Features

- Per-route inbound auth, so each webhook sender keeps its own secret and OpenClaw's hooks token never leaves the machine
- Optional per-route filters that drop events before they reach the gateway
- Forwards to OpenClaw's local `/hooks/*` endpoint with the hooks <redacted-bearer-token> injected
- Runs as a per-user service (launchd LaunchAgent on macOS, systemd user unit on Linux) on `127.0.0.1:18792`, exposed only through Tailscale Funnel paths under `/hooksproxy/`

### Environment Variables

_No environment variables required._

[Read more →](services/webhook-proxy)
