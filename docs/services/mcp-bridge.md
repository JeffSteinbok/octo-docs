---
layout: default
title: MCP Bridge
parent: Services
nav_order: 4
---

# MCP Bridge

> **Source:** [openclaw-hub/services/mcp-bridge](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/mcp-bridge)

The OAuth-protected MCP server behind the [Octo MCP](../mcp): how other agents, such as OctoDot in ChatGPT, use Octo. Every request needs a WorkOS AuthKit access token, checked before the request body is read, and only the owner's WorkOS account is allowed. Its tools are defined in `config/mcp-bridge/tools.json` in this repo: house and calendar reads call OpenClaw tools directly under the deliberately limited `external` agent and come back condensed; house changes go to that agent through Hass Guard; messages go straight out through the Gateway to a short list of named destinations. The service source is generic and lives in [`openclaw-hub/services/mcp-bridge`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/mcp-bridge); on the Mac mini it runs from the LaunchAgent `com.octo.openclaw.mcp-bridge`, backed up in this repo at `config/macos/launchd/`.

## Features

- Streamable HTTP MCP, stateless, at `https://<funnel-host>/mcp`
- OAuth 2.1 resource server: protected resource metadata (RFC 9728), and AuthKit's authorization server metadata proxied for clients that look for it on this origin
- Access tokens checked for JWKS signature, issuer, audience (the MCP URL), expiry, and a one-person allowlist
- Fails closed: refuses to start without an issuer, resource URL and valid tool definitions; never serves `/mcp` unauthenticated
- Tools defined in config, split by risk: direct, condensed reads (`house_status`, `calendar`); `control_house` (changes the house, confirmed in ChatGPT); `send_message` (iMessage or Discord to named destinations, confirmed in ChatGPT); `ping`
- MCP server instructions tell the client what Octo can and can't do
- Paired with the OpenClaw Gateway as its own device (`operator.read` + `operator.write`, no admin); the shared Gateway token is used once to pair and never stored
- Host header allowlist, POST only, 1 MiB body limit

## Tools

From `config/mcp-bridge/tools.json`:

| Tool | Kind | Action | What happens |
|---|---|---|---|
| `house_status` | read-only | `invoke` | `hass_state_list` for lights, covers, climate and media players, condensed (`home-assistant-status`); network-gear status lights are ignored |
| `calendar` | read-only | `invoke` + `dateRange` | `ics_calendar_fetch` (Personal, Family, TripIt) and `outlook_work_calendar_fetch`, merged and sorted (`calendar-events`) in Pacific time |
| `control_house` | changes things | `ask` | The request, quoted as data, to the `external` agent; Hass Guard checks every action |
| `send_message` | sends things | `send` | Direct Gateway `send` to a named destination from the private destinations file; no AI involved |
| `ping` | read-only | built in | Reachability |

Changing what OctoDot can do is a change to `tools.json` (and, for new OpenClaw tools, to the `external` agent's tool list), then a restart of the LaunchAgent.

## Funnel routes

ChatGPT doesn't connect to non-443 ports, so these paths on the shared 443 hostname go to `127.0.0.1:18793` unchanged:

| Path | Purpose |
|---|---|
| `/mcp` | MCP endpoint |
| `/.well-known/oauth-protected-resource` (and `…/mcp`) | Protected resource metadata |
| `/.well-known/oauth-authorization-server` | AuthKit metadata, proxied |

## Configuration

The LaunchAgent sets `MCP_BRIDGE_TOOLS` to `~/git/octo/config/mcp-bridge/tools.json` and reads the rest from a private env file, `~/.openclaw/secrets/mcp-bridge/mcp-bridge.env`:

| Variable | Description |
|---|---|
| `MCP_BRIDGE_RESOURCE` | Public MCP URL (`https://<funnel-host>/mcp`); must equal the WorkOS resource indicator |
| `MCP_BRIDGE_ISSUER` | AuthKit domain, exactly as in tokens' `iss` |
| `MCP_BRIDGE_ALLOWED_SUBJECTS` | WorkOS user IDs allowed in; empty means nobody |

Defaults cover the rest (device directory `~/.openclaw/secrets/mcp-bridge`, Gateway `ws://127.0.0.1:18789`, port 18793); the [mcp-bridge README](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/mcp-bridge) lists every setting. The device directory (mode 700/600, never in a repo) holds the device identity and token and `destinations.json`, the message destinations' handles and channel IDs.

## Install

```bash
cd ~/git/openclaw-hub/services/mcp-bridge
npm ci && npm run build && npm test
cp ~/git/octo/config/macos/launchd/com.octo.openclaw.mcp-bridge.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.octo.openclaw.mcp-bridge.plist
```

Pair with the Gateway once (the shared token is used for this command only):

```bash
OPENCLAW_GATEWAY_TOKEN=… node dist/pair.js
openclaw devices list    # role operator, scopes operator.read + operator.write
```

Funnel routes: `config/tailscale/apply-step-441.sh` (owner-run, needs the Tailscale operator).

## Logs

```bash
tail -f ~/Library/Logs/openclaw-mcp-bridge.log
```

At startup the log lists the tools and destination names it loaded. Every request is logged with its path and user agent; refusals include the reason, a `403` includes the WorkOS user ID so a new user can be allowlisted, and each `send_message` logs the destination name (never the message).
