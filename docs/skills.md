---
layout: default
title: Skills
nav_order: 3
---

# Skills

Skills are modular capabilities that agents can use. Each skill is a
self-contained package with its own metadata, dependencies, and commands.

## 🔧 config-backup

Backup OpenClaw config to Git with automatic change detection.

**Capabilities:**

- Detects changes to openclaw.json and commits only when needed
- Designed for cron — runs silently unless something goes wrong
- Supports forced commits for manual snapshots

---

## 📧 fastmail-send

📦 [Source on GitHub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/fastmail-send)

Send emails and calendar meeting invitations via Fastmail JMAP.

**Capabilities:**

- Compose and send plain-text emails with optional CC and attachments
- Create meeting requests with accept/decline buttons (iCalendar)
- Configurable signature and sender identity

---

## 🔧 hass-camera-snapshot

📦 [Source on GitHub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/hass-camera-snapshot)

Capture snapshots from home security cameras via Home Assistant.

**Capabilities:**

- Snap any individual camera or all cameras at once
- Automatically downloads and timestamps images locally
- Pre-flight checks with actionable error messages

---

## 🏡 homeassistant-cli

Advanced Home Assistant control using the official hass-cli tool.

**Capabilities:**

- Control lights, switches, climate, locks, and alarm systems
- Query entity states, history, and event logs
- Auto-completion and rich output formatting

---

## 🔧 opentable

📦 [Source on GitHub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/opentable)

Check real-time restaurant availability on OpenTable.

**Capabilities:**

- Look up restaurant IDs from OpenTable URL slugs
- Query available reservation slots by date, party size, and time
- Returns direct booking links for available times

**Dependencies:** python, requests, curl_cffi

---

## 🔧 outlook-work-calendar

Fetch work calendar events from a published Outlook endpoint.

**Capabilities:**

- Query events by date range with subject, time, and location
- Shows busy status and sensitivity level for scheduling
- No authentication required — uses published calendar feed

---

## 🔧 personal-calendars

Fetch personal and family calendars from Outlook Live ICS feeds.

**Capabilities:**

- Query personal, family, or all calendars by date range
- Returns events with subject, time, and location
- Supports multiple calendar sources in a single query

---
