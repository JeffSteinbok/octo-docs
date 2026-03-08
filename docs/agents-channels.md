---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components that enable communication and interaction within the system. Agents represent distinct entities with specific roles, while channels define the communication platforms through which agents interact with users. This structure allows for flexible and scalable communication across multiple platforms.

## Key Concepts

- **Agents**: Represent distinct entities with unique roles and identifiers.
- **Channels**: Define the communication platforms (e.g., Discord, Telegram) through which agents interact with users.
- **Agent-Channel Interaction**: Agents are connected to channels to facilitate communication, with configurable policies for direct messages and group interactions.

## How It Works

1. **Agents**:  
   Agents are predefined entities, each with a unique identifier, name, and emoji representation. They serve as the primary actors in the system.  
   - Example agents:
     - **Octo** (`id: main`, emoji: 🐙)
     - **mail-agent** (`id: mail`, emoji: 📬)
     - **Root** (`id: root`, emoji: 🔑)

2. **Channels**:  
   Channels represent communication platforms where agents interact with users. Each channel has specific configurations for direct messages, group interactions, and streaming capabilities.  
   - Example channels:
     - **Discord**:
       - Direct message policy: Pairing
       - Group policy: Allowlist
       - Streaming: Off
     - **Telegram**:
       - Direct message policy: Pairing
       - Group policy: Open
       - Streaming: Off

3. **Interaction**:  
   Agents are connected to channels to enable communication. The interaction behavior is governed by the channel's policies:
   - **Direct Message Policy**: Determines how agents handle one-on-one communication.
   - **Group Policy**: Defines the rules for agent participation in group conversations.
   - **Streaming**: Indicates whether real-time streaming is enabled for the channel.

## Common Pitfalls

- Ensure that channels are properly enabled; disabled channels will not facilitate communication.
- Verify that the direct message and group policies align with the intended use case to avoid unexpected behavior.
- Streaming is disabled by default for all channels; ensure this setting is configured if real-time streaming is required.
