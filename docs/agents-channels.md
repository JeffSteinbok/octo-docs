---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This system is configured with multiple agents and channels to facilitate communication and automation. Agents are specialized entities with distinct roles and permissions, while channels connect users to these agents through supported platforms. The configuration defines how agents operate, their security models, and how channels bind users to agents.

## Key Concepts

- **Agents**: Entities with specific roles, permissions, and access to tools or plugins.
- **Channels**: Communication interfaces (such as Discord) that connect users to agents.
- **Bindings**: Associations between channels and agents, determining which agents are accessible through each channel.
- **Security Model**: Each agent has defined permissions and exec settings.
- **Permissions and Exec Settings**: Control what actions agents can perform and which tools/plugins they can access.

## How It Works

1. Agents are configured with unique identifiers, names, emojis, permissions, exec settings, and access to tools/plugins.
2. Channels are set up with specific types (e.g., Discord), enabled status, policies for direct messages and groups, and streaming modes.
3. Channels bind users to agents, allowing communication and interaction according to channel policies.
4. Permissions and exec settings for each agent determine their capabilities and security boundaries.
5. The mail agent is currently unused and does not participate in channel bindings.

## 🐙 Octo

- **Agent ID**: main
- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins access: Not specified

## 📧 mail-agent

- **Agent ID**: mail
- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins access: Not specified
- **Note**: This agent is currently unused.

## 🔑 Root

- **Agent ID**: root
- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins access: Not specified

## 👨‍👩‍👧‍👦 Family

- **Agent ID**: family
- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins access: Not specified

## 📷 HA Hooks

- **Agent ID**: hass-hooks
- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins access: Not specified

## Channels

| Type     | Enabled | DM Policy | Group Policy | Streaming Mode | Bound Agents |
|----------|---------|-----------|--------------|---------------|--------------|
| Discord  | Yes     | pairing   | allowlist    | off           | All agents except mail-agent (mail-agent is unused) |
| Telegram | No      | pairing   | allowlist    | off           | None (channel disabled) |

- **Discord**: Enabled and connects users to agents with pairing DM policy and allowlist group policy. Streaming mode is off.
- **Telegram**: Disabled and does not connect users to any agents.

## How Channels Connect Users to Agents

Channels serve as the interface between users and agents. When a channel is enabled, it allows users to interact with agents according to the channel's policies. The Discord channel is active and binds users to all configured agents except the unused mail-agent. The Telegram channel is currently disabled and does not provide access to any agents.
