---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: Specifies the exact times and days a job should run.
- **Interval Schedule**: Specifies the frequency in milliseconds between job executions.
- **Time Zone Awareness**: All schedules are configured in the `America/Los_Angeles` time zone.

## How It Works

Scheduled jobs are configured to run automatically based on their defined schedules. Jobs can use either a cron expression or an interval-based schedule. Each job performs a specific task, such as fetching data, creating backups, or sending notifications. Enabled jobs execute as per their schedule without manual intervention.

## Scheduled Jobs

### 📅 Calendar Fetch (Hourly)

- **Description**: Fetches calendar data hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron-based, runs at the top of every hour from 7 AM to 5 PM (`0 7-17 * * *` in `America/Los_Angeles` time zone).

---

### 🗂️ Config Backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits are made only if changes are detected.
- **Schedule**: Interval-based, runs every 24 hours (86400000 milliseconds).

---

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron-based, runs at midnight (`0 0 * * *` in `America/Los_Angeles` time zone).

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based, runs at 9 PM from Sunday to Thursday (`0 22 * * 0-4` in `America/Los_Angeles` time zone).

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided in source material).
- **Schedule**: Cron-based, runs at 9 PM on weekdays (`0 21 * * 1-5` in `America/Los_Angeles` time zone).

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: (No description provided in source material).
- **Schedule**: Cron-based, runs at 10 PM on Fridays and Saturdays (`0 22 * * 5,6` in `America/Los_Angeles` time zone).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided in source material).
- **Schedule**: Cron-based, runs daily at 8 AM (`0 8 * * *` in `America/Los_Angeles` time zone).

---

### 🩺 Daily Health Check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9 AM (`0 9 * * *` in `America/Los_Angeles` time zone).
