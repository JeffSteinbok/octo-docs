---
layout: default
title: Config Backup
parent: Plugins
nav_order: 1
---

# 🗄️ Config Backup

Backs up OpenClaw config to Git with SHA-256 change detection

### `config_backup_run`

Back up OpenClaw config and agent workspace to Git. Copies ~/.openclaw config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `force` | boolean | Optional | Force backup even if no changes detected. Default: `False`. |
| `check_only` | boolean | Optional | Only check for changes without committing. Default: `False`. |
| `verbose` | boolean | Optional | Include verbose diagnostic output. Default: `False`. |
