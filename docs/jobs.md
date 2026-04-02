---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Scheduled Jobs

Automated tasks that run on cron schedules or fixed intervals. All times are in **America/Los_Angeles** unless noted.

### 🕖 Calendar Fetch Hourly

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the start of every hour from 7:00 AM to 5:00 PM (`0 7-17 * * *`).

---

### 🕛 Calendar Fetch Midnight

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM (`0 0 * * *`).

---

### 🗂️ Config Backup

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Interval-based, runs every 24 hours (86,400,000 milliseconds).

---

### 🌅 Evening Briefing

- **Description**: Sends a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM (`0 22 * * 0-4`).

---

### 📈 Portfolio Closing Briefing

- **Description**: End-of-day portfolio summary after market close.

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: Reminds about weekend morning alarm settings on Friday and Saturday nights.

---

### 📦 Daily Package Delivery Check

- **Description**: Checks status of all tracked packages and notifies about expected deliveries.

---

### ✅ Daily Health Check

- **Description**: Verifies email sending functionality and notifies Jeff via direct message if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9:00 AM (`0 9 * * *`).
