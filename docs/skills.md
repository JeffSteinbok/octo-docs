---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured information and guidance for specific tasks. Unlike plugins, which are executable code, skills are static documents that describe how to interact with various systems or perform operations. Skills help agents make informed decisions by outlining available entities, rules, and recommended flows for common scenarios.

Agents use skills to access domain-specific knowledge, such as how to control home music systems or query speaker status. This enables agents to respond accurately to user requests by following documented procedures and best practices.

## Key Concepts

- **Skills**: Markdown-defined documents containing task-specific knowledge and instructions.
- **Agents**: Entities that use skills to guide their actions and responses.
- **Plugins vs. Skills**: Plugins are executable code; skills are static knowledge, not code.
- **Entities**: Named objects (e.g., media players) referenced in skills for operations.
- **Zones**: Logical groupings of rooms or entities for bulk operations.

## How It Works

1. **Skill Definition**: Each skill is defined in markdown, outlining its purpose, relevant entities, rules, and common operations.
2. **Agent Usage**: Agents consult skills to determine how to perform tasks, such as controlling music or reporting speaker status.
3. **Entity Mapping**: Skills provide mappings between user-friendly names (like "living room") and system entity IDs.
4. **Operation Guidance**: Skills specify step-by-step flows, such as checking current volume before adjusting it, and reporting changes to users.
5. **Zone Handling**: Skills describe how to interpret zone names (e.g., "downstairs") and apply actions to all relevant entities.
6. **Discovery**: If an agent is unsure which entity to use, the skill describes how to discover available entities.

---

## Available Skills

### 🎵 Home Music

Control music and speakers at home via Home Assistant. Use this skill for:

- Adjusting volume on any speaker or room
- Checking what's playing
- Pausing, resuming, or skipping music
- Muting speakers
- Controlling Alexa, Sonos, and other media players

**Purpose:**  
Provides detailed instructions for interacting with home audio systems, including entity mappings for each room, operational rules (such as always checking current volume before changing it), and guidance for zone-based commands (e.g., "downstairs", "upstairs", "outside", "all speakers"). Covers standard operations like play, pause, volume adjustment, mute, and playlist selection.

---

## How Skills Are Used by Agents

Agents reference skills to:

- Map user requests to the correct entities and operations
- Follow documented rules (e.g., check volume before setting)
- Interpret zone names and apply actions to multiple entities
- Discover available entities when uncertain
- Provide accurate, context-aware responses to users

---

## How Skills Differ from Plugins

- **Skills** are markdown-defined knowledge, not executable code.
- **Plugins** are code modules that perform actions or queries.
- Skills provide structured information and procedures; plugins execute operations.
- Agents use skills for guidance and plugins for execution.
