---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured guidance for specific tasks. Unlike plugins, which are executable code, skills contain curated instructions, rules, and entity mappings to help agents interact with external systems or perform domain-specific operations. Skills solve the problem of encoding domain knowledge in a reusable, accessible format for agents.

## Key Concepts

- **Skills**: Markdown-defined knowledge modules used by agents to perform tasks.
- **Agents**: Entities that use skills to interpret user requests and interact with external systems.
- **Plugins vs Skills**: Plugins are executable code; skills are structured knowledge, not code.
- **Entity Mapping**: Skills often include mappings between logical concepts (like rooms) and system entities.
- **Rules and Operations**: Skills define rules and common operations for agents to follow.

## How It Works

1. Agents receive user requests and determine which skill applies.
2. The agent consults the relevant skill's markdown content for guidance, including entity mappings and operational rules.
3. The agent uses plugins (executable code) to perform actions as instructed by the skill, such as querying states or calling services.
4. Skills provide step-by-step instructions, rules, and entity lists to ensure consistent and accurate task execution.

---

## Available Skills

### 🎵 Home Music

**Purpose**:  
Control music and speakers at home via Home Assistant. This skill is used for adjusting volume, checking what's playing, pausing/resuming/skipping music, muting, or controlling Alexa/Sonos/media players across various rooms and zones.

**How Agents Use This Skill**:
- Agents follow rules to check current volume before changing it, report old and new values, and use mapped entity IDs for each room or zone.
- Agents perform operations such as volume adjustment, mute/unmute, playback control, and playlist selection using Home Assistant plugin tools.
- Agents query individual room entities to report speaker status, only including speakers that are currently playing.

**Rooms and Entities**:

| Room           | Entity ID                        |
|----------------|----------------------------------|
| Living Room    | `media_player.alexa_living_room` |
| Kitchen        | `media_player.alexa_kitchen`     |
| Home Theater   | `media_player.home_theater`      |
| Hallway        | `media_player.hallway`           |
| Bonus Room     | `media_player.bonus_room`        |
| Family Room    | `media_player.family_room`       |
| Main Bedroom   | `media_player.main_bedroom`      |
| All Speakers   | `media_player.all_speakers`      |
| Downstairs     | `media_player.downstairs_2`      |
| Outside        | `media_player.alexa_outside`     |
| Spotify (Jeff) | `media_player.spotify_jeff_steinbok` |

**Zones**:

| Zone       | Rooms                                 | Entities                                                      |
|------------|---------------------------------------|---------------------------------------------------------------|
| Downstairs | Living Room, Kitchen, Home Theater    | `media_player.alexa_living_room`, `media_player.alexa_kitchen`, `media_player.home_theater` |
| Upstairs   | Main Bedroom, Hallway, Bonus Room     | `media_player.main_bedroom`, `media_player.hallway`, `media_player.bonus_room`              |
| Outside    | Outside Speakers                      | `media_player.alexa_outside`                                 |

**Common Operations**:
- Get current state (volume, track, etc.)
- Set volume (absolute or relative)
- Mute/unmute speakers
- Pause/play/skip tracks
- Play specific playlists or stations

**Discovery**:
If the agent is unsure which entity to use, it can list all media player entities and select those that are currently playing or match the room name.

---

## How Skills Differ from Plugins

- **Skills**: Provide structured, markdown-defined knowledge and operational guidance for agents.
- **Plugins**: Execute code to perform actions; skills instruct agents on how and when to use plugins.
- **Skills are not executable code**; they are reference material for agents to interpret and act upon user requests.
