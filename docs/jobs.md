---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their schedules. These jobs automate recurring tasks, ensuring consistent execution of critical operations such as data fetching, backups, and system health checks.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: Jobs that run at fixed intervals, specified in milliseconds.
- **Time Zone Awareness**: All schedules are aligned to the `America/Los_Angeles` time zone unless otherwise noted.

## How It Works

Each job is configured with a schedule and a specific purpose. Jobs are executed automatically based on their defined schedule. Cron-based jobs use cron expressions to specify exact times and days for execution, while interval-based jobs run at regular intervals.

## Scheduled Jobs

### 🕒 Calendar Fetch (Hourly)

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron-based, every hour from 7:00 AM to 5:00 PM PST (`0 7-17 * * *`).

---

### 🗂️ Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Interval-based, every 24 hours (86,400,000 milliseconds).

---

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, daily at 12:00 AM PST (`0 0 * * *`).

---

### 🌅 Evening Briefing

- **Description**: Weekday 9 PM briefing summarizing tasks for the following morning.
- **Schedule**: Cron-based, Monday through Friday at 9:00 PM PST (`0 22 * * 0-4`).

---

### 📈 Portfolio Closing Briefing

- **Description**: *(No description provided)*.
- **Schedule**: Cron-based, Monday through Friday at 9:00 PM PST (`0 21 * * 1-5`).

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: *(No description provided)*.
- **Schedule**: Cron-based, Friday and Saturday at 10:00 PM PST (`0 22 * * 5,6`).

---

### 📦 Daily Package Delivery Check

- **Description**: *(No description provided)*.
- **Schedule**: Cron-based, daily at 8:00 AM PST (`0 8 * * *`).

---

### ✅ Daily Health Check

- **Description**: Verifies email sending functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, daily at 9:00 AM PST (`0 9 * * *`).
