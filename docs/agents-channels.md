---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components that enable communication between users and the system. Agents represent distinct roles or personas within the system, each with specific configurations and responsibilities. Channels define the mediums through which users interact with agents, such as messaging platforms. Together, they facilitate seamless user interactions across supported platforms.

## Key Concepts

- **Agents**: Configurable entities that represent roles or personas within the system.
- **Channels**: Communication mediums (e.g., Discord, Telegram) that connect users to agents.
- **Agent Configuration**: Includes permissions, execution settings, and bindings to specific channels.
- **Channel Policies**: Define how users interact with agents in direct messages and group settings.

## How It Works

1. **Agent Configuration**:  
   Each agent is configured with a unique identifier, name, and optional emoji. These attributes help define the agent's role and how it is presented to users.

2. **Channel Setup**:  
   Channels are configured with specific types (e.g., Discord, Telegram) and policies that govern user interactions. Channels can be enabled or disabled based on system requirements.

3. **Agent-Channel Binding**:  
   Agents are bound to specific channels, enabling them to interact with users on those platforms. The configuration ensures that agents are accessible only through the intended channels.

4. **User Interaction**:  
   Users interact with agents via the configured channels. Policies such as direct message (DM) and group policies determine how these interactions occur.

## Agents

| ID    | Name        | Emoji | Description |
|-------|-------------|-------|-------------|
| main  | Octo        | 🐙    | Represents the primary agent in the system. |
| mail  | mail-agent  | 📬    | Handles email-related interactions. |
| root  | Root        | 🔑    | A privileged agent with elevated permissions. |

## Channels

| Type      | Enabled | DM Policy | Group Policy | Streaming |
|-----------|---------|-----------|--------------|-----------|
| Discord   | Yes     | Pairing   | Allowlist    | Off       |
| Telegram  | Yes     | Pairing   | Open         | Off       |

## How Channels Connect Users to Agents

Channels serve as the interface through which users communicate with agents. Each channel is configured with specific policies:

- **DM Policy**: Determines how direct messages are handled. For example, the "pairing" policy ensures that users are paired with specific agents for one-on-one interactions.
- **Group Policy**: Defines how agents participate in group conversations. Policies such as "allowlist" and "open" control whether agents can join specific groups or all groups.
- **Streaming**: Indicates whether real-time streaming of messages is enabled for the channel.

By binding agents to channels, the system ensures that users can interact with the appropriate agents through their preferred communication platforms.
