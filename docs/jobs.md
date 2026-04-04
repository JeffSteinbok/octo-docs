---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Scheduled Jobs

## Overview

This document provides an overview of the scheduled jobs available in the system. These jobs are automated tasks designed to perform recurring operations such as data fetching, backups, and notifications. Each job is configured with a specific schedule and purpose to ensure timely and efficient execution.

## Key Concepts

- **Job Name**: A unique identifier for the scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency of the job's execution, defined using cron expressions or time intervals.
- **Time Zone**: The time zone in which the job's schedule is defined.

## Scheduled Jobs

### 📅 Calendar Fetch (Hourly)

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7:00 AM to 5:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### 📂 Config Backup

- **Description**: Backs up the `openclaw.json` configuration file daily. Commits changes only if the file has been modified.
- **Schedule**: Every 24 hours (86,400,000 milliseconds).

---

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at 12:00 AM).
- **Time Zone**: America/Los_Angeles.

---

### 🌅 Evening Briefing

- **Description**: Sends a weekday 9:00 PM briefing summarizing tasks scheduled for the following morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### 📈 Portfolio Closing Briefing

- **Description**: No description provided.
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: No description provided.
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### 📦 Daily Package Delivery Check

- **Description**: No description provided.
- **Schedule**: Cron expression `0 8 * * *` (daily at 8:00 AM).
- **Time Zone**: America/Los_Angeles.

---

### 🩺 Daily Health Check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9:00 AM).
- **Time Zone**: America/Los_Angeles.
