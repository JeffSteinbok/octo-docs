---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate various tasks, such as fetching data, sending reminders, and performing system health checks, to ensure efficient and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Specifies when and how often the job runs, using either cron expressions or interval-based scheduling.
- **Time Zone**: All schedules are specified in the `America/Los_Angeles` time zone unless otherwise noted.

## Scheduled Jobs

### 📅 Calendar Fetch Hourly

- **Description**: Fetch calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7:00 AM to 5:00 PM).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at 12:00 AM).

---

### 🗂️ Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Every 24 hours (interval-based).

---

### 🌅 Evening Briefing

- **Description**: Weekday 9:00 PM briefing to summarize tasks for the next morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9:00 PM).

---

### 🌇 Portfolio Closing Briefing

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9:00 PM).

---

### ⏰ Evening Alarm Reminder

- **Description**: Nightly 10:30 PM reminder for Jeff to check the alarm if there is an early morning work meeting.
- **Schedule**: Cron expression `30 22 * * *` (daily at 10:30 PM).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 8 * * *` (daily at 8:00 AM).

---

### ✅ Daily Health Check

- **Description**: Verifies email sending functionality and sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9:00 AM).

---

### 🕒 WW Daily Points Check-in

- **Description**: (No description provided).
- **Schedule**: Cron expression `30 17 * * *` (daily at 5:30 PM).

---

### ⚠️ Late-Early Conflict Morning Check

- **Description**: Flags conflicts if today's schedule includes a late meeting (after 6:00 PM) and tomorrow's schedule includes an early meeting (before 9:00 AM).
- **Schedule**: Cron expression `0 10 * * *` (daily at 10:00 AM).

---

### 📜 Lobster Changelog Weekly Scan

- **Description**: Weekly Monday scan of `lobster.shahine.com/changelog` for new ideas.
- **Schedule**: Cron expression `0 9 * * 1` (Mondays at 9:00 AM).
