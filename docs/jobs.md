---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Scheduled Jobs

## Overview

This document provides an overview of scheduled jobs, their purposes, and execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using either a cron expression or a time interval.
- **Time Zone**: Specifies the time zone for the job's schedule.

## Scheduled Jobs

### 🕒 Calendar Fetch (Hourly)

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM).
- **Time Zone**: America/Los_Angeles.

### 💾 Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Every 24 hours (86,400,000 milliseconds).

### 📅 Evening Briefing

- **Description**: Weekday 9 PM briefing to outline tasks for the following morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (9 PM, Monday to Friday).
- **Time Zone**: America/Los_Angeles.

### 🕘 Portfolio Closing Briefing

- **Description**: *No description provided.*
- **Schedule**: Cron expression `0 21 * * 1-5` (9 PM, Monday to Friday).
- **Time Zone**: America/Los_Angeles.

### ⏰ Evening Alarm Reminder

- **Description**: Nightly 10:30 PM reminder for Jeff to check the alarm if there is an early morning work meeting.
- **Schedule**: Cron expression `30 22 * * *` (10:30 PM daily).
- **Time Zone**: America/Los_Angeles.

### 📦 Daily Package Delivery Check

- **Description**: *No description provided.*
- **Schedule**: Cron expression `0 8 * * *` (8 AM daily).
- **Time Zone**: America/Los_Angeles.

### 🩺 Daily Health Check

- **Description**: Verifies email sending functionality daily and sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (9 AM daily).
- **Time Zone**: America/Los_Angeles.

### 🕔 WW Daily Points Check-in

- **Description**: *No description provided.*
- **Schedule**: Cron expression `30 17 * * *` (5:30 PM daily).
- **Time Zone**: America/Los_Angeles.

### ⚠️ Late-Early Conflict Morning Check

- **Description**: Flags if there is a late meeting (after 6 PM) today and an early meeting (before 9 AM) tomorrow. Runs daily at 10 AM.
- **Schedule**: Cron expression `0 10 * * *` (10 AM daily).
- **Time Zone**: America/Los_Angeles.

### 🦞 Lobster Changelog Weekly Scan

- **Description**: Weekly scan of `lobster.shahine.com/changelog` for new ideas.
- **Schedule**: Cron expression `0 9 * * 1` (9 AM every Monday).
- **Time Zone**: America/Los_Angeles.

### 🌙 Calendar Fetch (Midnight)

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (12 AM daily).
- **Time Zone**: America/Los_Angeles.
