---
layout: default
title: OneDrive Sync
parent: Services
nav_order: 1
---

# OneDrive Sync

Keeps the Obsidian vault and other files under `~/OneDrive/` in sync with Microsoft OneDrive, so notes written on the owner's other devices reach Octo and the [Obsidian Vault Indexer](obsidian-indexer). On the Mac mini this is the Microsoft OneDrive app; nothing from this repo runs there. On a Linux host it is the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) client, set up as described below.

## Features

- macOS: the Microsoft OneDrive app syncs to `~/Library/CloudStorage/OneDrive-Personal`, and `~/OneDrive` is a symlink to that folder, so paths under `~/OneDrive/` are the same on either platform
- Linux: runs as a user systemd service in `--monitor` mode
- Linux: uses inotify to pick up local file changes in near real time, with a full rescan every 5 minutes as a safety net
- Linux: uses Microsoft Graph change notifications over WebSocket to pick up remote changes

## On the Mac mini

Sign in to the OneDrive app with the owner's Microsoft account and let it sync to its default location. Then link the folder to the path Octo uses:

```bash
ls -l ~/OneDrive   # should point to ~/Library/CloudStorage/OneDrive-Personal
ln -s ~/Library/CloudStorage/OneDrive-Personal ~/OneDrive   # only if the link is missing
```

Add OneDrive to **System Settings → General → Login Items & Extensions → Open at Login** (or turn on its "OneDrive Launcher" background item there). Without it the app doesn't come back after a reboot and the vault quietly stops syncing; check with `pgrep -x OneDrive`.

The app manages its own sync and logs; there is no LaunchAgent or config in this repo for it.

## On a Linux host

Everything from here on applies only to a Linux host running the `abraunegg/onedrive` client. Octo ran this way before it moved to the Mac mini on 2026-10-21.

### Setup

The client runs with no custom config file (all defaults). It is installed from apt and enabled as a user systemd service.

```bash
systemctl --user status onedrive                    # check status
journalctl --user -u onedrive -n 50 --no-pager      # view logs
systemctl --user restart onedrive                   # restart
```

### Known issue: 404 itemNotFound loop

Occasionally the client gets stuck repeatedly receiving `HTTP 404 itemNotFound` errors from the OneDrive API. Signs:

- New folders or files don't appear in OneDrive on other devices
- The same error repeats in the journal about every 30 seconds
- The client doesn't recover on its own

The likely cause is stale sync state: the client holds item IDs that no longer match what the API expects, usually after new folders are created locally before the API has confirmed their parent.

**Workaround:** restart the service. It does a clean initial sync and rebuilds its state.

```bash
systemctl --user restart onedrive
```

### Watchdog (planned)

To avoid restarting by hand, a watchdog timer is planned. Its files are in this repo:

- `scripts/onedrive-watchdog.sh`: the watchdog script
- `scripts/systemd/onedrive-watchdog.service`: oneshot service unit
- `scripts/systemd/onedrive-watchdog.timer`: 5-minute timer unit

Deploy with:

```bash
cp scripts/onedrive-watchdog.sh ~/.config/onedrive/watchdog.sh
chmod +x ~/.config/onedrive/watchdog.sh
cp scripts/systemd/onedrive-watchdog.service ~/.config/systemd/user/
cp scripts/systemd/onedrive-watchdog.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now onedrive-watchdog.timer
```

The script restarts the service if it finds 5 or more `itemNotFound` errors in the last 2 minutes, and logs to `~/.config/onedrive/watchdog.log`.

### cURL HTTP/2 warning

The client warns that cURL 8.5.0 has known HTTP/2 bugs and falls back to HTTP/1.1. Ubuntu 24.04's apt repositories don't carry a newer cURL. The fallback works, so the warning can be ignored.
