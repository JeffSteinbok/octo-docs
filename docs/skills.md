---
layout: default
title: Skills
nav_order: 4
has_children: true
---

# Skills

Skills are markdown-defined guidance modules that agents load for domain-specific rules, workflows, and operating context.

Unlike plugins, skills do not execute code. They give agents shared instructions for how to use tools and interpret a problem domain.

Octo currently publishes **1 skill** in the public bundle.

| | Skill | Used by | Description |
|---|-------|---------|-------------|
| 🎵 | [Home Music](skills/home-music) | `main` | Control music and speakers at home via Home Assistant. Use when: adjusting volume on any speaker/room, checking what's playing, pausing/resuming/skipping music, muting, or controlling Alexa/Sonos/media players. Covers living room, kitchen, bedroom, bonus room, family room, hallway, and other HA media players. |

## How Skills Differ from Plugins

- **Skills** are bundled markdown knowledge for agents to read and follow.
- **Plugins** are executable integrations that expose callable tools and APIs.
- Skills can reference plugins, but they do not execute on their own.
