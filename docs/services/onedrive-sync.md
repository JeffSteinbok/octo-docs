---
layout: default
title: OneDrive Sync
parent: Services
nav_order: 1
---

# OneDrive Sync

Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive using the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) Linux client.

## Features

- Runs as a user systemd service in `--monitor` mode
- Uses inotify to react to local file changes in near real-time
- Full rescan every 5 minutes as a safety net
- WebSocket support for Microsoft Graph API change notifications

## Setup

The client runs with no custom config file — all defaults. It is installed via apt and enabled as a user systemd service.

```bash
# Check status
systemctl --user status onedrive

# View logs
journalctl --user -u onedrive -n 50 --no-pager

# Restart
systemctl --user restart onedrive
```

## Known Issue: 404 itemNotFound Loop

Occasionally the client enters a state where it repeatedly receives `HTTP 404 itemNotFound` errors from the Microsoft OneDrive API. This typically manifests as:

- New folders or files not appearing in OneDrive on other devices
- Repeated identical errors in the journal every ~30 seconds
- The client not recovering on its own

The root cause is likely a stale delta state — the client holds item IDs that no longer match what the API expects, usually triggered when new folders are created locally before the API has confirmed the parent.

**Workaround:** Restart the service. It will perform a clean initial sync and re-establish state.

```bash
systemctl --user restart onedrive
```

## Watchdog (Planned)

Source files live in the `octo` repo:

- `scripts/onedrive-watchdog.sh` — the watchdog script
- `scripts/systemd/onedrive-watchdog.service` — oneshot service unit
- `scripts/systemd/onedrive-watchdog.timer` — 5-minute timer unit

Deploy with:

```bash
cp scripts/onedrive-watchdog.sh ~/.config/onedrive/watchdog.sh
chmod +x ~/.config/onedrive/watchdog.sh
cp scripts/systemd/onedrive-watchdog.service ~/.config/systemd/user/
cp scripts/systemd/onedrive-watchdog.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now onedrive-watchdog.timer
```

The script checks for ≥5 `itemNotFound` errors in the last 2 minutes and restarts the service if found, logging to `~/.config/onedrive/watchdog.log`.

## cURL / HTTP2 Warning

The client logs a warning about cURL 8.5.0 having known HTTP/2 bugs and automatically falls back to HTTP/1.1. Ubuntu 24.04's apt repos don't carry a newer cURL version. The fallback is functional — this warning can be ignored.
