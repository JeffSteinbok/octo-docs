---
layout: default
title: Config Backup
nav_order: 1
nav_exclude: true
---

# 🗄️ Config Backup

Backs up OpenClaw config to Git with SHA-256 change detection

## Configuration Schema

_No plugin config schema documented._

## Tools

### `config_backup_run`

Back up OpenClaw config and agent workspace to Git. Copies ~/.openclaw config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `check_only` | boolean | Optional | Only check for changes without committing. Default: `False`. |
| `force` | boolean | Optional | Force backup even if no changes detected. Default: `False`. |
| `verbose` | boolean | Optional | Include verbose diagnostic output. Default: `False`. |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/config-backup
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/config-backup.js --help

## Back up OpenClaw config and agent workspace to Git. Copies ~/.openclaw config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).
node dist/bin/config-backup.js config-backup-run <check_only> <force> <verbose>

## JSON output
node dist/bin/config-backup.js <command> [args...] --json
```
