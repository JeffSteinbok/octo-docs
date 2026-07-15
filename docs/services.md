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
| 🛡️ | Config Watchdog | Watches `openclaw.json` and auto-recovers the gateway if a bad config is detected — rotating backups, recovery ladder, and GitHub incident filing | [Read more →](services/config-watchdog) |
| 📡 | FastMail SSE Service | Real-time email notification daemon using JMAP EventSource | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) |
| ⚙️ | Glances | Third-party system-monitoring server run outside OpenClaw on each monitored host; the Glances plugin reads CPU, memory, disk, and summary metrics from it | [GitHub ↗](https://github.com/nicolargo/glances) |
| 📝 | Obsidian Vault Indexer | Long-running systemd service that watches the Obsidian vault directory and maintains a SQLite FTS5 full-text search index. Part of the [`carapace-obsidian`](https://github.com/JeffSteinbok/carapace-obsidian) plugin. | [Read more →](services/obsidian-indexer) |
| ⚙️ | Octo Satellite | Local secrets broker providing credentialed access to Amazon and Monarch Money without exposing passwords or session cookies to the gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ | OneDrive Sync | Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive using the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) Linux client. | [Read more →](services/onedrive-sync) |
| ⚙️ | Outlook Webhook Service | Real-time Outlook inbox notifications via MS Graph change notifications, dispatched through the OpenClaw mail rule pipeline | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/outlook-webhook) |
| ⚙️ | Webhook Proxy | Auth-validating webhook proxy that sits between Tailscale Funnel and OpenClaw hooks. Validates inbound auth (HMAC-SHA256 or bearer) per route and forwards with the OpenClaw hooks bearer *** injected. Enables separate auth schemes per hook endpoint. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy) |

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
