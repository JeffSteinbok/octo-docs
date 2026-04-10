---
layout: default
title: Agents & Channels
nav_order: 2
---

# agents-channels

## Overview

This page describes the agents and channels configured in the system. Agents are specialized entities with distinct roles and permissions, while channels provide the interface through which users interact with agents. The configuration determines how agents are secured, what capabilities they have, and how they are bound to communication channels.

## Key Concepts

- **Agents**: Entities with specific roles, permissions, and access to tools or plugins.
- **Channels**: Communication interfaces (such as Discord and Telegram) that connect users to agents.
- **Bindings**: Associations between agents and channels, enabling user interaction.
- **Security Model**: Defines agent permissions, exec settings, and accessible tools/plugins.
- **Channel Policies**: Rules governing direct messages and group access.

## How It Works

1. Agents are configured with unique identifiers, names, emojis, permissions, and exec settings.
2. Channels are set up with types, enabled status, and policies for direct messages and group access.
3. Each channel binds to one or more agents, allowing users to interact with agents through the channel.
4. Security models for agents specify whether exec is enabled, what permissions are granted, and which tools or plugins are accessible.
5. Users connect to agents via channels, subject to channel policies and agent permissions.

## 🐙 Octo

- **Agent ID**: main
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified
- **Channel Bindings**: Not specified

## 📧 mail-agent

- **Agent ID**: mail
- **Status**: Currently unused
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified
- **Channel Bindings**: Not specified

## 🔑 Root

- **Agent ID**: root
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified
- **Channel Bindings**: Not specified

## 👨‍👩‍👧‍👦 Family

- **Agent ID**: family
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified
- **Channel Bindings**: Not specified

## 📷 HA Hooks

- **Agent ID**: hass-hooks
- **Security Model**:
  - Exec: Not specified
  - Permissions: Not specified
  - Tools/Plugins: Not specified
- **Channel Bindings**: Not specified

## Channels

| Type     | Enabled | DM Policy | Group Policy | Streaming Mode | Bound Agents |
|----------|---------|-----------|--------------|---------------|--------------|
| Discord  | Yes     | pairing   | allowlist    | off           | Not specified |
| Telegram | No      | pairing   | allowlist    | off           | Not specified |

- Channels connect users to agents, subject to channel policies.
- Discord channel is enabled; Telegram channel is currently disabled.
- DM policy is set to "pairing" and group policy to "allowlist" for both channels.
- Streaming mode is off for all channels.
