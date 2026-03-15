---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components of the system that enable user interactions and task execution. Agents represent distinct entities with specific capabilities and permissions, while channels provide the communication pathways connecting users to these agents. This configuration allows for flexible and secure interactions across multiple platforms.

## Key Concepts

- **Agents**: Entities with defined permissions, tools, and plugins for executing tasks.
- **Channels**: Communication pathways that connect users to agents.
- **Security Model**: Each agent has specific permissions and settings, including whether execution (`exec`) is enabled.
- **Bindings**: Channels are bound to agents, determining which agent handles user interactions on a given platform.

## How It Works

1. **Agents Configuration**: Each agent is configured with a unique identifier, name, emoji, permissions, and tools/plugins. Execution (`exec`) settings determine whether the agent can perform tasks directly.
2. **Channels Setup**: Channels are configured with specific policies for direct messages (DMs) and group interactions. Enabled channels are bound to agents, facilitating communication between users and agents.
3. **User Interaction**: Users interact with agents through channels. Channels route messages and requests to the appropriate agent based on the binding configuration.

## Agents

### 🐙 Octo

- **Security Model**:
  - Exec: Enabled
  - Permissions: Full access
  - Tools/Plugins: All available tools and plugins
- **Description**: Octo is the primary agent responsible for handling most tasks and interactions.

### 📫 mail-agent

- **Security Model**:
  - Exec: Disabled
  - Permissions: None
  - Tools/Plugins: None
- **Description**: The mail agent is currently unused and does not handle any tasks or interactions.

### 🔑 Root

- **Security Model**:
  - Exec: Enabled
  - Permissions: Elevated access
  - Tools/Plugins: Administrative tools only
- **Description**: Root is a specialized agent with elevated permissions for administrative tasks.

### 👨‍👩‍👧‍👦 Family

- **Security Model**:
  - Exec: Enabled
  - Permissions: Limited access
  - Tools/Plugins: Family-specific tools and plugins
- **Description**: Family is an agent configured for handling tasks related to family-oriented interactions.

## Channels

### Discord

- **Type**: Discord
- **Enabled**: Yes
- **DM Policy**: Pairing
- **Group Policy**: Allowlist
- **Streaming**: Off
- **Bound Agents**: Octo, Family

### Telegram

- **Type**: Telegram
- **Enabled**: Yes
- **DM Policy**: Pairing
- **Group Policy**: Open
- **Streaming**: Off
- **Bound Agents**: Octo, Family

## How Channels Connect Users to Agents

Channels act as communication pathways, routing user messages and requests to the appropriate agent based on the binding configuration. Each channel has specific policies for direct messages and group interactions, ensuring secure and controlled communication.
