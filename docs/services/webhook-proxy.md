---
layout: default
title: Webhook Proxy
parent: Services
nav_order: 3
---

# Webhook Proxy

Auth-validating proxy between Tailscale Funnel and OpenClaw's hooks endpoint. Each route checks the sender's own auth scheme (HMAC-SHA256 signature or <redacted-bearer-token>), optionally filters out events that shouldn't wake an agent, and forwards what's left to OpenClaw with the hooks <redacted-bearer-token> added. The service source lives in [`openclaw-hub/services/webhook-proxy`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/webhook-proxy); this folder holds Octo's systemd unit (Linux) and setup notes. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.webhook-proxy`, backed up in this repo at `config/macos/launchd/`.

## Features

- Per-route inbound auth, so each webhook sender keeps its own secret and OpenClaw's hooks token never leaves the machine
- Optional per-route filters that drop events before they reach the gateway
- Forwards to OpenClaw's local `/hooks/*` endpoint with the hooks <redacted-bearer-token> injected
- Runs as a per-user service (launchd LaunchAgent on macOS, systemd user unit on Linux) on `127.0.0.1:18792`, exposed only through Tailscale Funnel paths under `/hooksproxy/`

## Routes

| Path | Auth | Filter | Forwards to |
|------|------|--------|-------------|
| `/hooksproxy/github-issues` | HMAC-SHA256 (`X-Hub-Signature-256`) | GitHub issues from allowed senders carrying an actionable `ilc:` label (`ilc:approved`, `ilc:plan-approved`, `ilc:pr-needs-work`) | `/hooks/github-issues` |

## Files

| File | Purpose |
|------|---------|
| `webhook-proxy.service` | systemd user unit (Linux) |
| `config/macos/launchd/com.octo.openclaw.webhook-proxy.plist` | launchd LaunchAgent (macOS), installed at `~/Library/LaunchAgents/` |
| `~/.openclaw/services/webhook-proxy-config.json` | Route config (this repo: `config/webhook-proxy-config.json` → symlink or copy) |
| `~/.openclaw/.env` | Secrets (OPENCLAW_HOOKS_TOKEN, GITHUB_WEBHOOK_SECRET) |

## Required .env vars

Add to `~/.openclaw/.env`:

```env
OPENCLAW_HOOKS_TOKEN=<openclaw hooks.*** value>
GITHUB_WEBHOOK_SECRET=<secret you set in GitHub webhook settings>
```

## Install

```bash

## Build the service
cd ~/git/openclaw-hub/services/webhook-proxy
npm install
npm run build

## macOS: install the LaunchAgent
cp ~/git/octo/config/macos/launchd/com.octo.openclaw.webhook-proxy.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.octo.openclaw.webhook-proxy.plist
launchctl print gui/$(id -u)/com.octo.openclaw.webhook-proxy

## Linux: install the systemd unit
cp ~/git/octo/services/webhook-proxy/webhook-proxy.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable webhook-proxy
systemctl --user start webhook-proxy
systemctl --user status webhook-proxy
```

## Tailscale Funnel routing

Add the proxy path (run once — Tailscale persists this):

```bash
tailscale serve --https=443 /hooksproxy/github-issues http://127.0.0.1:18792/hooksproxy/github-issues
```

Verify:

```bash
tailscale funnel status
```

Expected output should show `/hooksproxy/github-issues` → `http://127.0.0.1:18792`.

## GitHub webhook setup

In `JeffSteinbok/octo` → Settings → Webhooks → Add webhook:

- **Payload URL:** `https://<tailnet-host>/hooksproxy/github-issues`
- **Content type:** `application/json`
- **Secret:** value of `GITHUB_WEBHOOK_SECRET`
- **Events:** Let me select individual events → ✅ Issues, ✅ Pull requests

## Logs

```bash

## macOS
tail -f ~/Library/Logs/openclaw-webhook-proxy.log

## Linux
journalctl --user -u webhook-proxy -f
```

## Adding a new route

1. Edit `~/.openclaw/services/webhook-proxy-config.json` — add a new entry to `routes`
2. Add the new secret env var to `~/.openclaw/.env`
3. Add Tailscale Funnel path: `tailscale serve --https=443 /hooksproxy/<path> http://127.0.0.1:18792/hooksproxy/<path>`
4. Restart: `launchctl kickstart -k gui/$(id -u)/com.octo.openclaw.webhook-proxy` on macOS, `systemctl --user restart webhook-proxy` on Linux
