---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components of the system that facilitate communication between users and automated services. Agents represent distinct roles or personas, each with specific configurations and permissions. Channels are the mediums through which users interact with these agents, such as messaging platforms. Together, agents and channels enable seamless and structured user interactions.

## Key Concepts

- **Agents**: Configurable entities that represent roles or personas in the system.
- **Channels**: Communication mediums (e.g., Discord, Telegram) that connect users to agents.
- **Bindings**: Associations between agents and channels to enable communication.
- **Policies**: Rules governing direct messages (DMs) and group interactions within channels.

## How It Works

1. **Agent Configuration**:  
   Each agent is defined with a unique ID, name, and optional emoji for identification. Agents can be assigned specific permissions and execution settings to define their behavior.

2. **Channel Configuration**:  
   Channels are configured with a type (e.g., Discord, Telegram) and policies that control how users interact with agents. These policies include:
   - **DM Policy**: Determines how direct messages are handled (e.g., pairing users with agents).
   - **Group Policy**: Defines rules for group interactions (e.g., allowlist or open access).
   - **Streaming**: Indicates whether streaming is enabled for the channel.

3. **Binding Agents to Channels**:  
   Agents are bound to specific channels, enabling them to communicate with users through those channels. This binding ensures that agents are accessible only through the intended communication mediums.

4. **User Interaction**:  
   Users interact with agents via the configured channels. The system enforces the defined policies to manage these interactions, ensuring a consistent and secure experience.

## Agents

| ID   | Name       | Emoji |
|------|------------|-------|
| main | Octo       | 🐙    |
| mail | mail-agent | 📬    |
| root | Root       | 🔑    |

## Channels

| Type      | Enabled | DM Policy | Group Policy | Streaming |
|-----------|---------|-----------|--------------|-----------|
| Discord   | Yes     | Pairing   | Allowlist    | Off       |
| Telegram  | Yes     | Pairing   | Open         | Off       |

## How Channels Connect Users to Agents

Channels serve as the interface between users and agents. When a user sends a message through a channel, the system routes the message to the appropriate agent based on the channel's configuration and bindings. The agent processes the message and responds via the same channel, adhering to the channel's policies for direct messages and group interactions. This structure ensures that communication is both efficient and policy-compliant.
