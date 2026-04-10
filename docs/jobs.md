---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page provides an overview of scheduled jobs that automate recurring tasks. These jobs help streamline operations by performing actions such as calendar fetching, health checks, reminders, and backups at defined intervals. Each job is configured with a specific schedule and purpose to ensure timely execution and reliability.

## Key Concepts

- **Scheduled Jobs**: Automated tasks executed at specified times or intervals.
- **Cron Scheduling**: Jobs scheduled using cron expressions for flexible timing.
- **Enabled/Disabled Status**: Indicates whether a job is active.
- **Time Zone Awareness**: Schedules are set with respect to the America/Los_Angeles time zone when applicable.

## How It Works

1. Each job is defined with a name, description, enabled status, and schedule.
2. Jobs use either cron expressions, fixed intervals, or one-shot scheduling.
3. Enabled jobs run automatically based on their schedule.
4. Some jobs perform checks, send reminders, or fetch data as described.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST.
- **Schedule**: Every hour from 7:00 AM to 5:00 PM (America/Los_Angeles).

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed).
- **Schedule**: Every 24 hours.

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning.
- **Schedule**: 9:00 PM, Monday to Friday (America/Los_Angeles).

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*
- **Schedule**: 9:00 PM, Monday to Friday (America/Los_Angeles).

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting.
- **Schedule**: 10:30 PM daily (America/Los_Angeles).

### 📦 Daily package delivery check

- **Description**: *(No description provided)*
- **Schedule**: 8:00 AM daily (America/Los_Angeles).

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails.
- **Schedule**: 9:00 AM daily (America/Los_Angeles).

### 🥘 Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali.
- **Schedule**: One-time (disabled).

### 🏅 WW Daily Points Check-in

- **Description**: *(No description provided)*
- **Schedule**: 5:30 PM daily (America/Los_Angeles).

### ⚠️ late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM).
- **Schedule**: 10:00 AM daily (America/Los_Angeles).

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas.
- **Schedule**: 9:00 AM every Monday (America/Los_Angeles).

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: 12:00 AM daily (America/Los_Angeles).

### 🍏 ww-diet-sync

- **Description**: *(No description provided)*
- **Schedule**: 4:00 AM daily (America/Los_Angeles).
