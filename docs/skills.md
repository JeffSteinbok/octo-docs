---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured information and guidance for specific tasks. Unlike plugins, which are executable code, skills supply agents with domain-specific instructions, rules, and context to help them interact with external systems or perform actions. Skills solve the problem of giving agents reliable, reusable knowledge without requiring code execution.

## Key Concepts

- **Skills**: Markdown-defined knowledge modules used by agents for task-specific guidance.
- **Agents**: Entities that utilize skills to perform actions or answer questions.
- **Plugins vs. Skills**: Plugins are executable code; skills are static, markdown-based knowledge.
- **Entity Mapping**: Skills often include mappings between logical concepts (like rooms) and system entities.
- **Rules and Operations**: Skills define rules, common operations, and procedures for agents to follow.

## How It Works

1. Agents access skills to obtain structured knowledge about a domain or task.
2. Skills provide instructions, rules, and mappings that guide agents in interacting with external systems.
3. Agents use the information from skills to determine which actions to take, which entities to target, and how to report results.
4. Skills are not executable; agents interpret the markdown content and apply it as guidance.

---

## Available Skills

### 🎵 Home Music

**Purpose**:  
Control music and speakers at home via Home Assistant. This skill is used for adjusting volume, checking what's playing, pausing/resuming/skipping music, muting, and controlling Alexa, Sonos, and other media players across various rooms.

**Usage by Agents**:  
Agents use this skill to:
- Map user requests to specific Home Assistant media player entities.
- Follow rules for volume adjustment (always check current volume before changing).
- Query and report speaker status, including volume and currently playing track/artist.
- Apply commands to zones (e.g., "downstairs", "upstairs", "outside") or all speakers.
- Discover available entities and their states.

**Key Features**:
- Room and zone mapping to entity IDs.
- Volume control rules and reporting.
- Common operations: get state, set volume, mute/unmute, pause/play/skip, play specific media.
- Guidance for reporting only active speakers.
- Discovery instructions for available media player entities.

---

## How Skills Differ from Plugins

- **Skills** are markdown-defined knowledge, providing structured information and instructions.
- **Plugins** are executable code used for performing actions or retrieving data.
- Skills do not execute code; they guide agents in how to use plugins or interact with systems.
