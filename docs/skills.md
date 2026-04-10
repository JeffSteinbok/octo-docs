---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured information and guidance for specific tasks. Unlike plugins, which are executable code, skills offer detailed instructions, rules, and context to help agents interact with external systems or perform domain-specific actions. Skills solve the problem of encapsulating operational knowledge in a reusable, accessible format for agents.

## Key Concepts

- **Skills**: Markdown-defined knowledge modules containing instructions, rules, and context for specific tasks.
- **Agents**: Entities that use skills to perform actions or answer questions based on the provided knowledge.
- **Plugins vs. Skills**: Plugins are executable code, while skills are static knowledge and operational guidance.
- **Skill Usage**: Agents reference skills to determine how to interact with external systems or follow domain-specific procedures.

## How It Works

1. Skills are defined in markdown and include detailed instructions, rules, and context for a specific domain or task.
2. Agents consult skills to understand how to perform actions, such as controlling devices or reporting status.
3. Skills guide agents on which entities to interact with, what operations are allowed, and how to interpret and present information.
4. Agents use plugins to execute actions, but rely on skills for the knowledge of when and how to use those plugins.

---

## Available Skills

### 🎵 Home Music

Control music and speakers at home via Home Assistant. Use this skill when adjusting volume on any speaker or room, checking what's playing, pausing/resuming/skipping music, muting, or controlling Alexa, Sonos, and other media players. Covers living room, kitchen, bedroom, bonus room, family room, hallway, and other Home Assistant media players.

**Purpose**:  
Provides agents with detailed instructions for controlling home audio devices, including entity mapping, volume rules, zone definitions, and common operations.

**How Agents Use It**:
- Reference entity IDs for specific rooms or zones.
- Follow rules for volume adjustment (always check current volume before changing).
- Use provided operations for play, pause, mute, skip, and playlist selection.
- Aggregate and report speaker status by querying individual entities.
- Apply commands to zones (downstairs, upstairs, outside) or all speakers as needed.
- Discover available media players and their states.

**Skill vs. Plugin**:  
This skill contains operational knowledge and guidance. Actual actions (such as changing volume or playing music) are performed by plugins like `hass_state_get` and `hass_service_call`, but the skill provides the context and rules for their use.
