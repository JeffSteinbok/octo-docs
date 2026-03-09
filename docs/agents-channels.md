---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This document describes the agents and channels configured in the system, their security models, and how they interact. Agents are responsible for executing tasks and responding to user interactions, while channels provide the communication pathways between users and agents. Together, they enable seamless and secure interactions across various platforms.

## Key Concepts

- **Agents**: Components that execute tasks and respond to user interactions. Each agent has specific permissions, execution settings, and access to tools or plugins.
- **Channels**: Communication pathways that connect users to agents. Each channel has specific policies governing direct messages, group interactions, and streaming capabilities.
- **Bindings**: The association between channels and agents, determining which agents are accessible through which channels.

## How It Works

1. **Agent Configuration**: Each agent is configured with specific permissions, execution settings, and access to tools or plugins. These configurations determine the agent's capabilities and security model.
2. **Channel Configuration**: Channels are configured with policies for direct messages, group interactions, and streaming. These settings define how users can interact with agents through the channel.
3. **Channel-Agent Binding**: Channels are bound to specific agents, enabling users to interact with the agents through the configured communication pathways.

## 🐙 Octo

### Security Model

- **Exec Enabled**: Yes
- **Permissions**: Full access to all system resources
- **Tools/Plugins**: Full access to all available tools and plugins

### Description

The Octo agent is the primary agent in the system, responsible for handling the majority of user interactions and executing tasks. It is configured with full permissions and access to all tools, making it the most versatile and capable agent.

## 📫 mail-agent

### Security Model

- **Exec Enabled**: No
- **Permissions**: None
- **Tools/Plugins**: None

### Description

The mail-agent is currently unused and does not participate in any interactions or task execution.

## 🔑 Root

### Security Model

- **Exec Enabled**: Yes
- **Permissions**: Elevated access for administrative tasks
- **Tools/Plugins**: Access to administrative tools only

### Description

The Root agent is designed for administrative purposes, with elevated permissions and access to specific tools required for system management.

## Channels

| Channel Type | Enabled | DM Policy | Group Policy | Streaming | Bound Agents |
|--------------|---------|-----------|--------------|-----------|--------------|
| Discord      | Yes     | Pairing   | Allowlist    | Off       | Octo, Root   |
| Telegram     | Yes     | Pairing   | Open         | Off       | Octo, Root   |

### Channel Details

- **Discord**: Supports direct messages with a pairing policy and group interactions with an allowlist policy. Streaming is disabled. This channel is bound to the Octo and Root agents.
- **Telegram**: Supports direct messages with a pairing policy and open group interactions. Streaming is disabled. This channel is bound to the Octo and Root agents.

### Channel-Agent Interaction

Channels serve as the communication interface between users and agents. Users interact with agents through the channels, and the channel configuration determines the scope and nature of these interactions. For example, direct messages may require pairing, while group interactions may be restricted to an allowlist or open to all users.
