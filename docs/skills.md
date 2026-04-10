---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are markdown-defined knowledge modules that provide agents with structured information and guidance for specific domains or tasks. Unlike plugins, which are executable code, skills are static documents that help agents interpret user requests and interact with external systems using available tools. Skills solve the problem of encoding domain-specific knowledge in a reusable, accessible format for agents.

Agents use skills to understand how to perform actions, query states, and apply rules within a domain. Skills guide agents in mapping user intents to tool calls, ensuring consistent and accurate responses.

## Key Concepts

- **Skills**: Markdown documents containing domain-specific knowledge, instructions, and rules.
- **Agents**: Entities that use skills to interpret user requests and interact with external systems.
- **Plugins vs Skills**: Plugins are executable code; skills are static markdown knowledge, not code.
- **Tool Calls**: Agents use skills to determine when and how to call plugins/tools for actions or queries.
- **Entities and Zones**: Skills define relevant entities (e.g., speakers, rooms) and zones for context-aware actions.

## How It Works

1. **Agent Receives User Request**  
   The agent interprets the user's intent and identifies which skill is relevant.

2. **Skill Guidance**  
   The agent consults the skill's markdown content to understand domain-specific rules, entities, and recommended actions.

3. **Tool Calls**  
   Based on the skill's instructions, the agent uses plugins/tools to perform actions (e.g., querying state, setting volume).

4. **Response Construction**  
   The agent follows skill rules to construct user-facing responses, including reporting relevant information and applying domain-specific logic.

## Available Skills

### 🎵 Home Music

Control music and speakers at home via Home Assistant.  
Purpose:  
- Adjust volume on any speaker or room  
- Check what's playing  
- Pause, resume, skip music  
- Mute speakers  
- Control Alexa, Sonos, and other media players across various rooms and zones

#### How Agents Use This Skill

- Agents reference the skill to determine which entities correspond to each room or zone.
- Agents follow rules such as checking current volume before changing it and reporting both old and new values.
- Agents use tool calls (e.g., `hass_state_get`, `hass_service_call`) as described in the skill to interact with media players.
- Agents apply zone logic (e.g., "downstairs", "upstairs", "outside") to target multiple entities as needed.
- Agents only report speakers that are actively playing, skipping idle or unavailable devices.

#### Skill vs Plugin

- The Home Music skill is a markdown document providing knowledge and rules.
- Plugins (such as `hass_state_get`, `hass_service_call`) are executable tools used by agents, but the skill itself is not code.

#### Supported Rooms and Entities

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

#### Zones

- **Downstairs**: Living Room, Kitchen, Home Theater
- **Upstairs**: Main Bedroom, Hallway, Bonus Room
- **Outside**: Outside Speakers

When users reference a zone, agents apply actions to all entities in that zone.

---

No usage examples are present in the source material.
