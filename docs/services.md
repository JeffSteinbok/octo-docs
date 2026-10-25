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
| ⚙️ | Octo MCP | MCP server that lets OctoDot, an OpenAI Dot in ChatGPT, reach Octo. Every request needs a WorkOS AuthKit access token, checked before the request body is read, and only the owner's WorkOS account is allowed. The service source lives in [`openclaw-hub/services/octo-mcp`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/octo-mcp); on the Mac mini it runs from the LaunchAgent `com.octo.openclaw.octo-mcp`, backed up in this repo at `config/macos/launchd/`. See [MCP & OctoDot](../mcp) for the whole picture. | [Read more →](services/octo-mcp) |
| ⚙️ | Octo Satellite | Local secrets broker providing credentialed access to Amazon and Monarch Money without exposing passwords or session cookies to the gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ | OneDrive Sync | Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive using the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) Linux client. | [Read more →](services/onedrive-sync) |
| ⚙️ | Webhook Proxy | Auth-validating proxy between the outside world and OpenClaw's hooks endpoint. Each route checks the sender's own credential (an HMAC-SHA256 signature or a per-sender token in the `Authorization` header), optionally filters out events that shouldn't wake an agent, and forwards what's left to OpenClaw with the hooks token added, so no external sender ever holds the real hooks token. The service source lives in [`openclaw-hub/services/webhook-proxy`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy); this folder holds Octo's setup notes and the Linux systemd unit. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy`, backed up in this repo at `config/macos/launchd/`. | [Read more →](services/webhook-proxy) |

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

## ⚙️ Octo MCP

MCP server that lets OctoDot, an OpenAI Dot in ChatGPT, reach Octo. Every request needs a WorkOS AuthKit access token, checked before the request body is read, and only the owner's WorkOS account is allowed. The service source lives in [`openclaw-hub/services/octo-mcp`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/octo-mcp); on the Mac mini it runs from the LaunchAgent `com.octo.openclaw.octo-mcp`, backed up in this repo at `config/macos/launchd/`. See [MCP & OctoDot](../mcp) for the whole picture.

### Key Features

- Streamable HTTP MCP, stateless, at `https://<funnel-host>/mcp`
- OAuth 2.1 resource server: protected resource metadata (RFC 9728), and AuthKit's authorization server metadata proxied for clients that look for it on this origin
- Access tokens checked for JWKS signature, issuer, audience (the MCP URL), expiry, and a one-person allowlist
- Fails closed: refuses to start without an AuthKit issuer, never serves `/mcp` unauthenticated
- Host header allowlist, POST only, 1 MiB body limit
- Holds no secrets
- Tools: `ping` (live); `ask_octo` (planned)

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OCTO_MCP_AUTHKIT_ISSUER` | Yes | AuthKit domain (`https://<name>.authkit.app`); the service won't start without it |
| `OCTO_MCP_RESOURCE` | No | Public MCP URL, which must equal the WorkOS resource indicator (default `https://<funnel-host>/mcp`) |
| `OCTO_MCP_ALLOWED_SUBJECTS` | No | Comma-separated WorkOS user IDs allowed in; empty means nobody |
| `OCTO_MCP_ALLOWED_HOSTS` | No | Host header allowlist |
| `OCTO_MCP_PORT` | No | Listen port (default 18793) |

[Read more →](services/octo-mcp)

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
