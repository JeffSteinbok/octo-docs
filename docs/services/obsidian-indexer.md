---
layout: default
title: Obsidian Vault Indexer
parent: Services
nav_order: 2
---

# Obsidian Vault Indexer

Long-running service that watches the Obsidian vault and keeps a SQLite full-text search index (FTS5) of it up to date, so the [`carapace-obsidian`](https://github.com/JeffSteinbok/carapace-obsidian) plugin can search notes without reading every file. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.obsidian-indexer` (backed up in `config/macos/launchd/`).

## Features

- Watches the vault with `chokidar` and re-indexes files as they change
- Parses Markdown front matter, tags and `[[wikilinks]]`
- Keeps the index in a SQLite FTS5 database in WAL mode, so reads and writes can happen at the same time
- The plugin opens the database read-only, so it never conflicts with the indexer
- Supports prefix matching (`wash` finds `washer` and `washing`) and OR queries

## Architecture

```
┌──────────────────┐       ┌──────────────────┐       ┌────────────────┐
│ Obsidian vault   │       │ Indexer service  │       │ Plugin (r/o)   │
│ (Markdown files) │──────▶│ (chokidar watch) │──────▶│ (VaultReader)  │
│                  │ watch │ SQLite FTS5 DB   │  read │ vault tools    │
└──────────────────┘       └──────────────────┘       └────────────────┘
```

## Vault location

The vault is `~/OneDrive/JeffBrain/`, synced from the owner's other devices by OneDrive (see [OneDrive Sync](onedrive-sync)).

## Environment Variables

The LaunchAgent sets both:

| Variable | Required | Description |
|---|---|---|
| `OBSIDIAN_VAULT_ROOT` | yes | Vault folder to watch (on the Mac mini, the `JeffBrain` folder in OneDrive) |
| `OBSIDIAN_INDEX_LOCATION` | no | Where the index database is written (default `~/.openclaw/obsidian-index.db`) |

## Logs

```bash
tail -f ~/Library/Logs/openclaw-obsidian-indexer.log
launchctl kickstart -k gui/$(id -u)/com.octo.openclaw.obsidian-indexer   # restart
```

## Source

The indexer and the OpenClaw plugin are both distributed from the [carapace-obsidian](https://github.com/JeffSteinbok/carapace-obsidian) repo, which has the full installation and configuration details.
