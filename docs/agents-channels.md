---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents & Channels

Octo is made up of several agents. Each agent is a separate OpenClaw assistant with its own instructions, workspace and permissions, so a conversation or event only gets the tools its job needs. Channels are the messaging apps people use to reach those agents.

This page shows what each agent is for, a simplified view of its permissions, and why it is set up that way. Exact routing rules, file paths and detailed allowlists are left out.

For the AI models each agent uses, see [Models](models). Apps that connect to the Gateway as paired devices, such as Hassonic and OctoDot, are covered under [Connected Apps](connected-apps).

## The Agents

In the Permissions column, *allowed* and *denied* are set explicitly for that agent; anything not listed follows its tool profile.

| Agent | Used for | Permissions | Why it is set up this way |
|-------|----------|-------------|---------------------------|
| `main` | The owner's everyday assistant: direct chats and proactive check-ins | Custom tool set. Allowed: shell (`exec`). Can hand work to `root`, `family`, `finance`. | Keeps the everyday assistant capable while limiting its shell to approved commands only, with no arbitrary shell access. |
| `mail` | Mail processing handed off by other agents (currently unused) | Minimal tool profile. Allowed: file reads. Denied: shell (`exec`), browser, file writes. | Treats mail as untrusted input and keeps mail processing away from broader tools. |
| `root` | Admin and debugging work the owner explicitly escalates | Custom tool set. Allowed: file reads. Broad access, inherited from OpenClaw's defaults. | Keeps privileged admin and debugging access on a separate path that is used only on request. |
| `family` | Family members' iMessage DMs and the family group chat | Messaging tool profile. Denied: shell (`exec`), browser, file reads, file writes. | Gives family conversations a narrow, safer tool set. Calendar plugins apply per-person read and write rules based on who sent the message. |
| `finance` | Household finance and retirement planning | Minimal tool profile. Allowed: file reads, file writes. Denied: shell (`exec`), browser. | Keeps account data and planning notes away from everyday chat, with read-only finance tools. |
| `hass-hooks` | Home Assistant camera and doorbell events (see [Hooks](hooks)) | Named tools only. Allowed: file reads. Denied: shell (`exec`). Camera, image, messaging and skill tools, plus workspace-only read. Messaging can attach verified image, audio, video, PDF, and office files from OpenClaw’s temp directory, full media cache, and delivery-queue media directory. Attachment checks block `.env` files, secrets, and files in other agents’ workspaces. | Lets webhook automation inspect camera events and send notifications with saved camera images. |
| `coding` | Coding specialist in `#coding` on Discord, and GitHub issue work (see [Hooks](hooks)) | OpenClaw's default tools. | Gets the shell access coding work needs, kept away from everyday chat. |
| `hassonic` | Home control from the [Hassonic](hassonic) iPhone app | Named tools only. Denied: shell (`exec`). Home Assistant state, an allowlisted set of actions, and web search. | The app talks only to this agent, so a phone request can reach Home Assistant but nothing else. Every action is checked by the [Hass Guard](plugins/hass-guard) plugin. |
| `group` | Other iMessage group chats (replies only when mentioned) | Messaging tool profile. Denied: shell (`exec`), browser, file reads, file writes. | Group chats can include people outside the family, so this agent gets only messaging, web search and read access to the family calendar: no shell, files or browser. |
| `external` | Other assistants that use Octo through the [Octo MCP](mcp) server, such as OctoDot in ChatGPT | Named tools only. Denied: shell (`exec`). | Outside assistants get a deliberately small set of tools, and house changes still go through Hass Guard. |
| `mail-reader` | Published agent | Named tools only. Denied: browser. | Keeps this agent separate from the rest of the system. |
| `partner` | The owner's partner's personal assistant | Named tools only. Allowed: shell (`exec`), file reads, file writes. Can hand work to `finance`. | Keeps this agent separate from the rest of the system. |
| `partner-mail` | Summarizes incoming mail for the partner agent's mailbox | Named tools only. Denied: browser. | Keeps this agent separate from the rest of the system. |
| `couple` | Shared planning for the two-person group | Named tools only. Allowed: file reads, file writes. | Keeps this agent separate from the rest of the system. |

## How household assistants work together

The owner uses the main agent and the owner's partner uses the partner agent.
Each personal agent has its own mailbox, conversation history and memory.
The couple agent serves their two-person planning group. The family agent
handles family conversations, and the group agent handles other shared chats.

The owner's Microsoft 365 tools use the default account. The partner agent
and its background mail agent use the partner account through the plugin's
agent mapping. The partner's personal and shared family Outlook snapshots
are cached in its workspace. See [External Integrations](external-integrations#microsoft-365-accounts)
for account routing, scheduled refreshes and the pending plugin upgrade.

The two personal agents exchange messages through their pinned direct chats.
The couple agent can ask either personal agent through those same direct
chats. Replies to the couple agent go to its pinned group. These sends
leave personal transcripts private. Dedicated read-only tools give the
personal agents a view of the couple and family conversations, while
native session visibility stays scoped to each agent's own tree.

The personal agents can share normal calendar details, including times,
titles, locations and attendees. A private event appears only as a busy
interval. An ICS event without CLASS is public by default. Microsoft
calendar sharing uses the provider's own sensitivity field. For Microsoft
events with missing or unrecognized sensitivity, share only the busy
interval. If there is no workable time or a schedule is unclear, the relevant
personal assistant asks its owner directly before replying. A relayed
message from any agent never counts as approval to change a calendar.

The partner agent can create and manage its own automations. Jobs run as
that agent with a per-job tool list. It can send approved reminders directly
to the owner and delegate finance questions with the owner’s permission.
It can inspect images or PDFs in its workspace and manage its session goals. Shell
access is limited to public waitlist status checks. Administrative approval
stays with the owner.

### Shell Access

Shell access (the `exec` tool) is set per agent under `agents.entries.<id>.tools.exec` in OpenClaw's config:

- **`main`** uses `mode: allowlist`: it can run only the approved commands named in its `safeBins` list. Those commands live in `~/safebin/`; see [CLI Tools](clis).
- **`root`** uses `mode: full`: unrestricted shell access, for admin and debugging work the owner asks for.
- Agents with shell marked *denied* above can't run commands at all.

## Channels

Each channel has its own rules for who may message Octo:

- **DM policy** `pairing`: someone new gets a short code, and their messages are ignored until the owner approves it. `allowlist`: only listed senders get through.
- **Group policy** `allowlist`: Octo takes part only in listed group chats.
- **Streaming** `partial`: a reply appears as it is written. `off`: the reply is sent once it is complete.

| Channel | Enabled | DM Policy | Group Policy | Streaming |
|---------|---------|-----------|--------------|-----------|
| `discord` | Yes | pairing | allowlist | partial |
| `imessage` | Yes | allowlist | allowlist | — |
| `telegram` | Yes | pairing | allowlist | off |
| `whatsapp` | Yes | allowlist | allowlist | — |

## Session Settings

A session is one ongoing conversation with an agent, with its own history.

| Setting | Value | Meaning |
|---------|-------|---------|
| Scope | `per-channel-peer` | Each person gets a separate conversation on each channel. |
| Reset | `idle` | A new conversation starts after a period without messages. |
