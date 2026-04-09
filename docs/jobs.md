---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using either cron expressions or interval-based timing.
- **Time Zone**: Specifies the time zone for scheduled jobs.

## Scheduled Jobs

### 📅 Calendar Fetch Hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM, PST).

---

### 💾 Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Every 24 hours.

---

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9 PM briefing about the next morning's schedule.
- **Schedule**: Cron expression `0 22 * * 0-4` (9 PM, Monday to Friday, PST).

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided)
- **Schedule**: Cron expression `0 21 * * 1-5` (9 PM, Monday to Friday, PST).

---

### ⏰ Evening Alarm Reminder

- **Description**: Nightly 10:30 PM reminder for Jeff to check the alarm if there is an early morning meeting.
- **Schedule**: Cron expression `30 22 * * *` (10:30 PM, PST).

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided)
- **Schedule**: Cron expression `0 8 * * *` (8 AM, PST).

---

### 🩺 Daily Health Check

- **Description**: Verifies email sending functionality daily and sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (9 AM, PST).

---

### 🦞 Lobster Changelog Weekly Scan

- **Description**: Weekly Monday scan of `lobster.shahine.com/changelog` for new ideas.
- **Schedule**: Cron expression `0 9 * * 1` (9 AM, Monday, PST).

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (12 AM, PST).

---

### ⚖️ Late-Early Conflict Morning Check

- **Description**: Daily 10 AM check to flag if there is a late meeting (after 6 PM) today and an early meeting (before 9 AM) tomorrow.
- **Schedule**: Cron expression `0 10 * * *` (10 AM, PST).

---

### 📊 WW Daily Points Check-in

- **Description**: (No description provided)
- **Schedule**: Cron expression `30 17 * * *` (5:30 PM, PST).

---

### 🥗 WW Diet Sync Progress

- **Description**: (No description provided)
- **Schedule**: Every 90 seconds.

---

### 🥗 WW Diet Sync

- **Description**: (No description provided)
- **Schedule**: Cron expression `0 4 * * *` (4 AM, PST).
