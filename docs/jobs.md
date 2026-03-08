---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. These jobs are designed to automate recurring tasks such as fetching calendar data and backing up configuration files. Each job runs on a predefined schedule to ensure timely and consistent execution.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specified intervals or times.
- **Cron Schedule**: A time-based job scheduler used for running jobs at specific times or intervals.
- **Time Zones**: Jobs may be configured to run in specific time zones.
- **Conditional Execution**: Some jobs only perform actions if certain conditions are met (e.g., changes detected).

## How It Works

1. Each job is defined with a unique name, description, and schedule.
2. Jobs are enabled or disabled based on configuration.
3. Jobs execute automatically according to their defined schedule, either using a cron expression or a fixed interval in milliseconds.
4. Some jobs include conditional logic to determine whether an action is necessary (e.g., only committing changes if they exist).

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based schedule, runs at the top of every hour from 7:00 AM to 5:00 PM PST.
  - Cron Expression: `0 7-17 * * *`
  - Time Zone: America/Los_Angeles

### 🌙 calendar-fetch-midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based schedule, runs daily at 12:00 AM PST.
  - Cron Expression: `0 0 * * *`
  - Time Zone: America/Los_Angeles

### 💾 config-backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. The job only commits changes if the file has been modified.
- **Schedule**: Runs every 24 hours.
  - Interval: 86,400,000 milliseconds (24 hours)
