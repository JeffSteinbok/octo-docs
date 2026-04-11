---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This system is configured with multiple agents and channels to facilitate communication between users and automated agents. Agents are specialized entities with distinct roles and permissions, while channels serve as the interface connecting users to these agents. The configuration defines how agents are set up, their security models, and how channels bind users to agents.

## Key Concepts

- **Agents**: Automated entities with specific roles, permissions, and access to tools or plugins.
- **Channels**: Communication interfaces (such as Discord or Telegram) that connect users to agents.
- **Bindings**: Associations between channels and agents, determining which agents are accessible via each channel.
- **Security Model**: Each agent has defined permissions, exec settings, and access to tools/plugins.
- **Channel Policies**: Channels enforce policies for direct messages and group interactions.

## How It Works

1. **Agent Configuration**: Each agent is defined with a unique identifier, name, emoji, and security settings including permissions and exec capabilities.
2. **Channel Setup**: Channels are configured with type, enabled status, and policies for direct messages and group access.
3. **Binding Agents to Channels**: Channels are bound to agents, allowing users to interact with specific agents through the channel interface.
4. **User Interaction**: Users connect to agents via channels, subject to channel policies and agent permissions.

---

## 🐙 Octo

- **Agent ID**: main
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified

## 📧 mail-agent

- **Agent ID**: mail
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified
- **Note**: This agent is currently unused.

## 🔑 Root

- **Agent ID**: root
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified

## 👨‍👩‍👧‍👦 Family

- **Agent ID**: family
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified

## 📷 HA Hooks

- **Agent ID**: hass-hooks
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified

---

## Channels

| Channel Type | Enabled | DM Policy | Group Policy | Streaming Mode | Bound Agents |
|--------------|---------|-----------|--------------|---------------|--------------|
| Discord      | true    | pairing   | allowlist    | off           | All agents   |
| Telegram     | false   | pairing   | allowlist    | off           | All agents   |

- **Discord**: Enabled and connects users to all configured agents. Direct messages require pairing, and group access is managed via an allowlist. Streaming is disabled.
- **Telegram**: Currently disabled. When enabled, it would connect users to all agents with similar policies as Discord.

---

## How Channels Connect Users to Agents

Channels serve as the entry point for users to interact with agents. Each channel enforces policies for direct messages and group interactions, ensuring secure and controlled access to agents. When a user connects via a channel, they are routed to the appropriate agent based on channel bindings and policies.
