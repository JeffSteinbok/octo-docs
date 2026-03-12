---
layout: default
title: Skills
nav_order: 4
---

# Skills

## Overview

Skills are predefined sets of markdown-defined knowledge that enable agents to perform specific tasks or interact with external systems. Unlike plugins, which execute code, skills provide structured information and rules for handling specific domains or functionalities. Skills are used by agents to interpret user requests and perform actions within their defined scope.

## Key Concepts

- **Skills**: Markdown-defined knowledge used by agents to perform specific tasks.
- **Agents**: Utilize skills to interpret user requests and execute actions.
- **Difference from Plugins**: Skills are knowledge-based, while plugins execute code.
- **Usage Scope**: Each skill defines its own domain and rules for interaction.

## How It Works

1. **Skill Definition**: Skills are defined in markdown format, specifying their purpose, rules, and usage scenarios.
2. **Agent Interaction**: Agents use skills to interpret user input and determine the appropriate actions.
3. **Execution**: Skills guide agents in performing tasks, such as querying states, controlling devices, or providing structured responses.

## Available Skills

### 🎵 Home Music

**Purpose**:  
The Home Music skill enables agents to control music and speakers at home via Home Assistant. It is used for tasks such as adjusting volume, checking what's playing, pausing, resuming, skipping tracks, muting, and controlling devices like Alexa, Sonos, and other media players.

**Usage**:  
Agents use the Home Music skill to interact with various media player entities across different rooms and zones in the house. Common operations include getting the current state of a speaker, adjusting volume, muting/unmuting, and controlling playback.

**Key Features**:  
- Control individual speakers or groups of speakers (zones).
- Query and report current volume, track, and artist information.
- Perform playback actions like pause, play, skip, and previous.
- Support for Spotify integration via Home Assistant.

**Room Layout and Zones**:  
- **Downstairs**: Living Room, Kitchen, Home Theater  
- **Upstairs**: Main Bedroom, Hallway, Bonus Room  
- **Outside**: Outside Speakers  

Commands can be applied to specific rooms, zones, or all speakers. For example, "downstairs" applies to all entities in the downstairs zone, while "everywhere" applies to all speakers.

**Example Operations**:  
- **Get Current State**: Query the current volume, track, and artist for a specific speaker.  
- **Set Volume**: Adjust the volume of a speaker to a specific level.  
- **Mute/Unmute**: Toggle mute status for a speaker.  
- **Playback Control**: Pause, play, skip, or go to the previous track.  
- **Play Media**: Start playing a specific playlist or station.
