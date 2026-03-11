---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides information about scheduled jobs within the system. Scheduled jobs automate recurring tasks such as data fetching and backups, ensuring consistent operation and reducing manual intervention.

## Key Concepts

- **Scheduled Jobs**: Predefined tasks executed automatically based on a schedule.
- **Cron Expressions**: Used to define specific execution times for jobs.
- **Time Zones**: Jobs may operate in specific time zones.
- **Enabled Status**: Indicates whether a job is active.

## How It Works

Scheduled jobs are configured with specific schedules and descriptions. Jobs can be enabled or disabled, and their execution times are defined using either cron expressions or interval-based schedules. Time zones are specified for jobs requiring localized execution times.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

- **Description**: Fetch calendars hourly between 7am and 5pm PST.
- **Schedule**: Cron expression `0 7-17 * * *` in the time zone `America/Los_Angeles`.
- **Enabled**: Yes

### 🗂️ Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Executes every 24 hours (`86400000ms` interval).
- **Enabled**: Yes

### 🌙 Calendar Fetch Midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` in the time zone `America/Los_Angeles`.
- **Enabled**: Yes
