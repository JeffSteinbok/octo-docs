---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate recurring tasks, ensuring timely and consistent operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks executed at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: Jobs scheduled to run at fixed intervals, defined in milliseconds.
- **Time Zone**: All schedules are specified in the `America/Los_Angeles` time zone.

## How It Works

Scheduled jobs are configured to run automatically based on their defined schedules. Jobs can be triggered using either a cron expression or a fixed interval. Each job has a specific purpose, such as fetching data, creating backups, or sending reminders. The system ensures that these tasks are executed reliably and on time.

## Scheduled Jobs

### 📅 Calendar Fetch Hourly

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the top of every hour from 7:00 AM to 5:00 PM (`0 7-17 * * *`).

---

### 🗂️ Config Backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours (86400000 milliseconds).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM (`0 0 * * *`).

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM (`0 21 * * 0-4`).

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM (`0 21 * * 1-5`).

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs Friday and Saturday at 10:00 PM (`0 22 * * 5,6`).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs daily at 8:00 AM (`0 8 * * *`).
