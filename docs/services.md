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
| 🐕 | Config Watchdog | Watches openclaw.json and auto-recovers the gateway if a bad config is detected — rotating backups, recovery ladder, and GitHub incident filing. | [Read more →](services/config-watchdog) |
| 📡 | FastMail SSE Service | Real-time email notification daemon using JMAP EventSource | [Read more →](services/fastmail-sse) |
| ⚙️ | Glances | Third-party system-monitoring server run outside OpenClaw on each monitored host; the Glances plugin reads CPU, memory, disk, and summary metrics from it | [GitHub ↗](https://github.com/nicolargo/glances) |
| ⚙️ | Microsoft 365 Webhook | Receives Microsoft Graph inbox change notifications, runs new mail through the carapace mail rule pipeline, and brokers Microsoft OAuth tokens for the m365 plugin | [GitHub ↗](https://github.com/JeffSteinbok/carapace-m365/tree/main/services/m365-webhook) |
| 🌉 | MCP Bridge | OAuth-protected MCP server (WorkOS AuthKit) that lets other agents, such as OctoDot in ChatGPT, use Octo through a few config-defined tools: direct, condensed reads, guarded house changes and messages to named destinations | [Read more →](services/mcp-bridge) |
| 📝 | Obsidian Vault Indexer | Long-running indexer that maintains a SQLite FTS5 index of the Obsidian vault for full-text search | [Read more →](services/obsidian-indexer) |
| ⚙️ | Octo Satellite | Local secrets broker providing credentialed access to Amazon and Monarch Money without exposing passwords or session cookies to the gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ | OneDrive Sync | Keeps the Obsidian vault and other files synced to Microsoft OneDrive via the abraunegg/onedrive Linux client | [Read more →](services/onedrive-sync) |
| 🪝 | Webhook Proxy | Auth-validating webhook proxy between the outside world and OpenClaw hooks. Each route checks its sender's own credential (GitHub HMAC signature or a per-sender <redacted-bearer-token>), filters events, and forwards to the Gateway with the hooks token, which no external sender holds | [Read more →](services/webhook-proxy) |

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

Watches Octo's FastMail mailboxes in real time and runs each new message through the [Carapace Mail Runtime](https://github.com/JeffSteinbok/carapace-mail-runtime) rules: notify, pick up package tracking numbers, or hand a self-sent command to an agent. Rules are plain matching on account, sender and subject, so no AI looks at a message unless a rule's action asks for it. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.fastmail-sse`, backed up in this repo at `config/macos/launchd/`.

### Key Features

- Real-time: listens on FastMail's JMAP event stream instead of polling
- Watches two accounts: Octo's own mailbox and the owner's personal inbox
- Rules hot-reload when the config file changes; adding or removing an account needs a restart
- Package tracking: finds UPS, FedEx, USPS and Amazon tracking numbers in shipping emails from known senders, adds them to package tracking, and removes them when the delivery email arrives
- Skips spam and no-reply senders
- Notifications go out through `openclaw message send`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FASTMAIL_JMAP_TOKEN` | Yes | FastMail API token |
| `FASTMAIL_INBOX_IDS` | Yes | Comma-separated mailbox IDs to watch |
| `NOTIFY_CHANNEL` | No | Channel for notifications (default `discord`) |
| `NOTIFY_TARGET` | Yes | Where notifications go on that channel |

[Read more →](services/fastmail-sse)

## 🌉 MCP Bridge

The OAuth-protected MCP server behind the [Octo MCP](../mcp): how other agents, such as OctoDot in ChatGPT, use Octo. Every request needs a WorkOS AuthKit access token, checked before the request body is read, and only the owner's WorkOS account is allowed. Its tools are defined in `config/mcp-bridge/tools.json` in this repo: house and calendar reads call OpenClaw tools directly under the deliberately limited `external` agent and come back condensed; house changes go to that agent through Hass Guard; messages go straight out through the Gateway to a short list of named destinations. The service source is generic and lives in [`openclaw-hub/services/mcp-bridge`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/mcp-bridge); on the Mac mini it runs from the LaunchAgent `com.octo.openclaw.mcp-bridge`, backed up in this repo at `config/macos/launchd/`.

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

_No environment variables required._

[Read more →](services/mcp-bridge)

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

## 🪝 Webhook Proxy

Auth-validating proxy between the outside world and OpenClaw's hooks endpoint. Each route checks the sender's own credential (an HMAC-SHA256 signature or a per-sender token in the `Authorization` header), optionally filters out events that shouldn't wake an agent, and forwards what's left to OpenClaw with the hooks token added, so no external sender ever holds the real hooks token. The service source lives in [`openclaw-hub/services/webhook-proxy`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy); this folder holds Octo's setup notes and the Linux systemd unit. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy`, backed up in this repo at `config/macos/launchd/`.

### Key Features

- Per-route inbound auth, so each sender has its own secret and OpenClaw's hooks token never leaves the machine
- Per-route filters that drop events before they reach the Gateway (GitHub: allowed senders and actionable labels only)
- Exact path matching, POST only, 1 MiB body limit, and a lockout after 10 failed auth attempts in a minute
- Listens on port 18792 on all interfaces: Tailscale Funnel reaches it on loopback through the `/hooksproxy` mount, and Home Assistant reaches it on the LAN
- Loads only its own env file, `~/.openclaw/secrets/webhook-proxy.env`, not the shared OpenClaw `.env`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENCLAW_HOOKS_TOKEN` | Yes | OpenClaw hooks token, added to forwarded requests. Rotate it together with `~/.openclaw/.env |
| `GITHUB_ISSUES_HOOK_SECRET` | Yes | Secret configured on the GitHub webhook |
| `HOOKSPROXY_HASS_TOKEN` | Yes | Token Home Assistant sends in the `Authorization` header on `/hass |

[Read more →](services/webhook-proxy)
