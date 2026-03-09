---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. These jobs are automated tasks designed to perform specific functions such as fetching data or creating backups. Each job is configured with a schedule and operates within defined parameters.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: A job scheduler that runs tasks at fixed intervals, defined in milliseconds.

## How It Works

1. Each job is configured with a specific purpose and schedule.
2. Jobs are executed automatically based on their defined schedule.
3. The system ensures that jobs run only when enabled and adhere to their specified timing.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the start of every hour from 7:00 AM to 5:00 PM PST.
  - **Cron Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles

### 🌙 calendar-fetch-midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM PST.
  - **Cron Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles

### 💾 config-backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. A commit is made only if changes are detected.
- **Schedule**: Runs every 24 hours.
  - **Interval**: 86,400,000 milliseconds (24 hours)
