---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This system connects users to agents through configurable channels. Agents are specialized entities with distinct permissions and capabilities, while channels serve as the interface between users and agents. The configuration determines which agents are available, their security models, and how users interact with them via channels.

## Key Concepts

- **Agents:** Entities that perform tasks, each with specific permissions and access controls.
- **Channels:** Communication interfaces (such as Discord) that connect users to agents.
- **Permissions:** Define what actions agents can perform, including access to plugins and exec capabilities.
- **Bindings:** Channels are configured to connect users to specific agents.
- **Security Model:** Each agent has defined permissions and exec settings.

## How It Works

1. **Agent Configuration:** Agents are defined with unique IDs, names, and emojis. Each agent is assigned a security model specifying permissions, exec settings, and accessible tools or plugins.
2. **Channel Setup:** Channels are configured by type (e.g., Discord), enabled status, and policies for direct messages and group interactions.
3. **Binding Agents to Channels:** Channels connect users to agents based on the configuration, allowing interactions according to the channel's policies.
4. **User Interaction:** Users communicate with agents through enabled channels. The channel's policies determine how users are paired with agents and which agents are accessible in group contexts.

## 🐙 Octo

- **Security Model:** Exec is enabled. Octo has permissions to access tools and plugins as configured.
- **Permissions:** Octo can perform actions as allowed by its configuration.
- **Channel Access:** Available through enabled channels.

## 📧 mail-agent

- **Security Model:** Currently unused.
- **Permissions:** Not active in any channel.
- **Channel Access:** Not connected to any channel.

## 🔑 Root

- **Security Model:** Exec is enabled. Root has elevated permissions and access to tools/plugins.
- **Permissions:** Root can perform privileged actions as allowed by its configuration.
- **Channel Access:** Available through enabled channels.

## 👨‍👩‍👧‍👦 Family

- **Security Model:** Exec is enabled. Family agent has permissions to access tools/plugins.
- **Permissions:** Family can perform actions as allowed by its configuration.
- **Channel Access:** Available through enabled channels.

## 📷 HA Hooks

- **Security Model:** Exec is enabled. HA Hooks agent has permissions to access tools/plugins.
- **Permissions:** HA Hooks can perform actions as allowed by its configuration.
- **Channel Access:** Available through enabled channels.

## Channels

| Channel Type | Enabled | DM Policy  | Group Policy | Streaming Mode | Bound Agents           |
|--------------|---------|------------|--------------|---------------|------------------------|
| Discord      | Yes     | Pairing    | Allowlist    | Off           | Octo, Root, Family, HA Hooks |
| Telegram     | No      | Pairing    | Allowlist    | Off           | Octo, Root, Family, HA Hooks |

- **Discord Channel:** Enabled. Connects users to Octo, Root, Family, and HA Hooks agents. Direct messages use a pairing policy; group interactions use an allowlist policy. Streaming is off.
- **Telegram Channel:** Disabled. Not currently connecting users to any agents.

## How Channels Connect Users to Agents

Channels serve as the bridge between users and agents. When a channel is enabled, users can interact with agents according to the channel's policies. Direct messages are managed by a pairing policy, while group interactions are governed by an allowlist. Only agents bound to enabled channels are accessible to users.
