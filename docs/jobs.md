---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs available in the system. These jobs are automated tasks designed to perform specific operations at predefined intervals, ensuring the system remains up-to-date and operational. Each job has a defined schedule and purpose, which are detailed below.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific intervals or times.
- **Cron Schedule**: A time-based job scheduler used to execute tasks at specific times or intervals.
- **Time Zones**: Some jobs are scheduled based on a specific time zone.
- **Enabled Jobs**: Only jobs marked as enabled are active and executed.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Runs every hour on the hour from 7:00 AM to 5:00 PM (PST).
  - **Type**: Cron
  - **Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles

### 🌙 calendar-fetch-midnight

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Runs daily at 12:00 AM (PST).
  - **Type**: Cron
  - **Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles

### 💾 config-backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. A commit is only made if changes are detected.
- **Schedule**: Runs every 24 hours.
  - **Type**: Interval
  - **Interval**: 86,400,000 milliseconds (24 hours)
