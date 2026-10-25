---
layout: default
title: Octo MCP
parent: Services
nav_order: 4
---

# Octo MCP

MCP server that lets OctoDot, an OpenAI Dot in ChatGPT, reach Octo. Every request needs a WorkOS AuthKit access token, checked before the request body is read, and only the owner's WorkOS account is allowed. The service source lives in [`openclaw-hub/services/octo-mcp`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/octo-mcp); on the Mac mini it runs from the LaunchAgent `com.octo.openclaw.octo-mcp`, backed up in this repo at `config/macos/launchd/`. See [MCP & OctoDot](../mcp) for the whole picture.

## Features

- Streamable HTTP MCP, stateless, at `https://<funnel-host>/mcp`
- OAuth 2.1 resource server: protected resource metadata (RFC 9728), and AuthKit's authorization server metadata proxied for clients that look for it on this origin
- Access tokens checked for JWKS signature, issuer, audience (the MCP URL), expiry, and a one-person allowlist
- Fails closed: refuses to start without an AuthKit issuer, never serves `/mcp` unauthenticated
- Host header allowlist, POST only, 1 MiB body limit
- Holds no secrets
- Tools: `ping` (live); `ask_octo` (planned)

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
| `OCTO_MCP_ALLOWED_HOSTS` | no | Host header allowlist |
| `OCTO_MCP_PORT` | no | Listen port (default 18793) |

None of these are secrets, so they live in the LaunchAgent's `EnvironmentVariables`.

## Install

```bash
cd ~/git/openclaw-hub/services/octo-mcp
npm ci && npm run build && npm test
cp ~/git/octo/config/macos/launchd/com.octo.openclaw.octo-mcp.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.octo.openclaw.octo-mcp.plist
```

Funnel routes: `config/tailscale/apply-step-441.sh` (owner-run, needs the Tailscale operator).

## Logs

```bash
tail -f ~/Library/Logs/openclaw-octo-mcp.log
```

Every request is logged with its path and user agent; refusals include the reason, and a `403` includes the WorkOS user ID so a new user can be allowlisted.
