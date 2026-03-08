---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Scheduled jobs are automated tasks that run at predefined intervals to perform specific actions, such as fetching data or creating backups. These jobs ensure that critical operations are performed consistently and on time.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run on a predefined schedule.
- **Job Schedule**: Specifies when and how often a job runs, using either cron expressions or time intervals.
- **Job Purpose**: Each job has a specific purpose, such as data fetching or backup.

## How It Works

1. Each job is configured with a name, description, and schedule.
2. Jobs are enabled or disabled based on their configuration.
3. The schedule determines when the job runs, using either:
   - **Cron Expressions**: Define specific times and days for execution.
   - **Fixed Intervals**: Specify a recurring time interval in milliseconds.
4. Enabled jobs execute automatically according to their schedule.

## List of Scheduled Jobs

| Job Name                  | Description                                      | Schedule Type | Schedule Details                     | Enabled |
|---------------------------|--------------------------------------------------|---------------|--------------------------------------|---------|
| `calendar-fetch-hourly`   | Fetch calendars hourly 7am-5pm PST               | Cron          | `0 7-17 * * *` (PST)                | Yes     |
| `config-backup`           | Backup `openclaw.json` to Git daily (only commits if changed) | Fixed Interval | Every 86,400,000 ms (24 hours)       | Yes     |
| `calendar-fetch-midnight` | Fetch calendars at midnight PST                  | Cron          | `0 0 * * *` (PST)                   | Yes     |
