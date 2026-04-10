---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured information and guidance for specific tasks. Unlike plugins, which are executable code, skills are not code—they are documentation that helps agents understand how to interact with external systems or perform domain-specific operations. Skills solve the problem of giving agents clear, actionable instructions for complex tasks without requiring code execution.

Agents use skills to inform their decision-making and generate actions based on the documented procedures and rules. This enables agents to operate effectively within defined domains, such as home automation, by referencing skill content for context, entity mapping, and operational guidelines.

## Key Concepts

- **Skills**: Markdown-defined knowledge modules containing instructions, rules, and entity mappings for specific domains.
- **Agents**: Systems or processes that use skills to guide their actions and interactions.
- **Plugins vs. Skills**: Plugins are executable code; skills are documentation and knowledge, not code.
- **Entity Mapping**: Skills often include mappings between domain concepts (e.g., rooms) and system entities.
- **Operational Rules**: Skills specify rules and best practices for performing tasks (e.g., always check current volume before changing it).

## How It Works

1. Agents reference skills to understand how to perform domain-specific tasks.
2. Skills provide detailed instructions, entity mappings, and operational rules.
3. Agents use this information to generate actions, such as querying the state of a device or adjusting settings.
4. Skills guide agents in interpreting user commands, mapping them to system entities, and following best practices (e.g., reporting volume changes).
5. Skills are not executable; agents use them as knowledge sources to inform their behavior.

## Available Skills

### 🎵 Home Music

**Purpose**:  
Control music and speakers at home via Home Assistant. This skill covers adjusting volume, checking what's playing, pausing/resuming/skipping music, muting, and controlling Alexa, Sonos, and other media players across various rooms.

**Description**:  
- Provides entity mappings for speakers in rooms such as Living Room, Kitchen, Bedroom, Bonus Room, Family Room, Hallway, and more.
- Specifies operational rules, such as always checking current volume before changing it and reporting both old and new values.
- Details common operations: getting current state, setting volume, muting/unmuting, playback controls, and playing specific playlists or stations.
- Includes guidance for zone-based commands (e.g., "downstairs", "upstairs", "outside") and reporting speaker status.
- Spotify integration is available as a media player entity, with standard controls.

**How Agents Use This Skill**:  
Agents use the Home Music skill to:
- Map user commands to the correct Home Assistant entities.
- Follow documented procedures for querying and controlling media players.
- Apply zone-based actions when users reference areas like "downstairs" or "all speakers".
- Report speaker status and track information according to documented rules.

## How Skills Differ from Plugins

- **Skills** are markdown-defined documentation and knowledge, not executable code.
- **Plugins** are executable code modules that perform actions.
- Agents use skills for guidance and context, while plugins are used to execute specific operations.
