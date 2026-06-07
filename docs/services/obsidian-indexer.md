---
layout: default
title: Obsidian Vault Indexer
parent: Services
nav_order: 2
---

# Obsidian Vault Indexer

Long-running systemd service that watches the Obsidian vault directory and maintains a SQLite FTS5 full-text search index. Part of the [carapace-obsidian](https://github.com/JeffSteinbok/carapace-obsidian) plugin.

## Features

- Watches the vault via `chokidar` for real-time file change detection
- Parses markdown frontmatter, tags, and `[[wikilinks]]`
- Maintains a SQLite FTS5 database in WAL mode for concurrent access
- Plugin opens the DB with `readonly: true` — never conflicts with the indexer
- Supports prefix matching (`wash` → `washer`, `washing`) and OR queries

## Architecture

```
┌────────────────────┐       ┌──────────────────┐       ┌────────────────┐
│  Obsidian Vault    │       │  Indexer Service  │       │  Plugin (r/o)  │
│  (markdown files)  │──────▶│  (chokidar watch) │──────▶│  (VaultReader) │
│                    │ watch  │  SQLite FTS5 DB   │ read  │  6 tools       │
└────────────────────┘       └──────────────────┘       └────────────────┘
```

## Vault Location

The vault lives at `~/OneDrive/JeffBrain/` and is synced from other devices via the OneDrive Sync service.

## Source

See the [carapace-obsidian](https://github.com/JeffSteinbok/carapace-obsidian) GitHub repo for full installation and configuration details. The indexer service and OpenClaw plugin are both distributed from that repo.
