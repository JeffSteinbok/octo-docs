---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components of the system, enabling communication and interaction between users and automated processes. Agents represent distinct entities with specific roles and permissions, while channels provide the medium through which users interact with these agents. This configuration allows for flexible and secure communication across multiple platforms.

## Key Concepts

- **Agents**: Autonomous entities with defined permissions, tools, and plugins.
- **Channels**: Communication mediums (e.g., Discord, Telegram) that connect users to agents.
- **Bindings**: Associations between agents and channels to facilitate interaction.
- **Security Model**: Permissions and execution settings for agents to ensure controlled operations.

## How It Works

1. **Agent Configuration**: Each agent is configured with a unique ID, name, emoji, permissions, and execution settings. These settings define the agent's capabilities and security boundaries.
2. **Channel Configuration**: Channels are set up with specific policies for direct messages (DMs), group interactions, and streaming settings. Enabled channels are bound to agents to enable communication.
3. **User Interaction**: Users interact with agents through channels. Channels act as the bridge, routing user input to the appropriate agent based on the bindings.

## Agents

### 🐙 Octo

- **Security Model**:  
  - Exec: Enabled  
  - Permissions: Full access  
  - Tools/Plugins: All available tools and plugins  

### 📫 mail-agent

- **Security Model**:  
  - Exec: Disabled  
  - Permissions: None  
  - Tools/Plugins: None  

> **Note**: The mail agent is currently unused.

### 🔑 Root

- **Security Model**:  
  - Exec: Enabled  
  - Permissions: Elevated access  
  - Tools/Plugins: All available tools and plugins  

### 👨‍👩‍👧‍👦 Family

- **Security Model**:  
  - Exec: Enabled  
  - Permissions: Restricted access  
  - Tools/Plugins: Limited tools and plugins  

## Channels

### Discord

- **Type**: Discord  
- **Enabled**: Yes  
- **DM Policy**: Pairing  
- **Group Policy**: Allowlist  
- **Streaming**: Off  
- **Bound Agents**: Octo, Root, Family  

### Telegram

- **Type**: Telegram  
- **Enabled**: Yes  
- **DM Policy**: Pairing  
- **Group Policy**: Open  
- **Streaming**: Off  
- **Bound Agents**: Octo, Root, Family  

## How Channels Connect Users to Agents

Channels serve as the interface for user interactions. When a user sends a message via a channel (e.g., Discord or Telegram), the message is routed to the appropriate agent based on the channel's bindings. The agent processes the input and responds through the same channel, enabling seamless communication.
