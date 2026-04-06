---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Each job is designed to perform a specific task at a predefined schedule, ensuring the system operates efficiently and reliably. The schedules are defined using cron expressions or time intervals, and all times are specified in the Pacific Time Zone (PST).

## Key Concepts

- **Scheduled Jobs**: Tasks that run automatically based on a predefined schedule.
- **Cron Expressions**: A time-based job scheduler format used to define when a job should run.
- **Time Zones**: All schedules are configured in the `America/Los_Angeles` time zone (PST).
- **Enabled Jobs**: Only jobs marked as `enabled` are active and executed.

## How It Works

1. Each job is configured with a name, description, and schedule.
2. The schedule determines when the job will execute, either using a cron expression or a fixed time interval.
3. Enabled jobs run automatically at their scheduled times.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7:00 AM to 5:00 PM PST).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at 12:00 AM PST).

---

### 📦 Config Backup

- **Description**: Backs up `openclaw.json` to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Every 24 hours (86,400,000 milliseconds).

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9:00 PM briefing about the tasks scheduled for the next morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday to Thursday at 9:00 PM PST).

---

### 🌇 Portfolio Closing Briefing

- **Description**: *No description provided.*
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday to Friday at 9:00 PM PST).

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: *No description provided.*
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10:00 PM PST).

---

### 📦 Daily Package Delivery Check

- **Description**: *No description provided.*
- **Schedule**: Cron expression `0 8 * * *` (daily at 8:00 AM PST).

---

### ✅ Daily Health Check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9:00 AM PST).
