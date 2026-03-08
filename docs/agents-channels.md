---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents and Channels

## Overview

Agents and channels are core components of the system that enable communication between users and automated services. Agents represent specific roles or functionalities, while channels define the communication platforms through which users interact with these agents. This system allows for flexible configuration of agents and channels to suit various use cases.

## Key Concepts

- **Agents**: Represent distinct roles or functionalities, each with a unique identifier and configuration.
- **Channels**: Define the communication platforms (e.g., Discord, Telegram) through which users interact with agents.
- **Bindings**: Specify which agents are accessible through which channels.
- **Policies**: Define how direct messages (DMs) and group interactions are handled on each channel.

## How It Works

1. **Agent Configuration**: Agents are defined with unique identifiers, names, and optional metadata such as emojis. Each agent can be configured with specific permissions and execution settings.
2. **Channel Configuration**: Channels are set up to enable communication on specific platforms. Each channel has a type (e.g., Discord, Telegram) and associated policies for handling direct messages and group interactions.
3. **Binding Agents to Channels**: Agents are bound to specific channels, enabling users to interact with the agents through those platforms.
4. **User Interaction**: Users connect to the system via the configured channels. Based on the channel's policies and bindings, users can interact with the appropriate agents.

## Agents

| ID    | Name       | Emoji |
|-------|------------|-------|
| main  | Octo       | 🐙    |
| mail  | mail-agent | 📬    |
| root  | Root       | 🔑    |

### Agent Configuration

- **Permissions**: Each agent can be configured with specific permissions to control its access and capabilities.
- **Execution Settings**: Agents can be customized with execution settings to define their behavior and operational parameters.
- **Bindings**: Agents are associated with specific channels to determine where they are accessible.

## Channels

| Type      | Enabled | DM Policy | Group Policy | Streaming |
|-----------|---------|-----------|--------------|-----------|
| Discord   | true    | pairing   | allowlist    | off       |
| Telegram  | true    | pairing   | open         | off       |

### Channel Details

- **Discord**: Supports direct messages with a pairing policy and group interactions with an allowlist policy. Streaming is disabled.
- **Telegram**: Supports direct messages with a pairing policy and group interactions with an open policy. Streaming is disabled.

### Channel-User Interaction

Channels serve as the interface between users and agents. Depending on the channel's configuration:
- Users can initiate direct messages with agents based on the channel's DM policy.
- Group interactions are governed by the channel's group policy, which determines whether all users or only specific users can interact with agents in group settings.
