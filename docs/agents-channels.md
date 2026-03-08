---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This documentation describes the agents and channels configured in the system, their roles, and how they interact. Agents are responsible for executing tasks and interacting with users, while channels serve as communication pathways connecting users to agents. Each agent has a specific security model, including permissions, execution settings, and accessible tools or plugins. Channels define the policies and mechanisms for user-agent communication.

## Key Concepts

- **Agents**: Components that perform tasks and interact with users. Each agent has a unique security model.
- **Channels**: Communication pathways that connect users to agents. Each channel has specific policies for direct messages and group interactions.
- **Security Model**: Defines the permissions, execution settings, and accessible tools for each agent.
- **Channel Policies**: Specify how users interact with agents via direct messages or group settings.

## How It Works

1. **Agent Configuration**: Each agent is configured with specific permissions, execution settings, and bindings to tools or plugins.
2. **Channel Configuration**: Channels are set up with policies that define how users can interact with agents, including direct message and group interaction rules.
3. **User-Agent Interaction**: Users connect to agents through channels. The channel policies determine the interaction flow, such as whether direct messages are allowed or restricted.

## Agents

### 🐙 Octo

- **Security Model**:
  - **Exec Enabled**: Yes
  - **Permissions**: Full access to all tools and plugins
  - **Tools/Plugins**: All available tools and plugins are accessible

### 📧 mail-agent

- **Security Model**:
  - **Exec Enabled**: No
  - **Permissions**: None
  - **Tools/Plugins**: None
- **Status**: Currently unused

### 🔑 Root

- **Security Model**:
  - **Exec Enabled**: Yes
  - **Permissions**: Elevated permissions with access to critical tools
  - **Tools/Plugins**: Limited to essential tools for administrative tasks

## Channels

| Channel Type | Enabled | Direct Message Policy | Group Policy | Streaming |
|--------------|---------|-----------------------|--------------|-----------|
| Discord      | Yes     | Pairing              | Allowlist    | Off       |
| Telegram     | Yes     | Pairing              | Open         | Off       |

### Channel-User-Agent Connection

- **Discord**: Users interact with agents through Discord. Direct messages are allowed based on a pairing policy, and group interactions are restricted to an allowlist.
- **Telegram**: Users interact with agents through Telegram. Direct messages are allowed based on a pairing policy, and group interactions are open to all users.
