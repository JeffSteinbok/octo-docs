---
layout: default
title: Agents & Channels
nav_order: 2
---

# agents-channels

## Overview

This page describes the agents and channels configured in the system. Agents are specialized entities with distinct roles, permissions, and security models. Channels serve as communication pathways, connecting users to agents and facilitating interactions. The configuration determines which agents are available, their permissions, and how users can access them through various channels.

## Key Concepts

- **Agents**: Entities with specific roles, permissions, and access to tools or plugins.
- **Channels**: Communication interfaces (such as Discord) that connect users to agents.
- **Agent Security Model**: Defines exec settings, permissions, and accessible tools/plugins for each agent.
- **Bindings**: Associations between channels and agents, determining which agents are accessible via each channel.
- **Channel Policies**: Rules governing direct messages and group interactions.

## How It Works

1. Agents are configured with unique identifiers, names, emojis, and security models, including exec settings and permissions.
2. Channels are set up with types (e.g., Discord), enabled status, and policies for direct messages and group interactions.
3. Each channel binds to specific agents, allowing users to interact with those agents through the channel.
4. Channel policies define how users can connect to agents, including pairing for direct messages and allowlist for group access.
5. Users communicate with agents via enabled channels, following the channel's policies and the agent's permissions.

## 🐙 Octo

- **Security Model**: Exec is enabled. Octo has permissions to access tools and plugins as configured.
- **Permissions**: Full access to tools/plugins as defined in the system configuration.
- **Bindings**: Available through enabled channels.

## 📧 mail-agent

- **Security Model**: Currently unused.
- **Permissions**: Not active; no permissions granted.
- **Bindings**: Not bound to any channel.

## 🔑 Root

- **Security Model**: Exec is enabled. Root has elevated permissions.
- **Permissions**: Access to tools/plugins with higher privileges.
- **Bindings**: Available through enabled channels.

## 👨‍👩‍👧‍👦 Family

- **Security Model**: Exec is enabled. Family agent has permissions suitable for family-related tasks.
- **Permissions**: Access to tools/plugins as configured for family use.
- **Bindings**: Available through enabled channels.

## 📷 HA Hooks

- **Security Model**: Exec is enabled. HA Hooks agent has permissions for home automation hooks.
- **Permissions**: Access to tools/plugins related to home automation.
- **Bindings**: Available through enabled channels.

## Channels

| Channel Type | Enabled | DM Policy | Group Policy | Streaming Mode | Bound Agents |
|--------------|---------|-----------|--------------|---------------|--------------|
| Discord      | Yes     | Pairing   | Allowlist    | Off           | Octo, Root, Family, HA Hooks |
| Telegram     | No      | Pairing   | Allowlist    | Off           | None (disabled) |

- **Discord**: Connects users to Octo, Root, Family, and HA Hooks agents. Direct messages require pairing; group access is managed by an allowlist. Streaming is disabled.
- **Telegram**: Currently disabled; does not connect users to any agents.

## How Channels Connect Users to Agents

Channels act as bridges between users and agents. When a channel is enabled, users can interact with the agents bound to that channel, subject to the channel's policies for direct messages and group interactions. Disabled channels do not provide access to any agents.
