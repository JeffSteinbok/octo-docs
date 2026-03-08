# Scheduled Jobs Overview

## Overview

This page provides an overview of the scheduled jobs available in the system. Scheduled jobs are automated tasks that run at predefined intervals to perform essential operations such as data fetching and backups. These jobs ensure that critical processes are executed reliably and on time.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs.
  - **Cron Schedule**: Specifies exact times using a cron expression.
  - **Interval Schedule**: Specifies a recurring interval in milliseconds.
- **Time Zone**: Indicates the time zone used for scheduling.

## How It Works

1. Each job is configured with a unique name, description, and schedule.
2. Jobs with a cron schedule run at specific times defined by the cron expression.
3. Jobs with an interval schedule run at regular intervals based on the specified duration.
4. All jobs are enabled by default and execute automatically according to their schedule.

## Scheduled Jobs

| Job Name                 | Description                                      | Schedule Type | Schedule Details                     | Time Zone          |
|--------------------------|--------------------------------------------------|---------------|--------------------------------------|--------------------|
| `calendar-fetch-hourly`  | Fetch calendars hourly 7am-5pm PST               | Cron          | `0 7-17 * * *`                       | America/Los_Angeles |
| `config-backup`          | Backup openclaw.json to Git daily (only commits if changed) | Interval       | Every 86400000 milliseconds (24 hours) | N/A                |
| `calendar-fetch-midnight`| Fetch calendars at midnight PST                  | Cron          | `0 0 * * *`                          | America/Los_Angeles |
