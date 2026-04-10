---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured information and guidance for specific tasks. Unlike plugins, which are executable code, skills are static documents that help agents understand how to interact with external systems or perform domain-specific operations. Skills solve the problem of encoding domain knowledge in a reusable, accessible format for agents.

Agents use skills to inform their actions, interpret user requests, and determine the correct procedures for interacting with external services or devices. Skills are referenced by agents when handling tasks that require specialized knowledge, such as controlling home devices or managing media playback.

## Key Concepts

- **Skills**: Markdown-defined documents containing domain knowledge and operational guidance.
- **Agents**: Entities that use skills to inform their actions and respond to user requests.
- **Plugins vs. Skills**: Plugins are executable code; skills are static knowledge, not code.
- **Entity Mapping**: Skills often include mappings between user-friendly names and system entity IDs.
- **Operational Rules**: Skills may specify rules or best practices for performing actions.

## How It Works

1. An agent receives a user request related to a domain covered by a skill.
2. The agent consults the relevant skill document to determine the correct entities, actions, and procedures.
3. The agent follows any operational rules or best practices outlined in the skill.
4. The agent may use plugins to execute actions, but relies on skills for guidance and knowledge.

## Available Skills

### 🎵 Home Music

Control music and speakers at home via Home Assistant. This skill covers adjusting volume, checking what's playing, pausing/resuming/skipping music, muting, and controlling Alexa, Sonos, and other media players. It includes guidance for the living room, kitchen, bedroom, bonus room, family room, hallway, and other Home Assistant media players.

**Purpose**:  
Provides agents with knowledge about controlling home speakers and music, including entity mappings, operational rules (such as checking current volume before changing it), and zone definitions for grouped actions.

**Usage by Agents**:  
Agents use this skill to:
- Identify the correct media player entities for each room or zone.
- Follow rules for volume adjustment and reporting.
- Determine how to mute, pause, play, skip tracks, and play specific playlists.
- Aggregate and report speaker status across rooms and zones.
- Discover available media player entities when unsure.

**Difference from Plugins**:  
This skill is a markdown document containing structured knowledge and operational guidance. It does not execute code; instead, it informs agents how to use plugin tools (such as `hass_state_get` and `hass_service_call`) to perform actions.

**Zones and Entities**:

| Zone        | Rooms                                     | Entities                                                      |
|-------------|-------------------------------------------|---------------------------------------------------------------|
| Downstairs  | Living Room, Kitchen, Home Theater        | `media_player.alexa_living_room`, `media_player.alexa_kitchen`, `media_player.home_theater` |
| Upstairs    | Main Bedroom, Hallway, Bonus Room         | `media_player.main_bedroom`, `media_player.hallway`, `media_player.bonus_room`              |
| Outside     | Outside Speakers                          | `media_player.alexa_outside`                                 |

**Common Operations**:
- Get current state (volume, track, etc.)
- Set volume (absolute or relative)
- Mute/unmute speakers
- Pause/play/skip tracks
- Play specific playlists or stations
- Aggregate and report speaker status

**Discovery**:  
Agents can list available media player entities and their states to determine which speakers are active and which entity to use for a given command.

---

*No other skills are currently available.*
