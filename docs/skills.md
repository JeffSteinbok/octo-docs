---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are predefined sets of markdown-defined knowledge that enable agents to perform specific tasks or interact with external systems. Unlike plugins, which execute code, skills provide structured information and instructions that agents use to process and respond to user requests. Skills are designed to simplify complex operations and provide a consistent interface for interacting with various domains.

## Key Concepts

- **Skills vs Plugins**: Skills are markdown-defined knowledge, while plugins execute code. Skills focus on providing structured information for agents to use.
- **Agent Usage**: Agents use skills to interpret user requests and perform actions based on the knowledge defined in the skill.
- **Purpose**: Skills are tailored to specific domains or tasks, enabling agents to handle specialized scenarios effectively.

## How It Works

1. **Skill Definition**: Each skill is defined in markdown format, containing structured information about its purpose, rules, and supported operations.
2. **Agent Interaction**: When an agent receives a user request, it identifies the relevant skill based on the context and uses the knowledge defined within the skill to respond or perform actions.
3. **Execution**: The agent may use plugins to execute actions described in the skill, such as calling APIs or interacting with external systems.

## Available Skills

### 🎵 Home Music

**Purpose**:  
The Home Music skill enables agents to control music playback and speakers in various rooms via Home Assistant. It is used for tasks such as adjusting volume, checking what's playing, pausing/resuming/skipping tracks, muting, and controlling Alexa, Sonos, or other media players.

**Supported Rooms and Entities**:  
The skill covers the following rooms and media player entities:  

| Room          | Entity ID                     |
|---------------|-------------------------------|
| Living Room   | `media_player.alexa_living_room` |
| Kitchen       | `media_player.alexa_kitchen`     |
| Home Theater  | `media_player.home_theater`      |
| Hallway       | `media_player.hallway`           |
| Bonus Room    | `media_player.bonus_room`        |
| Family Room   | `media_player.family_room`       |
| Main Bedroom  | `media_player.main_bedroom`      |
| Outside       | `media_player.alexa_outside`     |

**Usage**:  
Agents use this skill to perform the following operations:  

- **Get Current State**: Retrieve the current volume, track, and artist for a specific media player.  
- **Set Volume**: Adjust the volume of a media player to a specific level.  
- **Volume Up/Down**: Increase or decrease the volume relative to the current level.  
- **Mute/Unmute**: Toggle mute status for a media player.  
- **Playback Control**: Pause, play, skip, or go back to the previous track.  
- **Play Specific Media**: Start playback of a specific playlist or station.  

**Zones**:  
Rooms are grouped into zones for easier control:  

| Zone       | Rooms                          | Entities                                   |
|------------|--------------------------------|-------------------------------------------|
| Downstairs | Living Room, Kitchen, Home Theater | `media_player.alexa_living_room`, `media_player.alexa_kitchen`, `media_player.home_theater` |
| Upstairs   | Main Bedroom, Hallway, Bonus Room | `media_player.main_bedroom`, `media_player.hallway`, `media_player.bonus_room` |
| Outside    | Outside Speakers               | `media_player.alexa_outside`              |

Commands can target individual rooms, zones, or all speakers (`media_player.all_speakers`).  

**Spotify Integration**:  
Spotify is supported via the `media_player.spotify_jeff_steinbok` entity. Standard playback and volume controls are available, with playlist and search functionality planned for future updates.  

**Discovery**:  
To discover available media player entities, agents can use the following command:  
```python
ha_state_list(domain="media_player")
```  
This will return a list of entities, including their current state and attributes.
