---
layout: default
title: Services
nav_order: 5
---

# Services

OpenClaw services are background processes that keep long-running automations available between conversations.


## Service Summary

| Service | Description | Docs |
|---------|-------------|------|
| 📡 FastMail SSE Service | Real-time email notification daemon using JMAP EventSource | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) |
| ⚙️ Octo Satellite | Local secrets broker providing credentialed access to Amazon and Monarch Money without exposing passwords or session cookies to the gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ OneDrive Sync | Keeps the Obsidian vault and other files synced to Microsoft OneDrive via `abraunegg/onedrive` | [Details ↓](#onedrive-sync) |
| 📝 Obsidian Vault Indexer | Long-running indexer that maintains a SQLite FTS5 index of the Obsidian vault for full-text search | [GitHub ↗](https://github.com/JeffSteinbok/carapace-obsidian) |

---

## OneDrive Sync

The OneDrive sync service keeps the Obsidian vault (and other files under `~/OneDrive/`) in sync with Microsoft OneDrive using the open-source [`abraunegg/onedrive`](https://github.com/abraunegg/onedrive) Linux client.

### Setup

The client runs as a user systemd service in `--monitor` mode, which uses inotify to react to local file changes in near real-time, plus a full rescan every 5 minutes.

```bash
# Check status
systemctl --user status onedrive

# View logs
journalctl --user -u onedrive -n 50 --no-pager

# Restart
systemctl --user restart onedrive
```

No custom config file is present at `~/.config/onedrive/config` — the client runs on defaults.

### Known Issue: 404 itemNotFound Loop

Occasionally the client enters a state where it repeatedly receives `HTTP 404 itemNotFound` errors from the Microsoft OneDrive API. This typically manifests as:

- New folders or files not appearing in OneDrive on other devices
- Repeated identical errors in the journal every ~30 seconds
- The client not recovering on its own

The root cause is likely a stale delta state — the client holds item IDs that no longer match what the API expects, usually triggered when new folders are created locally before the API has confirmed the parent.

**Workaround:** Simply restart the service. It will perform a clean initial sync and re-establish its state.

```bash
systemctl --user restart onedrive
```

### Watchdog (Planned)

To avoid having to manually restart the service, a systemd watchdog is planned with the following components:

**`~/.config/onedrive/watchdog.sh`** — checks for ≥5 `itemNotFound` errors in the last 2 minutes and restarts the service if found, logging to `~/.config/onedrive/watchdog.log`.

**`~/.config/systemd/user/onedrive-watchdog.service`** — oneshot service that runs the script.

**`~/.config/systemd/user/onedrive-watchdog.timer`** — timer that fires every 5 minutes.

Enable with:
```bash
chmod +x ~/.config/onedrive/watchdog.sh
systemctl --user daemon-reload
systemctl --user enable --now onedrive-watchdog.timer
```

### cURL / HTTP2 Warning

The client logs a warning about cURL 8.5.0 having known HTTP/2 bugs and automatically falls back to HTTP/1.1. Ubuntu 24.04's apt repos don't carry a newer cURL version. The fallback is functional — this warning can be ignored.

---

## Obsidian Vault Indexer

The Obsidian Vault Indexer is a long-running service that watches the vault directory and maintains a SQLite FTS5 full-text search index. It's part of the [`carapace-obsidian`](https://github.com/JeffSteinbok/carapace-obsidian) plugin, which pairs with OneDrive to give Octo read access to Jeff's notes.

### Architecture

```
┌────────────────────┐       ┌──────────────────┐       ┌────────────────┐
│  Obsidian Vault    │       │  Indexer Service  │       │  Plugin (r/o)  │
│  (markdown files)  │──────▶│  (chokidar watch) │──────▶│  (VaultReader) │
│                    │ watch  │  SQLite FTS5 DB   │ read  │  6 tools       │
└────────────────────┘       └──────────────────┘       └────────────────┘
```

- **Indexer** — watches the vault via `chokidar`, parses markdown (frontmatter, tags, wikilinks), and writes to a SQLite FTS5 database in WAL mode.
- **Plugin** — read-only; opens the DB with `readonly: true` so it never conflicts with the indexer.
- **Vault location** — `~/OneDrive/JeffBrain/` (synced via OneDrive, see above)

See the [carapace-obsidian GitHub repo ↗](https://github.com/JeffSteinbok/carapace-obsidian) for installation and configuration details.
