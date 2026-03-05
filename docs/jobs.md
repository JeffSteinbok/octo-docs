---
layout: default
title: Scheduled Jobs
nav_order: 4
---

# Scheduled Jobs

Cron-style jobs that run automatically on a schedule. Each job spawns an
isolated agent session, executes its task, and exits — no user interaction
required.

| Job | Description | Schedule | Status |
|-----|-------------|----------|--------|
| **calendar-fetch** | Fetch next 7 days from work, personal, Nicole, and family calendars every 12h | Every 12h | ✅ Enabled |
| **config-backup** | Backup openclaw.json to Git daily (only commits if changed) | Every 1d | ✅ Enabled |

## How It Works

Jobs are defined in `cron/jobs.json` inside the `.openclaw` directory.
The OpenClaw gateway reads this file and fires each job on its configured
schedule. Jobs run in isolated sessions so they don't pollute the main
conversation history.

Agents can create, edit, and delete jobs at runtime — for example,
`"remind me in 20 minutes"` creates a one-shot cron job that delivers
a message back through the active channel.