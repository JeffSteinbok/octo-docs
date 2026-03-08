---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components that enable communication and interaction within the system. Agents represent distinct entities or roles that perform specific tasks, while channels define the mediums through which users can interact with these agents. Together, they provide a flexible framework for managing user interactions across different platforms.

## Key Concepts

- **Agents**: Entities configured to perform specific roles, each with unique identifiers and attributes.
- **Channels**: Communication mediums (e.g., Discord, Telegram) that connect users to agents.
- **Agent Configuration**: Includes permissions, execution settings, and bindings to channels.
- **Channel Policies**: Define how direct messages (DMs) and group interactions are handled.

## How It Works

1. **Agent Configuration**:  
   Agents are defined with unique identifiers, names, and optional attributes (e.g., emoji). These agents are configured to perform specific roles and can be bound to one or more channels.

2. **Channel Configuration**:  
   Channels are set up to enable communication between users and agents. Each channel is configured with a type (e.g., Discord, Telegram), policies for direct messages and group interactions, and streaming settings.

3. **Connecting Users to Agents**:  
   Channels serve as the interface through which users interact with agents. Policies such as DM pairing and group allowlists determine how users can engage with agents in different contexts.

## Agents

| ID    | Name        | Emoji |
|-------|-------------|-------|
| main  | Octo        | 🐙    |
| mail  | mail-agent  | 📬    |
| root  | Root        | 🔑    |

## Channels

| Type      | Enabled | DM Policy | Group Policy | Streaming |
|-----------|---------|-----------|--------------|-----------|
| Discord   | Yes     | Pairing   | Allowlist    | Off       |
| Telegram  | Yes     | Pairing   | Open         | Off       |
