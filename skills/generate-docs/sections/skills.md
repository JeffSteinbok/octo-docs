---
output: skills.md
title: Plugins
nav_order: 3
data_source: plugins
overrides:
  config-backup:
    what: "Backup OpenClaw config to Git with automatic change detection."
    capabilities:
      - "Detects changes to openclaw.json and commits only when needed"
      - "Designed for cron — runs silently unless something goes wrong"
      - "Supports forced commits for manual snapshots"
  fastmail-send:
    what: "Send emails and calendar meeting invitations via Fastmail JMAP."
    capabilities:
      - "Compose and send plain-text emails with optional CC and attachments"
      - "Create meeting requests with accept/decline buttons (iCalendar)"
      - "Configurable signature and sender identity"
  hass-camera-snapshot:
    what: "Capture snapshots from home security cameras via Home Assistant."
    capabilities:
      - "Snap any individual camera or all cameras at once"
      - "Automatically downloads and timestamps images locally"
      - "Pre-flight checks with actionable error messages"
  homeassistant-cli:
    what: "Advanced Home Assistant control using the official hass-cli tool."
    capabilities:
      - "Control lights, switches, climate, locks, and alarm systems"
      - "Query entity states, history, and event logs"
      - "Auto-completion and rich output formatting"
  opentable:
    what: "Check real-time restaurant availability on OpenTable."
    capabilities:
      - "Look up restaurant IDs from OpenTable URL slugs"
      - "Query available reservation slots by date, party size, and time"
      - "Returns direct booking links for available times"
  outlook-work-calendar:
    what: "Fetch work calendar events from a published Outlook endpoint."
    capabilities:
      - "Query events by date range with subject, time, and location"
      - "Shows busy status and sensitivity level for scheduling"
      - "No authentication required — uses published calendar feed"
  personal-calendars:
    what: "Fetch personal and family calendars from Outlook Live ICS feeds."
    capabilities:
      - "Query personal, family, or all calendars by date range"
      - "Returns events with subject, time, and location"
      - "Supports multiple calendar sources in a single query"
---

Plugins are modular capabilities that agents can use. Each plugin is a
self-contained package with its own metadata, dependencies, and commands.

{{ items }}
