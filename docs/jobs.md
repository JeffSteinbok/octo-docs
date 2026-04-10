---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate various tasks, such as data fetching, backups, reminders, and health checks, to ensure smooth operations and timely notifications.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Specifies when and how often the job runs, using either a cron expression or a time interval.
- **Time Zone**: All schedules are defined in the `America/Los_Angeles` time zone unless otherwise noted.
- **Enabled Status**: Only enabled jobs are actively running.

## Scheduled Jobs

### 📅 Calendar Fetch Hourly

- **Description**: Fetches calendar data hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM).

---

### 🗂️ Config Backup

- **Description**: Backs up `openclaw.json` to Git daily, committing only if changes are detected.
- **Schedule**: Every 24 hours (86400000 milliseconds).

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9 PM briefing about the next morning's schedule.
- **Schedule**: Cron expression `0 22 * * 0-4` (Monday to Friday at 9 PM).

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday to Friday at 9 PM).

---

### ⏰ Evening Alarm Reminder

- **Description**: Sends a nightly reminder at 10:30 PM for Jeff to check the alarm if there’s an early morning meeting.
- **Schedule**: Cron expression `30 22 * * *` (daily at 10:30 PM).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).

---

### 🩺 Daily Health Check

- **Description**: Verifies email sending functionality and notifies Jeff via DM if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9 AM).

---

### 📝 WW Daily Points Check-in

- **Description**: (No description provided).
- **Schedule**: Cron expression `30 17 * * *` (daily at 5:30 PM).

---

### ⚠️ Late-Early Conflict Morning Check

- **Description**: Flags if there’s a late meeting (after 6 PM) today and an early meeting (before 9 AM) tomorrow.
- **Schedule**: Cron expression `0 10 * * *` (daily at 10 AM).

---

### 🦞 Lobster Changelog Weekly Scan

- **Description**: Scans the Lobster changelog for new ideas every Monday.
- **Schedule**: Cron expression `0 9 * * 1` (weekly on Mondays at 9 AM).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at midnight).

---

### 🍽️ WW Diet Sync

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 4 * * *` (daily at 4 AM).
