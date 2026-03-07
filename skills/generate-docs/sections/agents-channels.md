---
output: agents-channels.md
title: Agents & Channels
nav_order: 2
data_source: agents_channels
overrides:
  main: "Primary personal assistant — full access to all skills and tools"
  family-agent: "Family group chat agent with limited permissions"
  group-agent: "Generic group chat agent — responds only when mentioned"
  mail-agent: "Email processing agent with read-only access"
emoji_overrides:
  config-backup: "💾"
  fastmail: "📧"
  hass-camera-snapshot: "📷"
  homeassistant-cli: "🏡"
  ics-calendar: "📅"
  opentable: "🍽️"
  outlook-calendar: "📅"
  outlook-mail: "📬"
  outlook-work-calendar: "💼"
  weightwatchers: "⚖️"
---

## Agents

Agents are LLM-powered personas, each with their own identity, permissions,
and context. They decide which skills to invoke based on user requests.

{{ agents }}

## Channels

Channels are the messaging platforms through which users interact with agents.

{{ channels }}
