---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

This system connects users to agents through configurable channels. Agents are specialized entities with distinct permissions and access models, while channels provide the interface for user communication. The configuration defines which agents are available, their security settings, and how channels bind users to agents.

## Key Concepts

- **Agents**: Individual entities with specific roles, permissions, and access to tools or plugins.
- **Channels**: Communication interfaces (such as Discord) that connect users to agents.
- **Bindings**: Associations between channels and agents, determining which agents are accessible through each channel.
- **Security Model**: Each agent has defined permissions and exec settings controlling its capabilities.

## How It Works

1. Agents are configured with unique identifiers, names, emojis, permissions, and exec settings.
2. Channels are set up with types (e.g., Discord), enabled status, and policies for direct messages and group access.
3. Channels bind users to agents, allowing communication according to the channel's policies.
4. Security models for agents determine their access to tools, plugins, and exec capabilities.
5. Users interact with agents via enabled channels, subject to channel policies and agent permissions.

## 🐙 Octo

- **Agent ID**: main
- **Security Model**: Exec is enabled. Octo has permissions to access tools and plugins as configured.
- **Bindings**: Available through enabled channels.

## 📧 mail-agent

- **Agent ID**: mail
- **Security Model**: Permissions and exec settings are configured, but this agent is currently unused.
- **Bindings**: Not actively connected to any channel.

## 🔑 Root

- **Agent ID**: root
- **Security Model**: Exec is enabled. Root has elevated permissions and access to tools/plugins.
- **Bindings**: Available through enabled channels.

## 👨‍👩‍👧‍👦 Family

- **Agent ID**: family
- **Security Model**: Exec is enabled. Family agent has permissions to access tools/plugins as configured.
- **Bindings**: Available through enabled channels.

## 📷 HA Hooks

- **Agent ID**: hass-hooks
- **Security Model**: Exec is enabled. HA Hooks agent has permissions to access tools/plugins.
- **Bindings**: Available through enabled channels.

## Channels

| Type     | Enabled | DM Policy | Group Policy | Streaming Mode | Bound Agents            |
|----------|---------|-----------|--------------|---------------|-------------------------|
| Discord  | Yes     | pairing   | allowlist    | off           | Octo, Root, Family, HA Hooks |
| Telegram | No      | pairing   | allowlist    | off           | Octo, Root, Family, HA Hooks |

- **Discord**: The primary enabled channel. Connects users to agents according to pairing and allowlist policies.
- **Telegram**: Currently disabled.

Channels connect users to agents by enforcing direct message and group access policies. Only enabled channels allow user interaction with agents. The mail-agent is not currently bound to any channel.
