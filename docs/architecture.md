---
layout: default
title: Architecture
nav_order: 4
---

# Architecture

OpenClaw follows a modular, event-driven architecture where agents, skills,
channels, and services each play a distinct role.

## Components

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│   Channels   │◄───►│    Agents     │◄───►│   Skills   │
│  (Telegram,  │     │  (LLM-backed  │     │ (email,    │
│   Discord)   │     │   personas)   │     │  cameras,  │
└─────────────┘     └──────┬───────┘     │  dining)   │
                           │              └────────────┘
                    ┌──────▼───────┐
                    │   Services    │
                    │  (event       │
                    │   watchers)   │
                    └──────────────┘
```

## Agents

Agents are LLM-powered personas, each with their own identity, permissions,
and context. They decide which skills to invoke based on user requests.

| Agent | Role |
|-------|------|
| 🦞 Octo | Primary personal assistant — full access to all skills and tools |
| 🤖 group-agent | Generic group chat agent — responds only when mentioned |
| 🏠 family-agent | Family group chat agent with limited permissions |
| 📬 mail-agent | Email processing agent with read-only access |

## Channels

Channels are the messaging platforms through which users interact with agents.

| Platform | Status |
|----------|--------|
| Telegram | ✅ Enabled |
| Discord | ✅ Enabled |

## Skills

Skills are the system's capabilities: **fastmail-send, hass-camera-snapshot, opentable**.
Each is a self-contained module with declared dependencies, invoked by agents
as needed. See the [Skills](skills.html) page for details.

## Services

Services run continuously in the background, watching for events (new email,
calendar updates) and routing them as notifications through the messaging
channels. See the [Services](services.html) page for details.

## Design Principles

- **Modular:** Each skill and service is independently versioned and deployed
- **Secure:** Secrets stay in environment variables; public docs are auto-sanitized
- **Observable:** Services log to journald; agents maintain conversation history
- **Extensible:** New skills are added by dropping a folder with a `SKILL.md`