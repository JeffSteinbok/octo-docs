---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Each job is designed to automate specific tasks, such as fetching data, performing backups, or sending reminders, at predefined intervals. The schedules are configured using cron expressions or interval-based timing to ensure timely execution.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing configuration for when the job runs, defined using cron expressions or interval-based schedules.
- **Time Zone**: All cron-based schedules are configured in the `America/Los_Angeles` time zone unless otherwise specified.
- **Enabled Status**: Only enabled jobs are active and executed as per their schedule.

## How It Works

1. Each job is defined with a name, description, and schedule.
2. Jobs are executed automatically based on their configured schedule.
3. Cron-based jobs use standard cron expressions to specify execution times, while interval-based jobs use a millisecond interval.
4. Disabled jobs are not executed, even if their schedule is defined.

## Scheduled Jobs

### 📅 Calendar Fetch Hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based (`0 7-17 * * *`, time zone: `America/Los_Angeles`).

---

### 🗂️ Config Backup

- **Description**: Backs up `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours (interval-based).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based (`0 0 * * *`, time zone: `America/Los_Angeles`).

---

### 🌅 Evening Briefing

- **Description**: Sends a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based (`0 22 * * 0-4`, time zone: `America/Los_Angeles`).

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided)
- **Schedule**: Cron-based (`0 21 * * 1-5`, time zone: `America/Los_Angeles`).

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: (No description provided)
- **Schedule**: Cron-based (`0 22 * * 5,6`, time zone: `America/Los_Angeles`).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided)
- **Schedule**: Cron-based (`0 8 * * *`, time zone: `America/Los_Angeles`).

---

### ✅ Daily Health Check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based (`0 9 * * *`, time zone: `America/Los_Angeles`).

---

### 🕔 WW Daily Points Check-in

- **Description**: (No description provided)
- **Schedule**: Cron-based (`30 17 * * *`, time zone: `America/Los_Angeles`).
