---
layout: default
title: Skills
nav_order: 4
---

# Skills Overview

## Overview

Skills are predefined sets of markdown-defined knowledge that enable agents to perform specific tasks or provide information. Unlike plugins, which are executable code, skills are structured as static knowledge bases that guide agents in handling particular scenarios. Skills are used by agents to enhance their functionality and provide targeted assistance in specific domains.

## Key Concepts

- **Skills**: Markdown-defined knowledge bases that guide agents in specific tasks.
- **Agents**: Utilize skills to perform actions or provide information based on user requests.
- **Difference from Plugins**: Skills are not executable code; they are static knowledge resources that inform agent behavior.

## How It Works

1. **Skill Definition**: Each skill is defined in markdown format and contains detailed instructions, rules, and examples for handling specific tasks.
2. **Agent Utilization**: Agents reference skills to determine how to respond to user requests. Skills provide guidance on what actions to take and how to structure responses.
3. **Non-Executable**: Unlike plugins, skills do not execute code but instead serve as a knowledge base for agents.

## Available Skills

### 🎵 Home Music

**Purpose**:  
The Home Music skill enables agents to control music and speakers in a home environment via Home Assistant. It is used for tasks such as adjusting volume, checking what is playing, pausing, resuming, skipping tracks, muting, and controlling devices like Alexa, Sonos, or other media players.

**Usage by Agents**:  
Agents use the Home Music skill to interact with home media players by leveraging Home Assistant service calls and state queries. This allows agents to perform actions such as retrieving the current volume, adjusting it, or controlling playback.

**Key Features**:  
- Control individual or grouped speakers in various rooms or zones (e.g., living room, kitchen, bedroom).
- Retrieve and report current playback state, including volume, track, and artist.
- Perform common operations like play, pause, skip, mute, and adjust volume.
- Support for Spotify integration with basic controls (future enhancements planned for playlist and search functionality).

**Room Layout and Zones**:  
The Home Music skill organizes speakers into rooms and zones for easier control. For example:
- **Downstairs**: Living Room, Kitchen, Home Theater
- **Upstairs**: Main Bedroom, Hallway, Bonus Room
- **Outside**: Outside Speakers

Commands can target specific rooms, zones, or all speakers simultaneously.

**How It Differs from Plugins**:  
The Home Music skill provides structured knowledge on how to interact with media players using Home Assistant. It does not execute code directly but instead guides agents on how to use Home Assistant plugins like `ha_state_get` and `ha_service_call` to perform actions.
