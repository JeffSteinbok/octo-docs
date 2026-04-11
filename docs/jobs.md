---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page provides an overview of scheduled jobs that automate various tasks such as calendar fetching, health checks, reminders, and data backups. These jobs help streamline daily operations by running at specified times and intervals, ensuring timely notifications and maintenance.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Scheduling**: Many jobs use cron expressions to define their execution schedule.
- **Time Zone Awareness**: Schedules are set in the America/Los_Angeles time zone unless otherwise specified.
- **Job Enablement**: Only enabled jobs are active and will execute as scheduled.

## How It Works

1. Each job is defined with a name, description, and schedule.
2. Jobs are scheduled using either cron expressions or interval-based triggers.
3. Enabled jobs execute automatically according to their defined schedule.
4. Some jobs provide notifications or perform checks, while others fetch data or back up configurations.

---

## 🗓️ calendar-fetch-hourly

**Description:** Fetch calendars hourly 7am-5pm PST  
**Schedule:** Every hour at the top of the hour, from 7:00 AM to 5:00 PM (America/Los_Angeles)

---

## 💾 config-backup

**Description:** Backup openclaw.json to Git daily (only commits if changed)  
**Schedule:** Every 24 hours

---

## 📰 evening-briefing

**Description:** Weekday 9 PM briefing: what's on tap tomorrow morning  
**Schedule:** 9:00 PM, Monday to Friday (America/Los_Angeles)

---

## 📈 portfolio-closing-briefing

**Description:**  
**Schedule:** 9:00 PM, Monday to Friday (America/Los_Angeles)

---

## ⏰ evening-alarm-reminder

**Description:** Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting  
**Schedule:** 10:30 PM daily (America/Los_Angeles)

---

## 📦 Daily package delivery check

**Description:**  
**Schedule:** 8:00 AM daily (America/Los_Angeles)

---

## 🩺 daily-health-check

**Description:** Daily health check — verifies email sending works; DMs Jeff if anything fails  
**Schedule:** 9:00 AM daily (America/Los_Angeles)

---

## 🍽️ Remind Jeff to reach out to Zack Ali for dinner

**Description:** One-shot reminder to schedule another dinner with Zack Ali  
**Schedule:** One-time (disabled)

---

## 🏅 WW Daily Points Check-in

**Description:**  
**Schedule:** 5:30 PM daily (America/Los_Angeles)

---

## ⚠️ late-early-conflict-morning-check

**Description:** 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)  
**Schedule:** 10:00 AM daily (America/Los_Angeles)

---

## 🦞 Lobster changelog weekly scan

**Description:** Weekly Monday scan of lobster.shahine.com/changelog for new ideas  
**Schedule:** 9:00 AM every Monday (America/Los_Angeles)

---

## 🌙 calendar-fetch-midnight

**Description:** Fetch calendars at midnight PST  
**Schedule:** 12:00 AM daily (America/Los_Angeles)

---

## 🥗 ww-diet-sync

**Description:**  
**Schedule:** 4:00 AM daily (America/Los_Angeles)
