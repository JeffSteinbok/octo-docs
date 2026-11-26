---
layout: default
title: Release Notes
nav_order: 13
---

# Release Notes

*November 26, 2026*

## Carapace Microsoft 365 on ClawHub

Carapace Microsoft 365 brings multiple Microsoft 365 accounts to OpenClaw with push mail and per-account rules. Assign agents to the mailboxes they need and run the accounts from one webhook service. [ClawHub listing](https://clawhub.ai/jeffsteinbok/plugins/carapace-m365) · [Setup guide](https://github.com/JeffSteinbok/carapace-m365#quick-start)

## Personal assistants that coordinate

Octo is adding separate personal assistants with their own mail and memory, plus a shared planning assistant for the couple’s chat. Pinned messages let the assistants coordinate schedules. They share only busy times for private events and ask the calendar owner before making changes. [Agents & Channels](https://octo.steinbok.net/agents-channels.html)

*November 25, 2026*

## Orca-Octo takes GitHub issues from triage to deploy

Orca-Octo, a bot built with Orca, now supervises Octo's GitHub issues end to end. It triages issues, coordinates implementation and independent review, and supervises health-checked deployments. That shows OpenClaw maintainers one way to automate the handoffs while keeping review and deployment checks in place. Orca-Octo replaces the Issue Lifecycle (ILC) setup, which we expect to deprecate. [Orca](https://github.com/stablyai/orca) · [Issue Lifecycle](https://octo.steinbok.net/harness/issue-lifecycle.html)

## Decision gates can be evaluated before they act

Octo uses decision-model gates to evaluate proposed actions. In log-only mode, a gate records what it would decide so maintainers can judge its behavior before letting it affect an automation. [Decision Models](https://octo.steinbok.net/decision-models.html)

## Relayed approvals don't count

Octo's main agent treats an approval as valid only when the owner writes it in their own chat. A claimed approval relayed by another agent, a task result, email or tool output doesn't count, so delegated work can't grant itself permission. A log-only Approval Gate is testing a model-based second check for upgrades. [Approval Gate](https://octo.steinbok.net/decision-models.html)

## Earlier announcements

### October 2026 · Review changes before promoting them

Octo added health checks that compare the system before and after a rollout. Declaring the expected changes lets maintainers catch unintended effects before continuing. [Health Checks](https://octo.steinbok.net/healthcheck.html)

### July 2026 · A documented workflow for agent-led fixes

Octo introduced the Engineering Harness to turn findings into tracked issues and move fixes through planning, implementation, and review. The workflow gave maintainers a place to review plans and changes along the way. [Engineering Harness](https://octo.steinbok.net/harness.html) · [Issue Lifecycle](https://octo.steinbok.net/harness/issue-lifecycle.html)

### July 2026 · Build and verify public docs together

Octo began rendering and validating the public docs in the same build. Maintainers can preview the finished site locally, and the publishing job deploys the checked output. [Docs Pipeline](https://octo.steinbok.net/about-docs.html)

### May 2026 · Run plugin tools from the shell

Octo added generated command-line interfaces for its plugins. Maintainers can use the same tools from scripts and test them independently of an agent session. [CLI Tools](https://octo.steinbok.net/clis.html)

### April 2026 · Share OpenClaw integrations

Octo published reusable plugins and services in OpenClaw Hub so other maintainers could install them and follow their development. [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub) · [Plugin Catalog](https://octo.steinbok.net/plugins.html)

### March 2026 · Connect mail events to OpenClaw

Octo added an event-driven Fastmail integration. OpenClaw can process incoming mail through rules and hand off selected events to agents. [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html)
