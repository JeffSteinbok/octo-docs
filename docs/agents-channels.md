# Agents and Channels

## Overview

Agents and channels are core components of the system that enable communication between users and automated services. Agents represent distinct personas or roles that interact with users, while channels define the platforms through which these interactions occur. This configuration allows for flexible communication setups tailored to different use cases.

## Key Concepts

- **Agents**: Represent distinct roles or personas that interact with users.
- **Channels**: Define the platforms (e.g., Discord, Telegram) through which users communicate with agents.
- **Bindings**: Channels are configured to connect specific agents to users.
- **Policies**: Channels have configurable policies for direct messages (DMs) and group interactions.

## How It Works

1. **Agents** are configured with unique identifiers, names, and optional emojis to represent their personas.
2. **Channels** are configured to enable communication on specific platforms. Each channel has policies governing direct messages and group interactions.
3. Users interact with agents through the configured channels. The system ensures that the appropriate agent responds based on the channel and policies.

## Agents

The following agents are configured in the system:

| ID    | Name       | Emoji  | Description                                   |
|-------|------------|--------|-----------------------------------------------|
| main  | Octo       | 🐙     | Represents the primary agent for interactions. |
| mail  | mail-agent | 📬     | Handles mail-related interactions.            |
| root  | Root       | 🔑     | A root-level agent for administrative tasks.  |

## Channels

The following channels are configured to connect users to agents:

| Type      | Enabled | DM Policy | Group Policy | Streaming | Description                                                                 |
|-----------|---------|-----------|--------------|-----------|-----------------------------------------------------------------------------|
| Discord   | Yes     | Pairing   | Allowlist    | Off       | Enables communication via Discord with pairing-based DM policy and allowlist-based group policy. |
| Telegram  | Yes     | Pairing   | Open         | Off       | Enables communication via Telegram with pairing-based DM policy and open group policy. |

### Channel Policies

- **DM Policy**: Determines how direct messages are handled. For example, "pairing" requires a user-agent pairing to initiate communication.
- **Group Policy**: Governs group interactions. "Allowlist" restricts group communication to approved users, while "open" allows unrestricted group interactions.

### Channel-Agent Bindings

Channels are configured to connect users to the appropriate agents based on the platform and policies. Each channel ensures that users can interact with the agents seamlessly while adhering to the defined policies.
