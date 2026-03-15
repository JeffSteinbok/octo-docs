---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purpose, and their execution schedules. These jobs automate recurring tasks such as calendar fetching, data backups, and daily briefings, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Expressions**: Used to define specific schedules for jobs.
- **Time Zones**: Jobs may operate in specific time zones, such as PST.

## How It Works

Scheduled jobs are configured with specific execution times or intervals. Each job has a defined purpose and runs automatically based on its schedule. Jobs can use either cron expressions or interval-based scheduling.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.

---

### 🗂️ Config Backup

- **Description**: Backup `openclaw.json` daily to Git, committing only if changes are detected.
- **Schedule**: Runs every 24 hours (`86400000 ms`).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.

---

### 🌅 Evening Briefing

- **Description**: Weekday 9 PM briefing summarizing the next morning's agenda.
- **Schedule**: Cron expression `0 21 * * 0-4` in the `America/Los_Angeles` time zone.

---

### 📈 Portfolio Closing Briefing

- **Description**: No description provided.
- **Schedule**: Cron expression `0 21 * * *` in the `America/Los_Angeles` time zone.

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: No description provided.
- **Schedule**: Cron expression `0 22 * * 5,6` in the `America/Los_Angeles` time zone.

---

### 📦 Daily Package Delivery Check

- **Description**: No description provided.
- **Schedule**: Cron expression `0 8 * * *` in the `America/Los_Angeles` time zone.
