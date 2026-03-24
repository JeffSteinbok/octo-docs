---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and execution schedules. These jobs automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using either cron expressions or interval-based timing.
- **Time Zone**: All schedules are aligned to the `America/Los_Angeles` time zone.

## How It Works

Scheduled jobs are configured to run automatically based on predefined schedules. Each job has a specific purpose, such as fetching data, performing backups, or sending notifications. The schedule is defined using either:
- **Cron expressions**: Specify exact times and days for execution.
- **Interval-based timing**: Specify execution intervals in milliseconds.

## Scheduled Jobs

### 📅 Calendar Fetch (Hourly)

- **Description**: Fetches calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM, inclusive).

### 🗂️ Config Backup

- **Description**: Backs up `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours (interval-based).

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at midnight).

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9 PM briefing about the next morning's schedule.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9 PM).

### 📈 Portfolio Closing Briefing

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9 PM).

### ⏰ Weekend Morning Alarm Reminder

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10 PM).

### 📦 Daily Package Delivery Check

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).

### ✅ Daily Health Check

- **Description**: Verifies email sending functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9 AM).
