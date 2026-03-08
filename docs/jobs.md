---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Scheduled jobs are automated tasks that run at predefined intervals to perform specific operations, such as fetching data or creating backups. These jobs ensure that critical processes are executed reliably and on time.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Job Scheduling**: Jobs can be scheduled using either cron expressions or fixed intervals in milliseconds.
- **Time Zones**: Some jobs are configured to run in a specific time zone.

## How It Works

1. Each job is defined with a name, description, and schedule.
2. Jobs can be enabled or disabled as needed.
3. The scheduling mechanism ensures that jobs run at the specified times or intervals.
4. Cron-based jobs use a cron expression and time zone to determine their execution schedule.
5. Interval-based jobs run at fixed time intervals, specified in milliseconds.

## List of Scheduled Jobs

| Job Name                  | Description                                      | Schedule Type | Schedule Details                     | Enabled |
|---------------------------|--------------------------------------------------|---------------|---------------------------------------|---------|
| `calendar-fetch-hourly`   | Fetch calendars hourly 7am-5pm PST               | Cron          | `0 7-17 * * *` (America/Los_Angeles) | Yes     |
| `config-backup`           | Backup openclaw.json to Git daily (only commits if changed) | Interval      | Every 86400000ms                     | Yes     |
| `calendar-fetch-midnight` | Fetch calendars at midnight PST                  | Cron          | `0 0 * * *` (America/Los_Angeles)    | Yes     |
