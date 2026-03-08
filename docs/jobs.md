---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This document provides an overview of scheduled jobs available in the system. These jobs are automated tasks designed to perform specific functions at predefined intervals. They help ensure that critical operations, such as data fetching and backups, are performed consistently and reliably.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific intervals or times.
- **Cron Schedule**: A time-based job scheduler used to execute tasks at specific times or intervals.
- **Interval Schedule**: A job scheduler that runs tasks at fixed time intervals, measured in milliseconds.
- **Time Zones**: Some jobs are scheduled based on specific time zones.

## How It Works

1. Each job is defined with a name, description, and schedule.
2. Jobs can be scheduled using either a cron expression or a fixed interval in milliseconds.
3. Enabled jobs run automatically based on their defined schedule.

## List of Scheduled Jobs

### `calendar-fetch-hourly`

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: 
  - **Type**: Cron
  - **Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles
- **Enabled**: Yes

### `config-backup`

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits are only made if changes are detected.
- **Schedule**: 
  - **Type**: Interval
  - **Interval**: Every 86,400,000 milliseconds (24 hours)
- **Enabled**: Yes

### `calendar-fetch-midnight`

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: 
  - **Type**: Cron
  - **Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles
- **Enabled**: Yes
