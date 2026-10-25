---
layout: default
title: Octo MCP
parent: Services
nav_order: 4
---

# Octo MCP

MCP server that lets OctoDot, an OpenAI Dot in ChatGPT, reach Octo. Every request needs a WorkOS AuthKit access token, checked before the request body is read, and only the owner's WorkOS account is allowed. House and calendar questions go to OpenClaw's deliberately limited `external` agent; messages go straight out through the Gateway to a short allowlist of destinations. The service source lives in [`openclaw-hub/services/octo-mcp`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/octo-mcp); on the Mac mini it runs from the LaunchAgent `com.octo.openclaw.octo-mcp`, backed up in this repo at `config/macos/launchd/`. See [MCP & OctoDot](../mcp) for the whole picture and the reasoning.

## Features

- Streamable HTTP MCP, stateless, at `https://<funnel-host>/mcp`
- OAuth 2.1 resource server: protected resource metadata (RFC 9728), and AuthKit's authorization server metadata proxied for clients that look for it on this origin
- Access tokens checked for JWKS signature, issuer, audience (the MCP URL), expiry, and a one-person allowlist
- Fails closed: refuses to start without an AuthKit issuer, never serves `/mcp` unauthenticated
- Tools split by risk: `house_status` and `calendar` (read-only, fixed prompts), `control_house` (changes the house, confirmed in ChatGPT), `send_message` (iMessage or Discord to named destinations, confirmed in ChatGPT), `ping`
- MCP server instructions tell the client what Octo can and can't do
- Paired with the OpenClaw Gateway as its own device (`operator.read` + `operator.write`, no admin); the shared Gateway token is used once to pair and never stored
- Host header allowlist, POST only, 1 MiB body limit

## Tools

| Tool | Kind | What happens |
|---|---|---|
| `house_status` | read-only | Fixed question to the `external` agent: lights, covers, thermostat, TVs |
| `calendar` | read-only | Fixed question with a validated range or dates |
| `control_house` | changes things | Request (quoted as data) to the `external` agent; Hass Guard checks every action |
| `send_message` | sends things | Direct Gateway `send` to a named destination from the private allowlist; no AI involved |
| `ping` | read-only | Reachability |

## Funnel routes

ChatGPT doesn't connect to non-443 ports, so these paths on the shared 443 hostname go to `127.0.0.1:18793` unchanged:

| Path | Purpose |
|---|---|
| `/mcp` | MCP endpoint |
| `/.well-known/oauth-protected-resource` (and `…/mcp`) | Protected resource metadata |
| `/.well-known/oauth-authorization-server` | AuthKit metadata, proxied |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OCTO_MCP_AUTHKIT_ISSUER` | yes | AuthKit domain (`https://<name>.authkit.app`); the service won't start without it |
| `OCTO_MCP_RESOURCE` | no | Public MCP URL, which must equal the WorkOS resource indicator (default `https://<funnel-host>/mcp`) |
| `OCTO_MCP_ALLOWED_SUBJECTS` | no | Comma-separated WorkOS user IDs allowed in; empty means nobody |
| `OCTO_MCP_DEVICE_DIR` | no | Paired-device identity, device token and message destinations (default `~/.openclaw/secrets/octo-mcp`) |
| `OCTO_MCP_GATEWAY_URL` | no | OpenClaw Gateway WebSocket (default `ws://127.0.0.1:18789`) |
| `OCTO_MCP_AGENT` | no | Agent behind the house and calendar tools (default `external`) |
| `OCTO_MCP_ALLOWED_HOSTS` | no | Host header allowlist |
| `OCTO_MCP_PORT` | no | Listen port (default 18793) |

None of these are secrets, so they live in the LaunchAgent's `EnvironmentVariables`. The device token and the message destinations (handles and channel IDs) live in `OCTO_MCP_DEVICE_DIR` (mode 700/600), never in a repo.

## Install

```bash
cd ~/git/openclaw-hub/services/octo-mcp
npm ci && npm run build && npm test
cp ~/git/octo/config/macos/launchd/com.octo.openclaw.octo-mcp.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.octo.openclaw.octo-mcp.plist
```

Pair with the Gateway once (the shared token is used for this command only):

```bash
OPENCLAW_GATEWAY_TOKEN=… node dist/pair.js
openclaw devices list    # octo-mcp: role operator, scopes operator.read + operator.write
```

Funnel routes: `config/tailscale/apply-step-441.sh` (owner-run, needs the Tailscale operator).

## Logs

```bash
tail -f ~/Library/Logs/openclaw-octo-mcp.log
```

Every request is logged with its path and user agent; refusals include the reason, a `403` includes the WorkOS user ID so a new user can be allowlisted, and each `send_message` logs the destination name (never the message).
