---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components of the system that enable interaction between users and automated processes. Agents are configured with specific permissions, tools, and execution capabilities to perform tasks, while channels serve as communication pathways for users to interact with these agents. This document outlines the available agents, their configurations, and the channels through which they operate.

## Key Concepts

- **Agents**: Configurable entities with specific permissions and capabilities to perform tasks.
- **Channels**: Communication pathways that connect users to agents.
- **Bindings**: Associations between agents and channels to enable user interactions.
- **Policies**: Rules governing direct messages (DMs) and group interactions within channels.

## How It Works

1. **Agent Configuration**: Each agent is configured with a unique set of permissions, execution capabilities, and access to specific tools or plugins.
2. **Channel Setup**: Channels are configured with policies that define how users can interact with agents, such as DM policies and group policies.
3. **Binding Agents to Channels**: Agents are bound to specific channels, enabling communication between users and agents through those channels.
4. **User Interaction**: Users interact with agents via the configured channels, adhering to the policies set for those channels.

## Agents

### 🐙 Octo

- **Security Model**:
  - **Exec**: Enabled
  - **Permissions**: Full access to all system resources
  - **Tools/Plugins**: Full access to all available tools and plugins

### 📧 mail-agent

- **Status**: Currently unused

### 🔑 Root

- **Security Model**:
  - **Exec**: Enabled
  - **Permissions**: Elevated permissions for administrative tasks
  - **Tools/Plugins**: Full access to all available tools and plugins

## Channels

| Channel Type | Enabled | DM Policy | Group Policy | Streaming | Bound Agents |
|--------------|---------|-----------|--------------|-----------|--------------|
| Discord      | Yes     | Pairing   | Allowlist    | Off       | Octo, Root   |
| Telegram     | Yes     | Pairing   | Open         | Off       | Octo, Root   |

## How Channels Connect Users to Agents

Channels act as the interface through which users communicate with agents. Each channel is configured with specific policies that define how users can interact:

- **DM Policy**: Determines how direct messages are handled. For example, the "pairing" policy requires users to be paired with an agent before direct communication is allowed.
- **Group Policy**: Defines the rules for group interactions. For instance, the "allowlist" policy restricts group interactions to approved users, while the "open" policy allows all users to participate.

Agents are bound to one or more channels, enabling them to respond to user requests and perform tasks within the constraints of the channel's policies.
