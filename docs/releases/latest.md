---
layout: default
title: Release Notes
nav_order: 13
---

# Release Notes

## 2026-11-26

- **Carapace Microsoft 365 on ClawHub.** Carapace Microsoft 365 brings multiple Microsoft 365 accounts to OpenClaw with push mail and per-account rules. Assign agents to the mailboxes they need and run the accounts from one webhook service. [ClawHub listing](https://clawhub.ai/jeffsteinbok/plugins/carapace-m365) · [Setup guide](https://github.com/JeffSteinbok/carapace-m365#quick-start)
- **Personal assistants that coordinate.** Octo is preparing separate personal assistants with their own mail and memory, plus a shared planning assistant. The planned scheduling workflow uses pinned messages, shares only busy times for private events, and sends uncertain requests to the calendar owner for confirmation. [Agents & Channels](https://octo.steinbok.net/agents-channels.html)

## 2026-11-25

- **Orca-Octo takes GitHub issues from triage to deploy.** Orca-Octo, a bot built with Orca, now supervises Octo's GitHub issues end to end. It triages issues, coordinates implementation and independent review, and supervises health-checked deployments. That shows OpenClaw maintainers one way to automate the handoffs while keeping review and deployment checks in place. Orca-Octo replaces the Issue Lifecycle (ILC) setup, which we expect to deprecate. [Orca](https://github.com/stablyai/orca) · [Issue Lifecycle](https://octo.steinbok.net/harness/issue-lifecycle.html)
- **Decision gates can be evaluated before they act.** Octo uses decision-model gates to evaluate proposed actions. In log-only mode, a gate records what it would decide so maintainers can judge its behavior before letting it affect an automation. [Decision Models](https://octo.steinbok.net/decision-models.html)
- **Approval Gate previews upgrade decisions.** The log-only Approval Gate tests a model-based second check for explicit owner approvals before it can affect upgrades. [Approval Gate](https://octo.steinbok.net/plugins/approval-gate.html)

## 2026-11-24

- **Image annotations for Home Assistant captures.** Agents can mark an object or area and return the annotated image so readers can see what the agent is referring to. [Plugin Catalog](https://octo.steinbok.net/plugins.html)
- **Direct owner approval.** Octo's main agent accepts approvals only when the owner gives them directly in their own chat. This keeps delegated work from granting itself permission. [Approval Gate](https://octo.steinbok.net/plugins/approval-gate.html)

## 2026-11-23

Octo prepared log-only gates for mail, requests, and approvals. Maintainers can review the proposed decisions before using them to control what an automation does. [Decision Models](https://octo.steinbok.net/decision-models.html)

## 2026-11-22

The unhandled-mail gate began sending a summary when an Outlook message that matched no existing rule was worth surfacing. This gives important messages a route through without forwarding every unmatched message. [Decision Models](https://octo.steinbok.net/decision-models.html)

## 2026-11-21

Octo restored decision checks for automated camera alerts and flagged silent gates in its decision review. Maintainers can check whether a gate is receiving events before relying on its recommendations. [Decision Models](https://octo.steinbok.net/decision-models.html)

## 2026-11-04

Octo started evaluating unmatched mail in log-only mode and expanded the heartbeat gate to consider failed plugin health checks. These changes let maintainers preview mail decisions and see more operational failures in heartbeat reviews. [Decision Models](https://octo.steinbok.net/decision-models.html)

## 2026-10-31

Octo enabled the Mail Notify Gate in log-only mode. It records whether a matched email would warrant a notification, giving maintainers examples to review while existing mail rules continue to run. [Mail Notify Gate](https://octo.steinbok.net/plugins/mail-notify-gate.html)

## 2026-10-30

Octo began using its camera alert gate to decide which events to forward after observing its decisions for a week. The gate helps reduce routine alerts. [Hass Alert Gate](https://octo.steinbok.net/plugins/hass-alert-gate.html)

## 2026-10-26

Octo added authenticated MCP access for other agents and health checks that compare the system before and after a rollout. Maintainers can declare expected changes and catch unintended effects before continuing. [Agents & Channels](https://octo.steinbok.net/agents-channels.html) · [Health Checks](https://octo.steinbok.net/healthcheck.html)

## 2026-10-22

Octo updated its service and setup guides for macOS and Linux. The guides explain how to run services and find their logs on each platform. [Service Catalog](https://octo.steinbok.net/services.html)

## 2026-10-18

Calendar refreshes now preserve the last good copy when a source fails and continue fetching from other sources. Repeated scheduled-job failures also trigger alerts so maintainers can investigate. [Scheduled Tasks](https://octo.steinbok.net/scheduled-tasks.html)

## 2026-10-17

Octo moved to OpenClaw 2026.10.4 and Carapace Plugin SDK 3, and tightened tool access for hook- and app-driven agents. Its docs audit also expanded to catch retired jobs, missing service pages, and broken links. [Plugin Catalog](https://octo.steinbok.net/plugins.html) · [Docs Pipeline](https://octo.steinbok.net/about-docs.html)

## 2026-07-14

Octo introduced the Engineering Harness to turn findings into tracked issues and move fixes through planning, implementation, and review. The workflow gave maintainers a place to review plans and changes along the way. [Engineering Harness](https://octo.steinbok.net/harness.html) · [Issue Lifecycle](https://octo.steinbok.net/harness/issue-lifecycle.html)

## 2026-07-06

Octo documented its public docs pipeline and made invalid plugin metadata fail the build. Maintainers can catch malformed catalog entries before they reach the site. [Docs Pipeline](https://octo.steinbok.net/about-docs.html)

## 2026-07-03

Octo began rendering and validating the public docs in the same build. Maintainers can preview the finished site locally, and the publishing job deploys the checked output. [Docs Pipeline](https://octo.steinbok.net/about-docs.html)

## 2026-06-03

Octo added read-only Obsidian search and support for threaded Fastmail replies. The initial Carapace Plugin SDK release also gave plugin authors a way to generate command-line tools. [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub) · [CLI Tools](https://octo.steinbok.net/clis.html)

## 2026-05-09

Package tracking gained built-in USPS, FedEx, and UPS status lookups. External providers can override the defaults or fall back to them when they have no result. [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub)

## 2026-05-08

Octo switched scheduled calendar refreshes to plugin command-line tools. Refreshes run faster and use no model tokens for fetching. [CLI Tools](https://octo.steinbok.net/clis.html)

## 2026-05-07

Octo added generated command-line interfaces for its plugins. Maintainers can use the same tools from scripts and test them independently of an agent session. [CLI Tools](https://octo.steinbok.net/clis.html)

## 2026-05-06

Octo added shipment-processing actions and a package tracking plugin with pluggable status providers. Mail automations can register shipments and tracking can use the provider best suited to each carrier. [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub) · [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html)

## 2026-05-03

OpenClaw Hub moved its shared libraries, plugins, and Fastmail SSE service to TypeScript and added automated coverage for the migrated packages. It also added integrations for Withings, Glances, and restaurant search. [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub)

## 2026-04-27

Octo added automatic discovery of enabled plugins for its docs catalog and drew reusable integrations from their public source in OpenClaw Hub. Maintainers could follow the catalog back to the source that ships each integration. [Plugin Catalog](https://octo.steinbok.net/plugins.html) · [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub)

## 2026-04-19

Octo added an exporter that packages plugins and services with their shared dependencies. The bundles make reusable integrations easier to distribute and install. [OpenClaw Hub](https://github.com/JeffSteinbok/openclaw-hub)

## 2026-04-10

Octo documented how the shared mail runtime processes incoming messages and how the USPS plugin uses it. The guides show maintainers where to configure rules and how the processing stages fit together. [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html)

## 2026-04-09

Octo added richer Outlook calendar event details, faster calendar refreshes, and mail rules for USPS Informed Delivery. These changes gave agents more calendar context and let mail workflows recognize delivery notices. [Agents & Channels](https://octo.steinbok.net/agents-channels.html) · [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html)

## 2026-04-05

Octo experimented with voice calls, speech recognition, and speech synthesis. The initial voice chat configuration was removed while the rest of the platform evolved.

## 2026-03-28

Fastmail shipment detection began skipping placeholder tracking numbers in Amazon messages. This reduced false shipments in package tracking. [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html)

## 2026-03-14

Fastmail SSE expanded to watch multiple mailboxes with independent rules and to extract tracking numbers for automatic package updates. Octo also added stock quotes and expanded calendar support for TripIt and ICS feeds. [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html) · [Plugin Catalog](https://octo.steinbok.net/plugins.html)

## 2026-03-10

Octo added GitHub issue tools and expanded its Home Assistant tools. Agents could work with tracked issues and handle more home automation tasks from their conversations. [GitHub Plugin](https://octo.steinbok.net/plugins/github.html) · [Plugin Catalog](https://octo.steinbok.net/plugins.html)

## 2026-03-08

Octo added Outlook, ICS calendars, Spotify, and other integrations. It also started generating a docs bundle so readers could discover plugins, services, and scheduled work in one place. [Plugin Catalog](https://octo.steinbok.net/plugins.html) · [Docs Pipeline](https://octo.steinbok.net/about-docs.html)

## 2026-03-05

Octo added an event-driven Fastmail integration. OpenClaw can process incoming mail through rules and hand off selected events to agents. [Fastmail SSE](https://octo.steinbok.net/services/fastmail-sse.html)
