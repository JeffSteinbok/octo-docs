# Scheduled Jobs Overview

## Overview

This page provides an overview of the scheduled jobs available in the system. Scheduled jobs are automated tasks that run at predefined intervals to perform specific operations, such as fetching data or creating backups. These jobs help ensure the system remains up-to-date and reliable without requiring manual intervention.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency at which the job runs.
  - **Cron Schedule**: Specifies exact times and days for execution.
  - **Interval Schedule**: Specifies a recurring interval in milliseconds.
- **Time Zone**: Relevant for jobs scheduled using cron expressions.

## How It Works

1. Each job is configured with a name, description, and schedule.
2. Jobs with a cron schedule run at specific times based on the provided cron expression and time zone.
3. Jobs with an interval schedule run at regular intervals, measured in milliseconds.
4. Enabled jobs execute automatically according to their schedule.

## List of Scheduled Jobs

| Job Name                  | Description                                      | Schedule Type | Schedule Details                       |
|---------------------------|--------------------------------------------------|---------------|----------------------------------------|
| `calendar-fetch-hourly`   | Fetch calendars hourly 7am-5pm PST               | Cron          | `0 7-17 * * *` (America/Los_Angeles)  |
| `config-backup`           | Backup openclaw.json to Git daily (only commits if changed) | Interval      | Every 86400000ms (24 hours)           |
| `calendar-fetch-midnight` | Fetch calendars at midnight PST                  | Cron          | `0 0 * * *` (America/Los_Angeles)     |

## Common Pitfalls

- Ensure the time zone (`tz`) is correctly configured for cron-based jobs to avoid unexpected execution times.
- For interval-based jobs, verify that the interval duration (`everyMs`) aligns with the intended frequency.
- Disabled jobs will not run; ensure jobs are enabled if they are required for critical operations.
