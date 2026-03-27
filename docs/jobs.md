---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Each job is designed to perform a specific task at a predefined schedule, ensuring the system operates efficiently and critical processes are executed on time.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: A job scheduler that runs tasks at fixed intervals, defined in milliseconds.
- **Time Zones**: All schedules are configured in the `America/Los_Angeles` time zone unless otherwise specified.

## How It Works

1. Each job is defined with a name, description, and schedule.
2. Jobs are enabled by default and execute based on their configured schedule.
3. Schedules can be defined using either cron expressions or fixed intervals.
4. Jobs perform specific tasks, such as fetching data, creating backups, or sending notifications.

## Scheduled Jobs

### 📅 Calendar Fetch (Hourly)

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs every hour from 7:00 AM to 5:00 PM PST (`0 7-17 * * *`).

---

### 🗂️ Config Backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Interval-based, runs every 24 hours (86,400,000 milliseconds).

---

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM PST (`0 0 * * *`).

---

### 🌅 Evening Briefing

- **Description**: Sends a weekday 9:00 PM briefing about the next morning's agenda.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM PST (`0 22 * * 0-4`).

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM PST (`0 21 * * 1-5`).

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs Friday and Saturday at 10:00 PM PST (`0 22 * * 5,6`).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs daily at 8:00 AM PST (`0 8 * * *`).

---

### ✅ Daily Health Check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9:00 AM PST (`0 9 * * *`).
