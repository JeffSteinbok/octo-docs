---
layout: default
title: GitHub Issues
nav_order: 1
nav_exclude: true
---

# 🪝 GitHub Issues

Moving an issue in the `octo` repo to the next stage of the [issue lifecycle](../harness/issue-lifecycle) (by adding a label on GitHub) starts the `coding` agent on that stage: writing a plan, implementing an approved plan, or reworking a pull request. Nothing starts until the owner adds one of these labels, and the owner always merges.

The `coding` agent is Octo's coding specialist; it also works with the owner in the `#coding` channel on Discord.

## How an event gets here

1. GitHub sends the issue event to `https://<funnel-host>/hooksproxy/github-issues` through Tailscale Funnel, signed with an HMAC-SHA256 signature (`X-Hub-Signature-256`).
2. The [Webhook Proxy](../services/webhook-proxy) checks the signature, drops events from senders other than the owner's accounts and events that aren't one of the lifecycle labels, and forwards the rest to the Gateway's `/hooks/github-issues` endpoint with OpenClaw's hooks token added.
3. A transform on the Gateway checks the sender and label again, logs what it kept or dropped, and passes on only `labeled` events for the labels below.
4. OpenClaw starts a turn for the `coding` agent in a session for that issue and label, and delivers the agent's reply to the owner.

## Labels that start work

| Label | Added by | What the agent does |
|-------|----------|---------------------|
| `ilc:approved` | Owner | Writes an implementation plan and posts it on the issue |
| `ilc:plan-approved` | Owner | Hands the approved plan to Claude Code (the `claude` agent, over ACP), which implements it; the change then goes up as a pull request for the owner to review |
| `ilc:pr-needs-work` | Owner | Goes back to implementation to address the review |

The full set of `ilc:` labels and the state machine are on the [Issue Lifecycle](../harness/issue-lifecycle) page.

## At a glance

- **Endpoint:** `/hooksproxy/github-issues`
- **Agent:** `coding` (see [Agents & Channels](../agents-channels))
