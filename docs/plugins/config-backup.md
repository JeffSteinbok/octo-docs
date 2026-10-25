---
layout: default
title: Config Backup
nav_order: 1
nav_exclude: true
---

# 🗄️ Config Backup

Commits OpenClaw's config and the agent workspaces to Git, only when something has changed.

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

## Command-Line Use

Building the plugin also produces a standalone command-line version, with one command per tool. Add `--json` to any command for JSON output.

```bash
cd plugins/config-backup
npm install && npm run build
node dist/bin/config-backup.js --help
```

Commands:

```bash
node dist/bin/config-backup.js config-backup-run <check_only> <force> <verbose>
```
