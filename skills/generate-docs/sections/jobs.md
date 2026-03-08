---
output: jobs.md
title: Scheduled Jobs
nav_order: 6
data_keys:
  - jobs
---

Generate a documentation section for OpenClaw **scheduled jobs**.

Use the `jobs` array from the provided data. If the array is empty,
output only: "_No scheduled jobs configured._"

Group jobs by their `source` field and render each group:

### OpenClaw Jobs (`cron/jobs.json`) — where source is `"openclaw"`

Render a markdown table: **Job**, **Description**, **Schedule**, **Status**

- **Schedule**: use the `interval` field
- **Status**: `✅ Enabled` if `enabled` is true, otherwise `❌ Disabled`

### System Crontab (`crontab -e`) — where source is `"crontab"`

Render a markdown table: **Job**, **Schedule**

After the job tables, include this explanatory content verbatim:

## How It Works

Jobs are defined in `cron/jobs.json` inside the `.openclaw` directory.
The OpenClaw gateway reads this file and fires each job on its configured
schedule. Jobs run in isolated sessions so they don't pollute the main
conversation history.

Agents can create, edit, and delete jobs at runtime — for example,
`"remind me in 20 minutes"` creates a one-shot cron job that delivers
a message back through the active channel.

## Note: Two Places for Scheduled Tasks

Scheduled tasks are configured in **two places** — check both:

- **`~/.openclaw/cron/jobs.json`** — OpenClaw's built-in cron scheduler (listed above)
- **`crontab -e`** — System crontab for tasks that run outside OpenClaw (e.g. `opentable-heartbeat.sh`)
