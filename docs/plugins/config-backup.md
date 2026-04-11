---
layout: default
title: Config Backup
parent: Plugins
nav_order: 1
---

# 🗄️ Config Backup

Backs up OpenClaw config to Git with SHA-256 change detection. Ensures that configuration and agent workspace files are committed and pushed only when content changes.

### config_backup_run

Back up OpenClaw config and agent workspace to Git. Copies ~/.openclaw config files into the Git repo, commits, and pushes only when content has changed (SHA-256 detection).

| Name        | Type    | Description                                 |
|-------------|---------|---------------------------------------------|
| force       | boolean | Force backup even if no changes detected    |
| check_only  | boolean | Only check for changes without committing   |
| verbose     | boolean | Include verbose diagnostic output           |
