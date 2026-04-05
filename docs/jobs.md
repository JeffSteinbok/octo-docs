---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: Specifies the exact times a job should run using cron expressions.
- **Interval Schedule**: Specifies the frequency of job execution in milliseconds.

## How It Works

Each job is configured with a specific schedule and runs automatically based on its defined timing. The schedules are either cron-based, allowing precise timing, or interval-based, specifying a fixed duration between executions. Jobs are designed to perform specific tasks, such as fetching data, sending notifications, or performing system checks.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs every hour from 7:00 AM to 5:00 PM PST (`0 7-17 * * *`).

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Interval-based, runs every 24 hours (86,400,000 milliseconds).

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM PST (`0 0 * * *`).

### 🌅 evening-briefing

- **Description**: Provides a weekday 9:00 PM briefing on tasks scheduled for the next morning.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM PST (`0 22 * * 0-4`).

### 📊 portfolio-closing-briefing

- **Description**: No description provided.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM PST (`0 21 * * 1-5`).

### ⏰ weekend-morning-alarm-reminder

- **Description**: No description provided.
- **Schedule**: Cron-based, runs on Fridays and Saturdays at 10:00 PM PST (`0 22 * * 5,6`).

### 📦 Daily package delivery check

- **Description**: No description provided.
- **Schedule**: Cron-based, runs daily at 8:00 AM PST (`0 8 * * *`).

### ✅ daily-health-check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9:00 AM PST (`0 9 * * *`).
