---
output: plugins.md
title: Plugins
nav_order: 4
data_keys:
  - plugins
---

Generate a documentation section for OpenClaw **plugins**.

Plugins are modular capabilities that agents can use. Each plugin is a
self-contained package with its own metadata, dependencies, and commands.

Use the `plugins` array from the provided data.

For each plugin, generate:
1. An H2 heading with a fun, relevant emoji you pick for the plugin and its name (e.g., `## 📧 fastmail-send`)
2. A description paragraph
3. If the plugin has `commands` (or `tools` or `functions`) in its data, list them
   under a **Commands:** subheading — show each command name in a code span and
   a brief one-line description of what it does
4. Capabilities listed under a **Capabilities:** subheading as bullet points
5. Dependencies if any, under a **Dependencies:** line
6. A horizontal rule (`---`) divider

### Manual Overrides

For the plugins listed below, use the provided description and capabilities
instead of the raw data description:

**config-backup** — Backup OpenClaw config to Git with automatic change detection.
- Detects changes to openclaw.json and commits only when needed
- Designed for cron — runs silently unless something goes wrong
- Supports forced commits for manual snapshots

**fastmail-send** — Send emails and calendar meeting invitations via Fastmail JMAP.
- Compose and send plain-text emails with optional CC and attachments
- Create meeting requests with accept/decline buttons (iCalendar)
- Configurable signature and sender identity

**hass-camera-snapshot** — Capture snapshots from home security cameras via Home Assistant.
- Snap any individual camera or all cameras at once
- Automatically downloads and timestamps images locally
- Pre-flight checks with actionable error messages

**homeassistant-cli** — Advanced Home Assistant control using the official hass-cli tool.
- Control lights, switches, climate, locks, and alarm systems
- Query entity states, history, and event logs
- Auto-completion and rich output formatting

**opentable** — Check real-time restaurant availability on OpenTable.
- Look up restaurant IDs from OpenTable URL slugs
- Query available reservation slots by date, party size, and time
- Returns direct booking links for available times

**outlook-work-calendar** — Fetch work calendar events from a published Outlook endpoint.
- Query events by date range with subject, time, and location
- Shows busy status and sensitivity level for scheduling
- No authentication required — uses published calendar feed

**personal-calendars** — Fetch personal and family calendars from Outlook Live ICS feeds.
- Query personal, family, or all calendars by date range
- Returns events with subject, time, and location
- Supports multiple calendar sources in a single query

Keep descriptions concise and factual.
