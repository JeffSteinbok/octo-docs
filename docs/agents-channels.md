---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This documentation provides an overview of the agents and channels configured in the system. Agents are responsible for handling specific tasks and interactions, while channels serve as communication pathways connecting users to these agents. The configuration defines the security model, permissions, and bindings between agents and channels.

## Key Concepts

- **Agents**: Components that perform specific tasks or handle interactions. Each agent has a unique security model, permissions, and accessible tools or plugins.
- **Channels**: Communication pathways (e.g., Discord, Telegram) that connect users to agents. Channels have specific policies for direct messages (DMs) and group interactions.
- **Bindings**: The association between agents and channels, determining which agent handles interactions on a given channel.

## How It Works

1. **Agent Configuration**: Each agent is configured with specific permissions, execution settings, and access to tools or plugins. These settings define the agent's capabilities and security model.
2. **Channel Configuration**: Channels are set up with policies for direct messages and group interactions, as well as their enabled/disabled status.
3. **Binding**: Channels are bound to specific agents, enabling users to interact with the appropriate agent through the channel.
4. **User Interaction**: Users communicate through channels, and the bound agent processes and responds to their requests.

## Agents

### 🐙 Octo

- **Security Model**: 
  - Execution: Enabled.
  - Permissions: Configured to handle general tasks and interactions.
  - Tools/Plugins: Has access to the necessary tools for its operations.

### 📧 mail-agent

- **Security Model**: 
  - Execution: Disabled.
  - Permissions: Not configured for active use.
  - Tools/Plugins: No tools or plugins are accessible.
- **Note**: This agent is currently unused.

### 🔑 Root

- **Security Model**: 
  - Execution: Enabled.
  - Permissions: Full administrative permissions.
  - Tools/Plugins: Has access to all tools and plugins in the system.

## Channels

| Channel Type | Enabled | DM Policy | Group Policy | Streaming | Bound Agent |
|--------------|---------|-----------|--------------|-----------|-------------|
| Discord      | Yes     | Pairing   | Allowlist    | Off       | Octo        |
| Telegram     | Yes     | Pairing   | Open         | Off       | Octo        |

## How Channels Connect Users to Agents

Channels act as the interface through which users interact with agents. Each channel is configured with specific policies:

- **DM Policy**: Determines how direct messages are handled. For example, "pairing" requires users to be paired with an agent for direct communication.
- **Group Policy**: Defines how group interactions are managed. Policies such as "allowlist" or "open" control access.
- **Streaming**: Indicates whether real-time streaming is enabled on the channel.

Agents are bound to channels, ensuring that user interactions on a specific channel are routed to the appropriate agent. For instance, both Discord and Telegram channels are bound to the Octo agent, enabling it to handle user interactions on these platforms.
