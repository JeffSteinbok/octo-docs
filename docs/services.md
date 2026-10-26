---
layout: default
title: Services
nav_order: 7
---

# Services

Services are long-running background programs that run alongside the Gateway and keep work going between conversations, such as watching mail, receiving webhooks or indexing notes. On the Mac mini, the services Octo runs itself start from LaunchAgents kept in this repo under `config/macos/launchd/`, and write their logs to `~/Library/Logs/`. Third-party services link to their own docs.

## Service Summary

|    | Service | Description | Docs |
| -- | ------- | ----------- | ---- |
| 🐕 | Config Watchdog | Watches openclaw.json and brings the Gateway back after a bad config change, using rotating backups and, if those fail, a GitHub issue. Not yet running on the Mac mini. | [Read more →](services/config-watchdog) |
| 📡 | FastMail SSE Service | Watches FastMail in real time (JMAP event stream) and runs each new message through the mail rules: notify, track packages, or hand a command to an agent | [Read more →](services/fastmail-sse) |
| ⚙️ | Glances | Third-party system monitor that runs on each monitored machine, outside OpenClaw; the Glances plugin reads CPU, memory and disk metrics from it | [GitHub ↗](https://github.com/nicolargo/glances) |
| ⚙️ | Microsoft 365 Webhook | Receives Microsoft Graph notifications for new inbox mail, runs it through the Carapace mail rules, and holds the Microsoft sign-in tokens the Microsoft 365 plugin uses | [GitHub ↗](https://github.com/JeffSteinbok/carapace-m365/tree/main/services/m365-webhook) |
| 🌉 | MCP Bridge | OAuth-protected MCP server (WorkOS AuthKit) that lets other assistants, such as OctoDot in ChatGPT, use Octo through a few tools: house and calendar reads, guarded house changes, and messages to named destinations | [Read more →](services/mcp-bridge) |
| 📝 | Obsidian Vault Indexer | Long-running indexer that maintains a SQLite FTS5 index of the Obsidian vault for full-text search | [Read more →](services/obsidian-indexer) |
| ⚙️ | Octo Satellite | Local service that holds the Amazon and Monarch Money logins and makes requests for the Octo Satellite plugin, so passwords and session cookies never reach the Gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ | OneDrive Sync | Keeps the Obsidian vault and other files in ~/OneDrive synced with Microsoft OneDrive. On the Mac mini the Microsoft OneDrive app does the syncing; the abraunegg/onedrive client is only for a Linux host | [Read more →](services/onedrive-sync) |
| 🪝 | Webhook Proxy | Sits in front of OpenClaw's hooks. Each route checks its sender's own credential (a GitHub signature or a per-sender token), drops events that shouldn't wake an agent, and forwards the rest to the Gateway with the hooks token, so no outside sender ever holds that token | [Read more →](services/webhook-proxy) |

## 🐕 Config Watchdog

Watches OpenClaw's config file, `openclaw.json`, and brings the Gateway back if a change breaks it. **It isn't running on the Mac mini:** the service ships only a Linux systemd unit, and Octo hasn't had a LaunchAgent for it since the move to macOS on 2026-10-21. Until there is one, a bad config change has to be fixed by hand (`openclaw doctor`, or restore `~/.openclaw/openclaw.json.last-good`).

### Key Features

- Keeps up to 10 numbered backups of the config, refreshed on every change
- Checks the Gateway's health after each change and marks a healthy config as last-good
- When the Gateway is unhealthy, works down a recovery ladder: the last-good config, then each backup in turn, then `openclaw doctor fix`, restarting and re-checking after each step
- If nothing works, files a GitHub issue with the `doctor` output and stops
- Never deletes anything: a bad config is kept as `openclaw.json.bad.<timestamp>`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENCLAW_CONFIG_FILE` | No | Config file to watch (default `~/.openclaw/openclaw.json`) |
| `WATCHDOG_BACKUP_VERSIONS` | No | Number of numbered backups to keep (default 10) |
| `OPENCLAW_GATEWAY_URL` | No | Gateway address for health checks (default `http://127.0.0.1:18789`) |
| `OPENCLAW_LAUNCHD_LABEL` | No | LaunchAgent to restart on macOS (default `ai.openclaw.gateway`) |
| `GITHUB_TOKEN` | No | Token used to file the GitHub issue |

[Read more →](services/config-watchdog)

## 📡 FastMail SSE Service

Watches Octo's FastMail mailboxes in real time and runs each new message through [Carapace Mail Runtime](https://github.com/JeffSteinbok/carapace-mail-runtime) rules: send a notification, pick up package tracking numbers, or hand a self-sent command to an agent. Rules match plainly on account, sender and subject, so no AI looks at a message unless a rule's action asks for it. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.fastmail-sse` (backed up in `config/macos/launchd/`).

### Key Features

- Real-time: listens on FastMail's JMAP event stream (server-sent events, hence "SSE") instead of polling
- Watches two accounts: Octo's own mailbox and the owner's personal inbox
- Rules hot-reload when the config file changes; adding or removing an account needs a restart
- Package tracking: finds UPS, FedEx, USPS and Amazon tracking numbers in shipping emails from known senders, adds them to package tracking, and removes them when the delivery email arrives
- Skips spam and no-reply senders
- Notifications go out through `openclaw message send`
- Loads extra actions from `action_plugins`: today [`libs/ts/mail_actions`](https://github.com/JeffSteinbok/octo/tree/main/libs/ts/mail_actions) for `process_self_email`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FASTMAIL_JMAP_TOKEN` | Yes | FastMail API token |
| `FASTMAIL_INBOX_IDS` | Yes | Comma-separated mailbox IDs to watch |
| `NOTIFY_CHANNEL` | No | Channel for notifications (default `discord`) |
| `NOTIFY_TARGET` | Yes | Where notifications go on that channel |

[Read more →](services/fastmail-sse)

## 🌉 MCP Bridge

The OAuth-protected MCP server behind the Octo MCP, which lets other agents, such as OctoDot in ChatGPT, use Octo through a few tools defined in `config/mcp-bridge/tools.json`. Every request needs a WorkOS AuthKit access token for the owner's account, checked before the request body is read. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.mcp-bridge` (backed up in `config/macos/launchd/`).

### Key Features

- Streamable HTTP MCP, stateless, at `https://<funnel-host>/mcp`
- OAuth 2.1 resource server: protected resource metadata (RFC 9728), and AuthKit's authorization server metadata proxied for clients that look for it on this origin
- Access tokens checked for JWKS signature, issuer, audience (the MCP URL), expiry, and a one-person allowlist
- Fails closed: refuses to start without an issuer, resource URL and valid tool definitions; never serves `/mcp` unauthenticated
- Tools defined in config, split by risk: direct, condensed reads (`house_status`, `calendar`); `control_house` (changes the house, confirmed in ChatGPT); `send_message` (iMessage or Discord to named destinations, confirmed in ChatGPT); `ping`
- MCP server instructions tell the client what Octo can and can't do
- Paired with the OpenClaw Gateway as its own device (`operator.read` + `operator.write`, no admin); the shared Gateway token is used once to pair and never stored
- Host header allowlist, POST only, 1 MiB body limit

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MCP_BRIDGE_TOOLS` | Yes | Tool definitions file (`~/git/octo/config/mcp-bridge/tools.json`) |
| `MCP_BRIDGE_RESOURCE` | Yes | Public MCP URL (`https://<funnel-host>/mcp`); must equal the WorkOS resource indicator |
| `MCP_BRIDGE_ISSUER` | Yes | AuthKit domain, exactly as in tokens' `iss |
| `MCP_BRIDGE_ALLOWED_SUBJECTS` | No | WorkOS user IDs allowed in; empty means nobody gets in |

[Read more →](services/mcp-bridge)

## 📝 Obsidian Vault Indexer

Long-running service that watches the Obsidian vault and keeps a SQLite full-text search index (FTS5) of it up to date, so the [`carapace-obsidian`](https://github.com/JeffSteinbok/carapace-obsidian) plugin can search notes without reading every file. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.obsidian-indexer` (backed up in `config/macos/launchd/`).

### Key Features

- Watches the vault with `chokidar` and re-indexes files as they change
- Parses Markdown front matter, tags and `[[wikilinks]]`
- Keeps the index in a SQLite FTS5 database in WAL mode, so reads and writes can happen at the same time
- The plugin opens the database read-only, so it never conflicts with the indexer
- Supports prefix matching (`wash` finds `washer` and `washing`) and OR queries

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OBSIDIAN_VAULT_ROOT` | Yes | Vault folder to watch (on the Mac mini, the `JeffBrain` folder in OneDrive) |
| `OBSIDIAN_INDEX_LOCATION` | No | Where the index database is written (default `~/.openclaw/obsidian-index.db`) |

[Read more →](services/obsidian-indexer)

## 🗂️ OneDrive Sync

Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive, so notes written on the owner's other devices reach Octo and the Obsidian Vault Indexer. On the Mac mini this is the Microsoft OneDrive app; nothing from this repo runs there. On a Linux host it is the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) client, set up as described below.

### Key Features

- macOS: the Microsoft OneDrive app syncs to `~/Library/CloudStorage/OneDrive-Personal`, and `~/OneDrive` is a symlink to that folder, so paths under `~/OneDrive/` are the same on either platform
- Linux: runs as a user systemd service in `--monitor` mode
- Linux: uses inotify to pick up local file changes in near real time, with a full rescan every 5 minutes as a safety net
- Linux: uses Microsoft Graph change notifications over WebSocket to pick up remote changes

### Environment Variables

_No environment variables required._

[Read more →](services/onedrive-sync)

## 🪝 Webhook Proxy

Auth-validating proxy between the outside world and OpenClaw's hooks endpoint. Each route checks the sender's own credential (an HMAC-SHA256 signature or a per-sender token), optionally drops events that shouldn't wake an agent, and forwards the rest to the Gateway with the hooks token added, so no external sender ever holds the real hooks token. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy` (backed up in `config/macos/launchd/`).

### Key Features

- Per-route inbound auth, so each sender has its own secret and OpenClaw's hooks token never leaves the machine
- Per-route filters that drop events before they reach the Gateway (GitHub: allowed senders and actionable labels only)
- Exact path matching, POST only, 1 MiB body limit, and a lockout after 10 failed auth attempts in a minute
- Listens on port 18792 on all interfaces (`bind_host: 0.0.0.0` in the config; the code's default is `127.0.0.1`): Tailscale Funnel reaches it on loopback through the `/hooksproxy` mount, and Home Assistant reaches it on the LAN
- The LaunchAgent loads only its own env file, `~/.openclaw/secrets/webhook-proxy.env`, not the shared OpenClaw `.env`. (The Linux `webhook-proxy.service` unit in this folder is from the retired host and still loads `~/.openclaw/.env`.)

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENCLAW_HOOKS_TOKEN` | Yes | OpenClaw hooks token, added to forwarded requests. Rotate it together with `~/.openclaw/.env |
| `GITHUB_ISSUES_HOOK_SECRET` | Yes | Secret configured on the GitHub webhook |
| `HOOKSPROXY_HASS_TOKEN` | Yes | Token Home Assistant sends in the `Authorization` header on `/hass |

[Read more →](services/webhook-proxy)
