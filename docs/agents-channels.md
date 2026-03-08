---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components that enable communication between users and the system. Agents represent distinct entities with specific roles, while channels define the mediums through which users interact with these agents. This system allows for flexible configuration of agents and channels to support various communication needs.

## Key Concepts

- **Agents**: Entities that perform specific roles within the system, each identified by a unique ID and associated with a name and emoji.
- **Channels**: Communication mediums (e.g., Discord, Telegram) that connect users to agents.
- **Permissions and Policies**: Channels have configurable policies for direct messages (DMs) and group interactions.
- **Bindings**: Channels are linked to agents to facilitate communication.

## How It Works

1. **Agent Configuration**: Each agent is defined with a unique ID, name, and emoji. These attributes help identify the agent and its role in the system.
2. **Channel Configuration**: Channels are configured with a type (e.g., Discord, Telegram), enabled status, and policies for managing user interactions:
   - **DM Policy**: Defines how direct messages are handled (e.g., pairing users with agents).
   - **Group Policy**: Specifies how group interactions are managed (e.g., allowlist or open access).
   - **Streaming**: Indicates whether real-time streaming is enabled.
3. **Connecting Users to Agents**: Channels serve as the bridge between users and agents. Based on the configured policies, users can interact with agents via the enabled channels.

## Agents

| ID    | Name       | Emoji | Description |
|-------|------------|-------|-------------|
| main  | Octo       | 🐙    | Represents the primary agent in the system. |
| mail  | mail-agent | 📬    | Handles email-related interactions. |
| root  | Root       | 🔑    | Serves as the root-level agent with elevated permissions. |

## Channels

| Type      | Enabled | DM Policy | Group Policy | Streaming | Bound Agents |
|-----------|---------|-----------|--------------|-----------|--------------|
| Discord   | Yes     | Pairing   | Allowlist    | Off       | All agents   |
| Telegram  | Yes     | Pairing   | Open         | Off       | All agents   |
