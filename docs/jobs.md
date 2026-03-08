# Scheduled Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Scheduled jobs are automated tasks that run at predefined intervals to perform specific operations, such as data synchronization or backups. These jobs help ensure that critical processes are executed reliably and on time.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency at which the job runs.
  - **Cron Schedule**: Specifies the exact times a job runs using a cron expression.
  - **Interval Schedule**: Specifies the time interval between job executions.
- **Time Zone**: The time zone in which the schedule is defined.

## How It Works

1. Each job is configured with a name, description, and schedule.
2. Jobs with a cron schedule run at specific times based on the cron expression and time zone.
3. Jobs with an interval schedule run at regular intervals, defined in milliseconds.
4. Enabled jobs are executed automatically according to their schedule.

## List of Scheduled Jobs

| Job Name                  | Description                                    | Schedule Type | Schedule Details                     | Time Zone          |
|---------------------------|------------------------------------------------|---------------|--------------------------------------|--------------------|
| `calendar-fetch-hourly`   | Fetch calendars hourly 7am-5pm PST             | Cron          | `0 7-17 * * *`                       | America/Los_Angeles |
| `config-backup`           | Backup `openclaw.json` to Git daily            | Interval      | Every 86400000ms (24 hours)          | N/A                |
| `calendar-fetch-midnight` | Fetch calendars at midnight PST                | Cron          | `0 0 * * *`                          | America/Los_Angeles |

## Common Pitfalls

- **Time Zone Awareness**: Ensure that the time zone for cron-based jobs is correctly understood and aligned with the desired execution times.
- **Disabled Jobs**: Verify that jobs are enabled if they are expected to run. Disabled jobs will not execute.
- **Cron Expression Syntax**: Ensure that cron expressions are correctly formatted to avoid unintended schedules.
