---
output: jobs.md
title: Scheduled Jobs
nav_order: 5
data_source: jobs
empty_message: "_No scheduled jobs configured._"
---

<!-- instructions:
  Shows all scheduled/cron jobs from two sources:
  1. OpenClaw jobs in ~/.openclaw/cron/jobs.json — table with name,
     description, cron schedule, and enabled/disabled status.
  2. System crontab entries — table with schedule, command, and description.

  If no jobs exist in either source, show the empty_message from frontmatter.
-->

{{ items }}

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
