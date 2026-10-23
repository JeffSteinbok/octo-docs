---
layout: default
title: Home
nav_order: 1
---

<div class="hero" markdown="0">
  <img src="{{ site.baseurl }}/assets/images/Octo_trimmed_tools.png" alt="Octo" />
  <h1>All About Octo&hellip;</h1>
  <p class="tagline">
    A personal AI assistant built on
    <a href="https://openclaw.ai">OpenClaw</a> — connecting language models
    to real-world services through plugins, agents, and channels.
  </p>
</div>

<div class="card-grid" markdown="0">
  <a class="card" href="{{ site.baseurl }}/memory">
    <div class="card-icon">🧠</div>
    <div class="card-title">Memory</div>
    <div class="card-desc">How agents remember — manual notes, dreaming, and HEARTBEAT discipline</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/agents-channels">
    <div class="card-icon">🤖</div>
    <div class="card-title">Agents &amp; Channels</div>
    <div class="card-desc">Personas and the platforms they talk through</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/plugins">
    <div class="card-icon">🧩</div>
    <div class="card-title">Plugins</div>
    <div class="card-desc">Modular capabilities — email, cameras, restaurants&hellip;</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/skills">
    <div class="card-icon">🎯</div>
    <div class="card-title">Skills</div>
    <div class="card-desc">Markdown-defined knowledge — no exec, no scripts</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/clis">
    <div class="card-icon">⌨️</div>
    <div class="card-title">CLI Tools</div>
    <div class="card-desc">Vetted scripts agents run via exec from ~/safebin/</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/services">
    <div class="card-icon">⚙️</div>
    <div class="card-title">Services</div>
    <div class="card-desc">Background daemons that watch for events</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/hooks">
    <div class="card-icon">🪝</div>
    <div class="card-title">Hooks</div>
    <div class="card-desc">Event-driven automations triggered by real-world activity</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/scheduled-tasks">
    <div class="card-icon">⏰</div>
    <div class="card-title">Scheduled Tasks</div>
    <div class="card-desc">Background jobs that sync data, send reminders, and keep Octo healthy</div>
  </a>
</div>

---

