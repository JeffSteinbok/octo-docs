---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components that enable communication between users and the system. Agents represent distinct entities that perform specific roles, while channels define the mediums through which users interact with these agents. This system allows for flexible configuration of agents and channels to meet various communication needs.

## Key Concepts

- **Agents**: Represent distinct entities with specific roles and configurations.
- **Channels**: Define the communication mediums (e.g., Discord, Telegram) through which users interact with agents.
- **Bindings**: Specify which agents are accessible through which channels.
- **Policies**: Define rules for direct messages (DMs) and group interactions within channels.

## How It Works

1. **Agent Configuration**:  
   Agents are configured with unique identifiers, names, and optional emoji representations. These identifiers are used to bind agents to specific channels.

2. **Channel Configuration**:  
   Channels are configured with their type (e.g., Discord, Telegram), policies for direct messages and group interactions, and streaming settings. Channels must be enabled to allow communication.

3. **Agent-Channel Binding**:  
   Agents are bound to channels, enabling users to interact with specific agents through the configured communication mediums.

4. **User Interaction**:  
   Users connect to agents via channels. Policies such as DM pairing and group allowlists determine how users can interact with agents within each channel.

## Agents

| ID   | Name       | Emoji   |
|------|------------|---------|
| main | Octo       | 🐙      |
| mail | mail-agent | 📬      |
| root | Root       | 🔑      |

### Agent Configuration

- **Permissions**: Agents are assigned roles and permissions based on their intended functionality.
- **Execution Settings**: Each agent operates within its defined scope and capabilities.
- **Bindings**: Agents are linked to specific channels to enable communication.

## Channels

| Type      | Enabled | DM Policy | Group Policy | Streaming |
|-----------|---------|-----------|--------------|-----------|
| Discord   | Yes     | Pairing   | Allowlist    | Off       |
| Telegram  | Yes     | Pairing   | Open         | Off       |

### Channel Details

- **Discord**: Supports direct messages with a pairing policy and group interactions restricted to an allowlist. Streaming is disabled.
- **Telegram**: Supports direct messages with a pairing policy and open group interactions. Streaming is disabled.

### Channel-User Connection

Channels serve as the interface for users to interact with agents. The policies configured for each channel determine how users can communicate with agents, ensuring secure and controlled interactions.
