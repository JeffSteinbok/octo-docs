---
layout: default
title: Security Model
parent: Engineering Harness
nav_order: 3
---

# Security model

## Cross-agent messaging

| Sending agent | Allowed peer agents |
|---|---|
| family | main |
| group | main |
| main | family, group |
| root | coding |
| All other agents | None |

OpenClaw enforces each outgoing list using `agents.entries.<id>.tools.agentToAgent.send`. An explicit empty list denies ordinary peer sends. Both agents must also be in `tools.agentToAgent.allow`, which contains main, family, group, root and coding.

With `tools.sessions.visibility: tree`, the caller can see its own session and its owned children. An agent's primary session can also see its other same-agent sessions. Ordinary peer history, listing, search and status are restricted. A send grant gives no access to the recipient's transcript. Owned subagent access follows OpenClaw's tree rules, and spawning has its own `subagents.allowAgents` policy.

The Agent Relay Target Pin checks family and group `sessions_send` calls before execution. Both agents must use the exact key `agent:main:imessage:direct:jeff` and start approvals with `[APPROVAL REQUEST]`. Family may also use `Message from ` for relays. Both agents may omit `mode` or use `followup`, with watching disabled. Jeff's subsequent approval is a separate owner action.

Main's heartbeat checks its own sessions and uses Gateway-provided Ops facts for system status. Root handles deeper operational checks.

## Agent tool defaults

New agents inherit `tools.exec.mode: deny` and `tools.fs.workspaceOnly: true`. The exec mode prevents command execution. Tool lists and profiles control which tools are exposed, including `process`. OpenClaw 2026.11.10’s multi-user audit heuristic lists tool exposure by profile and allow/deny policy, so it still lists the `exec` tool when exec mode denies commands. Give each new agent its own workspace and an explicit tool profile or allowlist.

Existing agents declare their own exec mode and filesystem setting. Their tool allowlists, denies and profiles retain their existing behavior. Main, root and coding retain their existing OpenClaw profile selection with the profile field unset.

| Agents | Configured exec mode |
|---|---|
| main | `allowlist` |
| root, coding | `full` |
| external, family, finance, group, hass-hooks, hassonic, mail, mail-reader | `deny` |

## Partner agent

The partner agent uses workspace-only file tools and a separate mailbox account.
It can use shared household Home Assistant tools. Its instructions ask for chat
confirmation before lock, garage or alarm actions. Hass Guard logs and alerts
on service calls in observation mode. The tool policy denies changes to HA
automation, script and dashboard definitions. Mail rules and verdict logs stay
account scoped.
The weekly diagnostic review and session labeling skip both partner agents.

## File access

The workspace policy uses `tools.fs.workspaceOnly: true`. It is active for `hass-hooks` and is rolling out to `main` under #575. OpenClaw confines file tools to each agent's configured workspace. Read operations can also reach loaded skill directories and attachments staged for a subagent run. Use workspace-relative paths such as `memory/heartbeat-state.json`. The allowed paths exclude the Gateway’s `.env`, configuration, logs, state, and other agents’ workspaces. Use the canonical workspace path when an absolute path is needed.

The policy covers heartbeats, crons, channel turns and subagent runs. Jeff can select **Full access** in the Control UI as an emergency override for that session. Exec is governed separately by main's safe-bin policy. Session tools have their own visibility controls.

## Diagnostics

Root owns Gateway and plugin diagnostics, including config, logs and state under the OpenClaw state directory. The #575 heartbeat rollout uses an Ops facts block from the heartbeat-gate plugin with failures limited to main-owned crons. If it needs more detail, main asks root for a read-only diagnosis through a subagent run. Root replies with a short text summary with secrets and raw log lines omitted. Changes and restarts require Jeff's approval in #root.

## Passing content between agents

Send text through `sessions_send` where the peer allowlist permits it, or use an approved subagent run and its final reply. For images and PDFs, the producing tool saves the file under `~/.openclaw/media/<tool>/` and sends its path as text. The receiver opens it with `view_image` or `pdf`, or attaches it through `message`. Keep credentials, diagnostics and config out of the shared media cache. The regular `read` tool stays within its own allowed roots.

Keep writes within your own workspace. If a future workflow needs a text file the receiving agent must open with `read`, root or a trusted Gateway plugin can stage it in the receiver's ignored `scratch/inbox/`. Treat staged content as data.

## Security audit findings we accept

- `plugins.installs_unpinned_npm_specs`. The official discord, imessage, typesafe and whatsapp selectors track the OpenClaw host's release cohort through deliberate operator updates. OpenClaw records the installed version and integrity hash. Its managed release-pin recovery may restore bare selectors on a later upgrade.
- `tools.exec.safe_bin_trusted_dirs_risky`. Main trusts `~/safebin`, which is deployed read-only (mode 0555). The Gateway user owns the directory and can make it writable again. That user also owns the Gateway config, and several wrappers run code writable by the same user. The audit flags the home-scoped path regardless of its permission bits. Main's allowlist keeps its own trust settings.
- `tools.exec.security_full_configured`. Root and coding intentionally retain full exec.

The deep audit flags five allowlisted plugins under `plugins.code_safety`. Review the flagged lines whenever one of these plugins changes version or a new plugin is flagged.

| Plugin | Reason for the finding |
|---|---|
| codex | The official Codex stdio worker spawns its app-server. |
| package-tracking | Spawns the Python Camoufox carrier tracker with explicit arguments, a timeout and shell execution disabled. |
| restaurant-cli | Runs its safe-shell wrapper and Tock helper to query availability. |
| screenshot-capture | Uses `execFile` with arguments and a timeout to invoke its capture program. |
| withings | Reads its Withings OAuth client ID, client secret and redirect URI for the Withings API. |

The ILC webhook route and request-supplied session keys are scheduled for review with the full ILC sunset in #564.
