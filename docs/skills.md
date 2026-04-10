---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that enable agents to perform specific tasks or answer questions in specialized domains. Unlike plugins, which are executable code, skills provide structured information and operational rules that guide agent behavior. Skills help agents interact with external systems, follow best practices, and deliver accurate responses by leveraging domain-specific knowledge.

Agents use skills to understand how to interact with various services or devices, ensuring consistent and reliable actions. Skills are not executable; instead, they serve as reference guides for agents, outlining procedures, available entities, and operational rules.

## Key Concepts

- **Skills**: Markdown-defined knowledge modules used by agents to perform domain-specific tasks.
- **Agents**: Entities that utilize skills to guide their actions and responses.
- **Plugins vs. Skills**: Plugins are executable code; skills are structured knowledge, not code.
- **Entities**: Devices or services referenced within skills (e.g., media players).
- **Zones**: Logical groupings of entities (e.g., rooms or areas in a home).

## How It Works

1. **Skill Definition**: Each skill is defined in markdown, specifying its purpose, entities, operational rules, and procedures.
2. **Agent Usage**: Agents reference skills to determine how to interact with external systems, which entities to use, and what steps to follow.
3. **Operational Guidance**: Skills provide step-by-step instructions, rules, and entity mappings, ensuring agents perform tasks correctly.
4. **Zone Handling**: Skills may define zones (e.g., "downstairs", "upstairs") to help agents apply actions across multiple entities.
5. **Discovery**: If an agent is unsure which entity to use, skills may provide discovery procedures.

---

## Available Skills

### 🎵 Home Music

Control music and speakers at home via Home Assistant. Use this skill for:

- Adjusting volume on any speaker or room
- Checking what's playing
- Pausing, resuming, or skipping music
- Muting speakers
- Controlling Alexa, Sonos, and other media players

**Purpose**:  
Enables agents to manage home audio systems, including volume control, playback operations, and reporting current status across various rooms and zones.

**Key Features**:

- Covers living room, kitchen, bedroom, bonus room, family room, hallway, and other Home Assistant media players.
- Provides entity mappings for each room and zone.
- Specifies operational rules (e.g., always check current volume before changing).
- Supports zone-based commands (e.g., "downstairs", "upstairs", "outside", "all speakers").
- Includes discovery instructions for identifying active media players.

---

## How Skills Are Used by Agents

Agents reference skills to:

- Identify which entities to interact with based on user commands.
- Follow operational rules (e.g., check current volume before setting a new value).
- Apply actions across zones or individual rooms.
- Report status and perform actions only on active devices.
- Use discovery procedures when entity mapping is unclear.

---

## How Skills Differ from Plugins

- **Skills**: Provide markdown-defined knowledge, operational rules, and entity mappings. They are not executable code.
- **Plugins**: Are executable code modules that perform actions or retrieve data.
- Skills guide agent behavior; plugins execute tasks.

---

## Example Usage

_No examples are present in the source material._
