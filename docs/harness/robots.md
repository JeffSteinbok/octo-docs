---
layout: default
title: Robots
parent: Engineering Harness
nav_order: 4
---

# Robots

Octo is one assistant persona with one owner and three bodies. Each body runs in a different environment.

| Body | Runtime and role |
|---|---|
| **Octo·Claw** | OpenClaw runs the day-to-day assistant. Its agents, plugins and configuration live under `agents/`, `plugins/` and `config/`. |
| **Octo·Orca** | Orca-Octo is an [Orca](https://github.com/stablyai/orca) bot that handles engineering for Octo. Its setup is backed up in this repo under `robots/orca/`. |
| **Octo·Dot** | ChatGPT uses the Connect Octo skill to reach Claw through the MCP bridge as a paired client. See the [ChatGPT Connector](../mcp-chatgpt). |

Steward is a separate persona that maintains open-source repositories.

## Orca-Octo

Orca-Octo takes Octo issues from triage through deployment. It dispatches implementation workers, arranges independent reviews, makes configuration changes in health-checked steps, and maintains the docs. The owner approves changes and authorizes any administrative action. Orca-Octo works through a GitHub bot account. Claw and Orca currently share that account. Dedicated GitHub identities for each robot are planned.

## Guarded handoff

The guarded handoff between Orca and OpenClaw is live.

- **Orca to Claw.** A dedicated session accepts read-only handoffs.
- **Claw to Orca.** The `orca-send` channel carries status updates and questions only.

## Trust model

Only the owner can approve, through an owner-authenticated channel or a GitHub approval label verified as applied by the owner. Messages from Octo and other robots are requests, never approvals. Display names, sender labels and shared accounts provide context. Approval requires verified owner attribution. A local process has the authority of its configured access on that machine. See the [Security Model](../security-model) for the enforced boundaries.

## Adding a robot

1. Choose its persona, body name and repo home.
2. Assign a dedicated GitHub identity, record stable routing addresses in private configuration, and define the robot's permitted actions and approval boundaries.
3. Back up its setup, define a health check, and add it to the docs.
