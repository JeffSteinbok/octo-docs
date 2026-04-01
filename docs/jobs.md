---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. These jobs are automated tasks designed to perform specific functions at predefined intervals, ensuring the system operates efficiently and reliably. Each job includes a description, its purpose, and scheduling details.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specified intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: Jobs that run at fixed time intervals, specified in milliseconds.
- **Time Zone Awareness**: All schedules are configured with a specific time zone to ensure consistent execution.

## Scheduled Jobs

### 🗓️ Calendar Fetch Hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the top of every hour (`0 7-17 * * *`).
- **Time Zone**: America/Los_Angeles.

---

### 🗂️ Config Backup

- **Description**: Backs up the `openclaw.json` configuration file daily. Commits changes only if modifications are detected.
- **Schedule**: Runs every 24 hours (86400000 milliseconds).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based, runs at midnight (`0 0 * * *`).
- **Time Zone**: America/Los_Angeles.

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9:00 PM briefing about tasks scheduled for the following morning.
- **Schedule**: Cron-based, runs at 10:00 PM Sunday through Thursday (`0 22 * * 0-4`).
- **Time Zone**: America/Los_Angeles.

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided in source material.)
- **Schedule**: Cron-based, runs at 9:00 PM Monday through Friday (`0 21 * * 1-5`).
- **Time Zone**: America/Los_Angeles.

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: (No description provided in source material.)
- **Schedule**: Cron-based, runs at 10:00 PM on Fridays and Saturdays (`0 22 * * 5,6`).
- **Time Zone**: America/Los_Angeles.

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided in source material.)
- **Schedule**: Cron-based, runs at 8:00 AM daily (`0 8 * * *`).
- **Time Zone**: America/Los_Angeles.

---

### ✅ Daily Health Check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs at 9:00 AM daily (`0 9 * * *`).
- **Time Zone**: America/Los_Angeles.
