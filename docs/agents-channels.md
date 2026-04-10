---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This page describes the agents and channels configured in the system. Agents are specialized entities with distinct roles and permissions, while channels provide communication pathways that connect users to agents. The configuration defines how agents are set up, their security models, and how channels bind to agents.

## Key Concepts

- **Agents**: Entities with specific roles, permissions, and access to tools or plugins.
- **Channels**: Communication interfaces (such as Discord or Telegram) that connect users to agents.
- **Bindings**: Associations between channels and agents, determining which agents are accessible through each channel.
- **Security Model**: Each agent's permissions, exec settings, and access to tools/plugins.
- **Channel Policies**: Rules governing direct messages and group interactions.

## How It Works

1. Agents are configured with unique identifiers, names, emojis, and security models.
2. Channels are set up with types, enabled status, and policies for direct messages and group access.
3. Channels bind users to agents, allowing communication according to channel policies.
4. Permissions and exec settings for each agent determine what actions they can perform and which tools/plugins they can access.
5. The mail agent is currently unused and not bound to any channel.

---

## 🐙 Octo

- **Agent ID**: `main`
- **Security Model**:
  - Exec: Enabled
  - Permissions: Standard operational permissions
  - Tools/Plugins: Access to configured tools and plugins

## 📧 mail-agent

- **Agent ID**: `mail`
- **Security Model**:
  - Exec: Disabled
  - Permissions: Restricted
  - Tools/Plugins: No access
- **Note**: This agent is currently unused.

## 🔑 Root

- **Agent ID**: `root`
- **Security Model**:
  - Exec: Enabled
  - Permissions: Elevated (administrative)
  - Tools/Plugins: Access to all tools and plugins

## 👨‍👩‍👧‍👦 Family

- **Agent ID**: `family`
- **Security Model**:
  - Exec: Enabled
  - Permissions: Family-specific operational permissions
  - Tools/Plugins: Access to family-related tools and plugins

## 📷 HA Hooks

- **Agent ID**: `hass-hooks`
- **Security Model**:
  - Exec: Enabled
  - Permissions: Home automation hooks
  - Tools/Plugins: Access to home automation plugins

---

## Channels

| Channel Type | Enabled | DM Policy  | Group Policy | Streaming Mode | Bound Agents         |
|--------------|---------|------------|--------------|---------------|----------------------|
| Discord      | Yes     | Pairing    | Allowlist    | Off           | Octo, Root, Family, HA Hooks |
| Telegram     | No      | Pairing    | Allowlist    | Off           | None                 |

- **Discord**: Connects users to Octo, Root, Family, and HA Hooks agents. Direct messages require pairing, and group access is managed by an allowlist. Streaming is disabled.
- **Telegram**: Currently disabled and not bound to any agents.

---

## Channel Bindings

- Channels connect users to agents based on channel policies and enabled status.
- Only enabled channels (such as Discord) allow users to interact with bound agents.
- The mail agent is not bound to any channel and is currently unused.
