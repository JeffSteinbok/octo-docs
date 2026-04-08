---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs perform various automated tasks, such as fetching data, sending reminders, and performing system checks, to ensure smooth operations and timely notifications.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Specifies when and how often the job runs, using either cron expressions or interval-based timing.
- **Time Zone**: All cron-based schedules are configured in the `America/Los_Angeles` time zone unless otherwise specified.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

- **Description**: Fetch calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs every hour from 7:00 AM to 5:00 PM PST (`0 7-17 * * *`).

### 🗂️ Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours.

### 🌙 Calendar Fetch Midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM PST (`0 0 * * *`).

### 📋 Evening Briefing

- **Description**: Weekday 9:00 PM briefing summarizing tasks for the next morning.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM PST (`0 22 * * 0-4`).

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided).
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM PST (`0 21 * * 1-5`).

### ⏰ Evening Alarm Reminder

- **Description**: Nightly 10:30 PM reminder for Jeff to check the alarm if there’s an early morning work meeting.
- **Schedule**: Cron-based, runs daily at 10:30 PM PST (`30 22 * * *`).

### 📦 Daily Package Delivery Check

- **Description**: (No description provided).
- **Schedule**: Cron-based, runs daily at 8:00 AM PST (`0 8 * * *`).

### ✅ Daily Health Check

- **Description**: Verifies email sending functionality daily. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9:00 AM PST (`0 9 * * *`).

### 🕵️ Late-Early Conflict Morning Check

- **Description**: Flags if there’s a late meeting (after 6:00 PM) today and an early meeting (before 9:00 AM) tomorrow.
- **Schedule**: Cron-based, runs daily at 10:00 AM PST (`0 10 * * *`).

### 🦞 Lobster Changelog Weekly Scan

- **Description**: Weekly scan of `lobster.shahine.com/changelog` for new ideas.
- **Schedule**: Cron-based, runs every Monday at 9:00 AM PST (`0 9 * * 1`).

### 🏋️ WW Daily Points Check-in

- **Description**: (No description provided).
- **Schedule**: Cron-based, runs daily at 5:30 PM PST (`30 17 * * *`).
