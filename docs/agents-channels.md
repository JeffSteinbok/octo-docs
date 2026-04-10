---
layout: default
title: Agents & Channels
nav_order: 2
---

# agents-channels

## Overview

This page describes the agents and channels configured in the system. Agents are specialized entities with distinct roles and permissions, while channels provide the interface through which users interact with agents. The configuration determines how agents are secured, what capabilities they have, and how channels connect users to them.

Agents are configured with specific permissions, exec settings, and bindings. Channels define the communication medium and policies for connecting users to agents.

## Key Concepts

- **Agents**: Entities with unique roles, permissions, and access to tools/plugins.
- **Channels**: Communication interfaces (such as Discord) that connect users to agents.
- **Permissions**: Define what actions agents can perform and which tools/plugins they can access.
- **Exec Settings**: Control whether agents can execute commands or scripts.
- **Bindings**: Specify which agents are accessible through each channel.
- **Channel Policies**: Determine how users are paired with agents and which groups are allowed.

## How It Works

1. Agents are configured with unique identifiers, names, emojis, permissions, exec settings, and tool/plugin access.
2. Channels are set up with a specific type (e.g., Discord), enabled status, and policies for direct messaging and group access.
3. Each channel binds to one or more agents, allowing users to interact with those agents through the channel.
4. Channel policies control user pairing and group allowlisting, determining who can access which agents.
5. Users connect to agents via channels, subject to the channel's policies and the agent's permissions.

## 🐙 Octo

- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins: Not specified

## 📧 mail-agent

- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins: Not specified
- **Note**: The mail agent is currently unused.

## 🔑 Root

- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins: Not specified

## 👨‍👩‍👧‍👦 Family

- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins: Not specified

## 📷 HA Hooks

- **Security Model**:
  - Exec enabled: Not specified
  - Permissions: Not specified
  - Tools/plugins: Not specified

## Channels

| Type     | Enabled | DM Policy | Group Policy | Streaming Mode | Bound Agents |
|----------|---------|-----------|--------------|---------------|--------------|
| Discord  | Yes     | Pairing   | Allowlist    | Off           | All agents   |
| Telegram | No      | Pairing   | Allowlist    | Off           | All agents   |

- **Discord**: Enabled. Connects users to all configured agents. Direct messaging uses pairing policy; group access is controlled by an allowlist. Streaming mode is off.
- **Telegram**: Disabled. Would connect users to all agents with pairing and allowlist policies if enabled.

Channels connect users to agents according to the channel's policies, enabling communication and interaction with the agents.
