---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Scheduled Jobs

These scheduled jobs automate recurring maintenance, reminders, calendar refreshes, and health checks.

## Job Summary

| Job | Enabled | Schedule | Description |
|-----|---------|----------|-------------|
| 🗓️ calendar-fetch-hourly | Yes | `0 7-17 * * *` (America/Los_Angeles) | Fetch calendars hourly 7am-5pm PST |
| 💾 config-backup | Yes | Every 1 day | Backup openclaw.json to Git daily (only commits if changed) |
| 📰 evening-briefing | Yes | `0 22 * * 0-4` (America/Los_Angeles) | Weekday 9 PM briefing: what's on tap tomorrow morning |
| 📈 portfolio-closing-briefing | Yes | `0 21 * * 1-5` (America/Los_Angeles) | — |
| ⏰ evening-alarm-reminder | Yes | `30 22 * * *` (America/Los_Angeles) | Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting |
| 📦 Daily package delivery check | Yes | `0 8 * * *` (America/Los_Angeles) | — |
| 🩺 daily-health-check | Yes | `0 9 * * *` (America/Los_Angeles) | Daily health check — verifies email sending works; DMs Jeff if anything fails |
| 🍽️ Remind Jeff to reach out to Zack Ali for dinner | No | One-time | One-shot reminder to schedule another dinner with Zack Ali |
| 🏅 WW Daily Points Check-in | Yes | `30 17 * * *` (America/Los_Angeles) | — |
| ⚠️ late-early-conflict-morning-check | Yes | `0 10 * * *` (America/Los_Angeles) | 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM) |
| 🦞 Lobster changelog weekly scan | Yes | `0 9 * * 1` (America/Los_Angeles) | Weekly Monday scan of lobster.shahine.com/changelog for new ideas |
| 🌙 calendar-fetch-midnight | Yes | `0 0 * * *` (America/Los_Angeles) | Fetch calendars at midnight PST |
| 🥗 ww-diet-sync | Yes | `0 4 * * *` (America/Los_Angeles) | — |

## 🗓️ calendar-fetch-hourly

- **Enabled:** Yes
- **Schedule:** `0 7-17 * * *` (America/Los_Angeles)
- **Description:** Fetch calendars hourly 7am-5pm PST

## 💾 config-backup

- **Enabled:** Yes
- **Schedule:** Every 1 day
- **Description:** Backup openclaw.json to Git daily (only commits if changed)

## 📰 evening-briefing

- **Enabled:** Yes
- **Schedule:** `0 22 * * 0-4` (America/Los_Angeles)
- **Description:** Weekday 9 PM briefing: what's on tap tomorrow morning

## 📈 portfolio-closing-briefing

- **Enabled:** Yes
- **Schedule:** `0 21 * * 1-5` (America/Los_Angeles)
- **Description:** No description exported.

## ⏰ evening-alarm-reminder

- **Enabled:** Yes
- **Schedule:** `30 22 * * *` (America/Los_Angeles)
- **Description:** Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting

## 📦 Daily package delivery check

- **Enabled:** Yes
- **Schedule:** `0 8 * * *` (America/Los_Angeles)
- **Description:** No description exported.

## 🩺 daily-health-check

- **Enabled:** Yes
- **Schedule:** `0 9 * * *` (America/Los_Angeles)
- **Description:** Daily health check — verifies email sending works; DMs Jeff if anything fails

## 🍽️ Remind Jeff to reach out to Zack Ali for dinner

- **Enabled:** No
- **Schedule:** One-time
- **Description:** One-shot reminder to schedule another dinner with Zack Ali

## 🏅 WW Daily Points Check-in

- **Enabled:** Yes
- **Schedule:** `30 17 * * *` (America/Los_Angeles)
- **Description:** No description exported.

## ⚠️ late-early-conflict-morning-check

- **Enabled:** Yes
- **Schedule:** `0 10 * * *` (America/Los_Angeles)
- **Description:** 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)

## 🦞 Lobster changelog weekly scan

- **Enabled:** Yes
- **Schedule:** `0 9 * * 1` (America/Los_Angeles)
- **Description:** Weekly Monday scan of lobster.shahine.com/changelog for new ideas

## 🌙 calendar-fetch-midnight

- **Enabled:** Yes
- **Schedule:** `0 0 * * *` (America/Los_Angeles)
- **Description:** Fetch calendars at midnight PST

## 🥗 ww-diet-sync

- **Enabled:** Yes
- **Schedule:** `0 4 * * *` (America/Los_Angeles)
- **Description:** No description exported.
