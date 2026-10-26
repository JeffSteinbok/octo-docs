---
layout: default
title: Webhook Proxy
parent: Services
nav_order: 3
---

# Webhook Proxy

> **Source:** [openclaw-hub/services/webhook-proxy](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy)

Auth-validating proxy between the outside world and OpenClaw's hooks endpoint. Each route checks the sender's own credential (an HMAC-SHA256 signature or a per-sender token), optionally drops events that shouldn't wake an agent, and forwards the rest to the Gateway with the hooks token added, so no external sender ever holds the real hooks token. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy` (backed up in `config/macos/launchd/`).

## Features

- Per-route inbound auth, so each sender has its own secret and OpenClaw's hooks token never leaves the machine
- Per-route filters that drop events before they reach the Gateway (GitHub: allowed senders and actionable labels only)
- Exact path matching, POST only, 1 MiB body limit, and a lockout after 10 failed auth attempts in a minute
- Listens on port 18792 on all interfaces (`bind_host: 0.0.0.0` in the config; the code's default is `127.0.0.1`): Tailscale Funnel reaches it on loopback through the `/hooksproxy` mount, and Home Assistant reaches it on the LAN
- The LaunchAgent loads only its own env file, `~/.openclaw/secrets/webhook-proxy.env`, not the shared OpenClaw `.env`. (The Linux `webhook-proxy.service` unit in this folder is from the retired host and still loads `~/.openclaw/.env`.)

## Routes

Each route forwards to one of the [hooks](../hooks) on the Gateway. Funnel mounts `/hooksproxy` on the proxy and strips the prefix (see [Funnel routes](../external-integrations#funnel-routes)), so the public URL `https://<funnel-host>/hooksproxy/<route>` arrives as `/<route>`.

| Route | Sender | Auth | Filter | Forwards to |
|---|---|---|---|---|
| `/github-issues` | GitHub (`JeffSteinbok/octo` webhook) | HMAC-SHA256 (`X-Hub-Signature-256`) | Drops pings, senders other than the owner and Octo's bot, and labels other than the actionable `ilc:` ones | `/hooks/github-issues` |
| `/hass` | Home Assistant (LAN, `http://<mac-lan-ip>:18792/hass`) | Per-sender token (`Authorization` header) | None | `/hooks/hass` |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENCLAW_HOOKS_TOKEN` | yes | OpenClaw hooks token, added to forwarded requests. Rotate it together with `~/.openclaw/.env` |
| `GITHUB_ISSUES_HOOK_SECRET` | yes | Secret configured on the GitHub webhook |
| `HOOKSPROXY_HASS_TOKEN` | yes | Token Home Assistant sends in the `Authorization` header on `/hass` |

All three live in `~/.openclaw/secrets/webhook-proxy.env` (mode 600). The route list is `~/.openclaw/services/webhook-proxy-config.json` (route paths, auth types and env var names only, no secret values).

## Files

| File | Purpose |
|---|---|
| `config/macos/launchd/com.octo.openclaw.webhook-proxy.plist` | LaunchAgent (macOS), installed at `~/Library/LaunchAgents/` |
| `services/webhook-proxy/webhook-proxy.service` | systemd user unit, for running on a Linux host instead (not used on the Mac mini) |
| `~/.openclaw/services/webhook-proxy-config.json` | Route config |
| `~/.openclaw/secrets/webhook-proxy.env` | Secrets (see above) |

## Install

```bash

## Build the service
cd ~/git/openclaw-hub/services/webhook-proxy
npm ci && npm run build && npm test

## macOS: install the LaunchAgent
cp ~/git/octo/config/macos/launchd/com.octo.openclaw.webhook-proxy.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.octo.openclaw.webhook-proxy.plist
launchctl print gui/$(id -u)/com.octo.openclaw.webhook-proxy
```

Funnel: one mount, `tailscale funnel --bg --set-path=/hooksproxy http://127.0.0.1:18792`. Funnel changes need the Tailscale operator; see `config/tailscale/restore-funnel.sh` and the `apply-step-*.sh` scripts.

## GitHub webhook setup

In `JeffSteinbok/octo` → Settings → Webhooks:

- **Payload URL:** `https://<funnel-host>/hooksproxy/github-issues`
- **Content type:** `application/json`
- **Secret:** the value of `GITHUB_ISSUES_HOOK_SECRET`
- **Events:** Issues

## Logs

```bash
tail -f ~/Library/Logs/openclaw-webhook-proxy.log   # macOS
journalctl --user -u webhook-proxy -f               # Linux
```

Each request logs its route, auth result, filter decision and the Gateway's response. Rejections are logged with the reason; secret values never are.

## Adding a route

1. Add the route to `~/.openclaw/services/webhook-proxy-config.json` with its auth type and the name of its secret's env var.
2. Add the secret to `~/.openclaw/secrets/webhook-proxy.env`.
3. Restart: `launchctl kickstart -k gui/$(id -u)/com.octo.openclaw.webhook-proxy`.
4. The existing `/hooksproxy` Funnel mount already covers new routes; no Funnel change is needed.
5. Add a rejection check for the route to `scripts/smoke-remote-access.sh`.
