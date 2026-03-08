---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Each job is designed to perform a specific task on a defined schedule, ensuring consistent and automated operations.

## Key Concepts

- **Scheduled Jobs**: Tasks that run automatically based on a predefined schedule.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: A schedule that runs jobs at fixed intervals, defined in milliseconds.
- **Time Zones**: Some jobs are configured to run in a specific time zone.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the top of every hour between 7:00 AM and 5:00 PM PST (`0 7-17 * * *`).
- **Time Zone**: America/Los_Angeles.

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at midnight PST (`0 0 * * *`).
- **Time Zone**: America/Los_Angeles.

### 💾 Config Backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits are only made if changes are detected.
- **Schedule**: Runs every 24 hours (86400000 milliseconds).