This is the documentation for **Octo** 🐙 — [Jeff Steinbok](https://github.com/JeffSteinbok)'s personal instance of
[OpenClaw](https://openclaw.ai), a modular AI assistant framework.

Selected public plugins, services, and shared Python libraries documented here are also mirrored in
[`openclaw-hub`](https://github.com/JeffSteinbok/openclaw-hub), which acts as the public source repo for those surfaces.

Much of this setup is inspired by [Omar Shahine](https://github.com/omarshahine)'s
work on 🦞 [Lobster](https://lobster.shahine.com) — his docs inspired me to publish
my own.

---


## 💬 Channels

I talk to Octo mostly via **iMessage**, plus [Discord](https://discord.com) and [Telegram](https://telegram.org). iMessage was always the channel I wanted, but it needs a Mac, and I wasn't buying one until I'd decided this was useful. It was: in October 2026 Octo moved to its own Mac mini, and now it sends and receives iMessages from there through OpenClaw's iMessage channel.

Family can text Octo too. Their DMs and our family group chat go to a separate **family** agent (see Security below). In other group chats Octo only answers when someone mentions it.

## 🔒 Security

<div class="info-box" markdown="0">
Security is the most important aspect of this experiment — even above just having fun.
</div>

- **Unprivileged account** — OpenClaw runs under its own dedicated standard (non-admin) macOS user with no `sudo` permissions. It can configure itself new plugins, but it cannot install anything on its own.
- **Owner-first access** — Octo's main agent only responds to me. Family members can message a separate **family** agent over iMessage, which has a much narrower set of tools.
- **Per-person calendar rules** — The family agent can read and update the family calendar for anyone, but only Nicole can ask about her calendar, only Nicole or I can ask about my work calendar, and only I can ask about my personal calendar and TripIt. The calendar plugins enforce this from the sender the channel reports, not from what the message claims.
- **No secrets in Git** — All tokens and credentials are kept in hidden files that are never synced to version control.
- **No exec on the main agent** — Octo's primary agent does not have `exec` permissions, meaning it cannot run arbitrary shell commands. If something truly dangerous needs to happen, I have to explicitly ask the **root** agent, which is the only one with elevated privileges. This also means we rely more heavily on purpose-built plugins rather than skills — since skills can't execute code without `exec`, every real-world interaction needs a proper plugin behind it.

### 📬 Mail & Calendar

- **Full mail read access** — Octo reads Jeff's personal Outlook inbox directly via the Microsoft Graph API (OAuth2). Mail is never injected into the AI as raw content — Octo queries it on demand using structured API calls.
- **Calendar access** — Octo fetches Jeff's personal and family calendars via Graph API, Nicole's calendar via ICS feed, and the work calendar via Exchange/Graph API. Calendars are synced to markdown files in memory every hour (7 AM–5 PM) and at midnight.
- **Dedicated mailbox** — Octo has its own mailbox on [Fastmail](https://www.fastmail.com) where it sends mail on Jeff's behalf. Incoming mail to that address is monitored via a Python SSE service.

## 💰 Cost

- **Self-hosted** — Runs on a Mac mini (Apple silicon, 16 GB of RAM) running macOS. It moved there from an old Lenovo X1 Yoga Gen 3 running Ubuntu in October 2026; the setup still works on Linux.
- **Token-conscious** — As much work as possible is pushed to Python plugins to reduce token usage. The default model is Anthropic Claude Sonnet 4.6, with Claude Haiku 4.5 and OpenAI as fallbacks. Ongoing effort goes into keeping per-run costs low:
    - Recurring tasks that don't need reasoning are rewritten as plain shell scripts executed via `exec`, eliminating model tokens entirely (e.g., calendar fetching dropped from ~75 s with 5 tool calls to ~6 s with zero tokens).
    - Cron jobs use `lightContext: true` to strip session history from the context window, cutting input tokens on every scheduled run.
    - Tool-allow lists (`toolsAllow`) are scoped narrowly on cron entries so agents can't accidentally reach for expensive tools.
    - Yes/no judgment calls go to a small typed decision model ([TypeSafe AI](https://docs.openclaw.ai/plugins/typesafe)'s Jev) instead of a full chat model.
    - The general pattern is: push work into scripts, let agents just interpret results.

  See [Models]({{ site.baseurl }}/models) for the current model lineup, fallbacks and per-agent overrides.

- **Development via [Claude Code](https://claude.com/claude-code)** — All plugin and config development is done through Claude Code. Initially I had Octo debug itself, but it turned out to be far more effective to use a separate Claude Code session for development, log reading, and troubleshooting.
- **Crontab over agent jobs** — Recurring tasks are pushed to crontab whenever possible to avoid spinning up agent sessions. If something fails, the script can send a message to OpenClaw to inform of the error.
- **Weekly cost report** — Every Monday at 5 AM PT, the root agent runs a [usage report skill]({{ site.baseurl }}/skills/usage-report) that parses OpenClaw's usage logs, generates a Markdown report broken down by agent, model, and token type, renders it to PDF, and posts it to Discord. It covers token cost breakdown (input / output / cache read / cache write), per-agent spend, cron job vs. interactive split, daily trend, and a model split table — everything needed to spot where costs are climbing and why.

## 🔧 Self-Improvement — The Octo Engineering Harness

Octo has a small but growing set of mechanisms for detecting its own drift and quality problems — and fixing them automatically. Validation scripts run on a weekly cron, file GitHub issues for anything they find, and a state machine drives each issue from triage through planning, Claude Code fix, PR review, and merge. The only manual step is approving the plan.

**[Engineering Harness →]({{ site.baseurl }}/harness)**

---

## 🦞 How [OpenClaw](https://openclaw.ai) Works — Super High Level ✈️

🤖 **[Agents & Channels]({{ site.baseurl }}/agents-channels)** — Agents are personas powered by language models. Each agent has its own
identity, personality, and set of permitted tools. Agents communicate with
users through **channels** — messaging platforms like iMessage, Discord or Telegram.

🧩 **[Plugins]({{ site.baseurl }}/plugins)** are self-contained capabilities that agents can invoke: sending
email, checking restaurant availability, snapping a security camera, and more.
Each plugin declares its own dependencies and is independently versioned.

🎯 **[Skills]({{ site.baseurl }}/skills)** are lightweight, markdown-defined capabilities. Unlike plugins,
skills don't run code — they provide structured prompts and instructions that
guide an agent's behavior. Think of plugins as _tools_ and skills as _knowledge_.

⌨️ **[CLI Tools]({{ site.baseurl }}/clis)** are vetted shell scripts that agents can invoke via `exec` from `~/safebin/`.
They let agents run deterministic, token-free operations — file transforms, data exports,
system queries — without reaching for a plugin.

⚙️ **[Services]({{ site.baseurl }}/services)** are long-running background daemons that watch for events (like
incoming email) and route notifications through the system.

🪝 **[Hooks]({{ site.baseurl }}/hooks)** are event-driven entry points — camera webhooks and other
signals that kick off targeted automations the moment something happens.

🧠 **[Memory]({{ site.baseurl }}/memory)** covers how agents build up long-term knowledge — manual
`MEMORY.md` files and daily notes committed to git, plus the autonomous **dreaming** process
that synthesises session transcripts in the background during idle time.
