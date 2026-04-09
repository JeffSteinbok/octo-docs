---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and execution schedules. These jobs automate various tasks, ensuring timely and consistent operations.

## Key Concepts

- **Job Name**: The identifier for the scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency of the job's execution, defined using cron expressions or interval-based scheduling.
- **Time Zone**: All schedules are specified in the `America/Los_Angeles` time zone unless otherwise noted.

## Scheduled Jobs

### 🗓️ Calendar Fetch (Hourly)

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7:00 AM to 5:00 PM).

---

### 📁 Config Backup

- **Description**: Backs up `openclaw.json` to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Every 24 hours (86,400,000 milliseconds).

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron expression `0 22 * * 0-4` (Monday to Friday at 9:00 PM PST).

---

### 📊 Portfolio Closing Briefing

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday to Friday at 9:00 PM PST).

---

### ⏰ Evening Alarm Reminder

- **Description**: Sends a nightly reminder at 10:30 PM to check the alarm if there is an early morning work meeting.
- **Schedule**: Cron expression `30 22 * * *` (daily at 10:30 PM PST).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 8 * * *` (daily at 8:00 AM PST).

---

### 🩺 Daily Health Check

- **Description**: Verifies email sending functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9:00 AM PST).

---

### 🕵️ Late-Early Conflict Morning Check

- **Description**: Flags conflicts where today has a late meeting (after 6:00 PM) and tomorrow has an early meeting (before 9:00 AM).
- **Schedule**: Cron expression `0 10 * * *` (daily at 10:00 AM PST).

---

### 🦞 Lobster Changelog Weekly Scan

- **Description**: Scans the Lobster changelog every Monday for new ideas.
- **Schedule**: Cron expression `0 9 * * 1` (weekly on Mondays at 9:00 AM PST).

---

### 🕛 Calendar Fetch (Midnight)

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at 12:00 AM PST).

---

### 🏆 WW Daily Points Check-in

- **Description**: (No description provided).
- **Schedule**: Cron expression `30 17 * * *` (daily at 5:30 PM PST).
