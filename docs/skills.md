---
layout: default
title: Skills
nav_order: 4
---

# Skills

Skills are markdown-defined guidance modules that agents load for domain-specific rules, workflows, and operating context.

Unlike plugins, skills do not execute code. They give agents shared instructions for how to use tools and interpret a problem domain.

## Skill Summary

| Skill | Used by | Description |
|-------|---------|-------------|
| 🎵 home-music | `main` | Control music and speakers at home via Home Assistant. Use when: adjusting volume on any speaker/room, checking what's playing, pausing/resuming/skipping music, muting, or controlling Alexa/Sonos/media players. Covers living room, kitchen, bedroom, bonus room, family room, hallway, and other HA media players. |

## 🎵 home-music

Control music and speakers at home via Home Assistant. Use when: adjusting volume on any speaker/room, checking what's playing, pausing/resuming/skipping music, muting, or controlling Alexa/Sonos/media players. Covers living room, kitchen, bedroom, bonus room, family room, hallway, and other HA media players.

- **Used by agent:** `main`
- **Published sections:** `Key Entities`, `Rules`, `Common Operations`, `Spotify (future)`, `List All Speaker Volumes`, `Room Layout / Zones`, `Discovery`

## How Skills Differ from Plugins

- **Skills** are bundled markdown knowledge for agents to read and follow.
- **Plugins** are executable integrations that expose callable tools and APIs.
- Skills can reference plugins, but they do not execute on their own.
