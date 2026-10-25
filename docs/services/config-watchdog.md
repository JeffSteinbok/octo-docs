---
layout: default
title: Config Watchdog
parent: Services
nav_order: 6
---

# Config Watchdog

> **Source:** [openclaw-hub/services/config-watchdog](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/config-watchdog)

Watches OpenClaw's config file, `openclaw.json`, and brings the Gateway back if a change breaks it. **It isn't running on the Mac mini:** the service ships only a Linux systemd unit, and Octo hasn't had a LaunchAgent for it since the move to macOS on 2026-10-21. Until there is one, a bad config change has to be fixed by hand (`openclaw doctor`, or restore `~/.openclaw/openclaw.json.last-good`).

## Features

- Keeps up to 10 numbered backups of the config, refreshed on every change
- Checks the Gateway's health after each change and marks a healthy config as last-good
- When the Gateway is unhealthy, works down a recovery ladder: the last-good config, then each backup in turn, then `openclaw doctor fix`, restarting and re-checking after each step
- If nothing works, files a GitHub issue with the `doctor` output and stops
- Never deletes anything: a bad config is kept as `openclaw.json.bad.<timestamp>`

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENCLAW_CONFIG_FILE` | no | Config file to watch (default `~/.openclaw/openclaw.json`) |
| `WATCHDOG_BACKUP_VERSIONS` | no | Number of numbered backups to keep (default 10) |
| `OPENCLAW_GATEWAY_URL` | no | Gateway address for health checks (default `http://127.0.0.1:18789`) |
| `OPENCLAW_LAUNCHD_LABEL` | no | LaunchAgent to restart on macOS (default `ai.openclaw.gateway`) |
| `GITHUB_TOKEN` | for incidents | Token used to file the GitHub issue |

The [config-watchdog README](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/config-watchdog) lists every setting and the full recovery sequence.
