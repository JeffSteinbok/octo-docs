---
layout: default
title: Skills
nav_order: 2
---

# Skills

Skills are modular capabilities that agents can use. Each skill is a
self-contained package with its own metadata, dependencies, and commands.

## 📧 fastmail-send

Send emails and calendar meeting invitations via Fastmail JMAP.

**Capabilities:**

- Compose and send plain-text emails with optional CC and attachments
- Create meeting requests with accept/decline buttons (iCalendar)
- Configurable signature and sender identity

---

## 🔧 hass-camera-snapshot

Capture snapshots from home security cameras via Home Assistant.

**Capabilities:**

- Snap any individual camera or all cameras at once
- Automatically downloads and timestamps images locally
- Pre-flight checks with actionable error messages

---

## 🔧 opentable

Check real-time restaurant availability on OpenTable.

**Capabilities:**

- Look up restaurant IDs from OpenTable URL slugs
- Query available reservation slots by date, party size, and time
- Returns direct booking links for available times

**Dependencies:** python, requests, curl_cffi

---
