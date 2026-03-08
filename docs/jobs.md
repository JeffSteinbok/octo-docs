---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. These jobs automate recurring tasks such as fetching calendar data and backing up configuration files, ensuring that critical processes are performed consistently and on schedule.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: A job scheduler that runs tasks at fixed intervals, defined in milliseconds.
- **Time Zone Awareness**: Some jobs are configured to run in a specific time zone.

## Scheduled Jobs

### 🗓️ Calendar Fetch (Hourly)

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based schedule, running at the start of every hour from 7:00 AM to 5:00 PM PST.
  - **Cron Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles

### 🗂️ Config Backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. A commit is only made if the file has changed.
- **Schedule**: Runs every 24 hours.
  - **Interval**: 86,400,000 milliseconds (24 hours)

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron-based schedule, running at midnight every day.
  - **Cron Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles

## How It Works

1. **Job Scheduling**: Each job is configured with a specific schedule, either using a cron expression or a fixed interval in milliseconds.
2. **Execution**: The system triggers the job based on its defined schedule. For cron-based jobs, the execution is aligned with the specified time zone.
3. **Task Completion**: The job performs its designated task, such as fetching calendar data or backing up configuration files.
4. **Post-Execution**: For jobs like the configuration backup, additional logic ensures that actions (e.g., Git commits) are only performed if necessary.
