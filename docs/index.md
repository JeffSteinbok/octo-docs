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
    to real-world services through agents, channels, and plugins.
  </p>
</div>

This is the documentation for **Octo** 🐙, [Jeff Steinbok](https://github.com/JeffSteinbok)'s personal AI assistant. Octo is one self-hosted instance of [OpenClaw](https://openclaw.ai), an open-source framework for running AI agents. It runs on a Mac mini, I talk to it mostly over iMessage, and it handles mail, calendars, packages, the house and more through a set of plugins, background services, webhooks and scheduled jobs.

These pages describe how it is put together, so you can borrow the parts you like for your own OpenClaw setup. Most of the site is generated from Octo's source repo ([About These Docs]({{ site.baseurl }}/about-docs) explains how), so the inventories stay current.

Much of this setup is inspired by [Omar Shahine](https://github.com/omarshahine)'s work on 🦞 [Lobster](https://lobster.shahine.com) — his docs inspired me to publish my own. Selected plugins, services and shared libraries documented here are published as open source in [`openclaw-hub`](https://github.com/JeffSteinbok/openclaw-hub).

<div class="card-grid" markdown="0">
  <a class="card" href="{{ site.baseurl }}/agents-channels">
    <div class="card-icon">🤖</div>
    <div class="card-title">Agents &amp; Channels</div>
    <div class="card-desc">Octo's agents, what each may do, and the messaging apps they talk through</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/memory">
    <div class="card-icon">🧠</div>
    <div class="card-title">Memory</div>
    <div class="card-desc">How agents remember — memory files, daily notes, and dreaming</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/models">
    <div class="card-icon">🧮</div>
    <div class="card-title">Models</div>
    <div class="card-desc">The language, decision and voice models behind each agent</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/external-integrations">
    <div class="card-icon">🌐</div>
    <div class="card-title">External Integrations</div>
    <div class="card-desc">How outside apps, other agents and webhooks reach Octo</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/plugins">
    <div class="card-icon">🧩</div>
    <div class="card-title">Plugins</div>
    <div class="card-desc">The tools agents call — email, calendars, cameras, restaurants&hellip;</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/skills">
    <div class="card-icon">🎯</div>
    <div class="card-title">Skills</div>
    <div class="card-desc">Markdown instructions that tell agents how to do a job</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/clis">
    <div class="card-icon">⌨️</div>
    <div class="card-title">CLI Tools</div>
    <div class="card-desc">Vetted scripts agents can run with <code>exec</code></div>
  </a>
  <a class="card" href="{{ site.baseurl }}/services">
    <div class="card-icon">⚙️</div>
    <div class="card-title">Services</div>
    <div class="card-desc">Background services that watch for events, such as new mail</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/scheduled-tasks">
    <div class="card-icon">⏰</div>
    <div class="card-title">Scheduled Tasks</div>
    <div class="card-desc">Jobs that sync data, send reminders, and keep Octo healthy</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/harness">
    <div class="card-icon">🔧</div>
    <div class="card-title">Engineering Harness</div>
    <div class="card-desc">How Octo finds its own problems and turns them into reviewed fixes</div>
  </a>
</div>

---

## 🦞 How Octo is put together

Octo is built from the standard [OpenClaw](https://openclaw.ai) pieces. At the center is the **Gateway**, OpenClaw's always-on process that runs the agents and connects them to everything else.

🤖 **[Agents]({{ site.baseurl }}/agents-channels)** are personas powered by language models. Each agent has its own identity, personality and set of permitted tools. Agents talk to people through **channels**: messaging apps such as iMessage, Discord and Telegram. The [Models]({{ site.baseurl }}/models) page lists which model each agent uses.

🧩 **[Plugins]({{ site.baseurl }}/plugins)** are self-contained tools that agents can call: sending email, checking restaurant availability, taking a snapshot from a security camera, and more. Each plugin declares its own dependencies and is versioned on its own.

🎯 **[Skills]({{ site.baseurl }}/skills)** are Markdown instructions. Unlike plugins, a skill is not code; it tells an agent how to approach a task and which tools to use. Think of plugins as _tools_ and skills as _know-how_.

⌨️ **[CLI Tools]({{ site.baseurl }}/clis)** are vetted scripts that agents allowed to use `exec` can run from `~/safebin/`. They do deterministic jobs — file transforms, data exports, system queries — without a plugin and without spending model tokens.

⚙️ **[Services]({{ site.baseurl }}/services)** are long-running background processes that watch for events (like incoming email) and pass them on to agents or notifications.

🪝 **[Hooks]({{ site.baseurl }}/hooks)** are webhook entry points. A webhook from GitHub, Home Assistant or Microsoft 365 starts an agent the moment something happens. [External Integrations]({{ site.baseurl }}/external-integrations) covers how hooks and outside apps reach Octo through Tailscale Funnel.

⏰ **[Scheduled Tasks]({{ site.baseurl }}/scheduled-tasks)** are OpenClaw cron jobs. Some start an agent; many just run a command and never touch a model.

🧠 **[Memory]({{ site.baseurl }}/memory)** is how agents build up long-term knowledge: `MEMORY.md` files and daily notes committed to Git, plus **dreaming**, a background process that distills session transcripts during idle time.

---

## 💬 Channels

I talk to Octo mostly over **iMessage**, plus [Discord](https://discord.com) and [Telegram](https://telegram.org). iMessage was always the channel I wanted, but it needs a Mac, and I wasn't buying one until I'd decided this was useful. It was: in October 2026 Octo moved to its own Mac mini, and it now sends and receives iMessages there through OpenClaw's iMessage channel.

Family can text Octo too. Their direct messages and our family group chat go to a separate **family** agent (see Security below). In other group chats Octo only answers when someone mentions it.

## 🔒 Security

<div class="info-box" markdown="0">
Security is the most important aspect of this experiment — even above just having fun.
</div>

- **Unprivileged account** — OpenClaw runs under its own standard (non-admin) macOS user with no `sudo` rights. It can configure new plugins for itself, but it can't install software on its own.
- **Owner-first access** — Octo's main agent only responds to me. Family members message a separate **family** agent over iMessage, which has a much narrower set of tools.
- **Per-person calendar rules** — The family agent can read and update the family calendar for anyone, but only Nicole can ask about her calendar, only Nicole or I can ask about my work calendar, and only I can ask about my personal calendar and TripIt. The calendar plugins enforce this using the sender the channel reports, not what the message claims.
- **No secrets in Git** — Tokens and credentials live in local files that are never committed to version control.
- **No `exec` on the main agent** — Octo's main agent can't run shell commands. If something truly needs elevated access, I have to ask the **root** agent explicitly; it is the only agent with elevated privileges. This is also why Octo leans on purpose-built plugins rather than skills: a skill can't run code without `exec`, so every real-world action needs a plugin behind it.

### 📬 Mail and calendar

- **Mail read access** — Octo reads my personal Outlook inbox through the Microsoft Graph API (OAuth2). Mail is never fed to the model wholesale; Octo queries it on demand with structured API calls.
- **Calendar access** — Octo reads my personal and family calendars through the Graph API, Nicole's calendar through an ICS feed, and my work calendar through Exchange and the Graph API. The calendars are synced to Markdown files in memory every hour from 7 AM to 5 PM, and at midnight.
- **Its own mailbox** — Octo has its own [Fastmail](https://www.fastmail.com) mailbox, which it uses to send mail on my behalf. The [Fastmail SSE service]({{ site.baseurl }}/services/fastmail-sse) watches that mailbox for incoming mail.

## 💰 Cost

- **Self-hosted** — Octo runs on a Mac mini (Apple silicon, 16 GB of RAM) running macOS. It moved there in October 2026 from an old Lenovo X1 Yoga Gen 3 running Ubuntu; the setup still works on Linux.
- **Token-conscious** — As much work as possible is pushed into plugins and scripts so it doesn't cost model tokens. The default model is Anthropic Claude Sonnet 4.6, with Claude Haiku 4.5 and an OpenAI model as fallbacks (see [Models]({{ site.baseurl }}/models) for the full lineup and per-agent overrides). The general rule is: push work into scripts, and let agents interpret the results.
    - **Command jobs over agent jobs** — Recurring tasks that don't need reasoning run as OpenClaw command jobs, which run a script without starting an agent session. Fetching calendars, for example, went from about 75 seconds and 5 tool calls to about 6 seconds and no tokens. If a script fails, it can send a message to OpenClaw to report the error.
    - **Light context for agent jobs** — Scheduled jobs that do need an agent use `lightContext: true`, which leaves session history out of the context window and cuts input tokens on every run.
    - **Narrow tool lists** — Scheduled jobs set `toolsAllow` to just the tools they need, so an agent can't reach for an expensive one by accident.
    - **Small models for yes/no calls** — Yes/no judgment calls go to a small decision model ([TypeSafe AI](https://docs.openclaw.ai/plugins/typesafe)'s Jev) instead of a full chat model.
- **Weekly cost report** — Every Monday at 5 AM Pacific, the root agent runs the [usage report skill](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/usage-report). It parses OpenClaw's usage logs and posts a PDF report to Discord, broken down by agent, model and token type (input, output, cache read, cache write), with the split between scheduled and interactive runs, a daily trend, and a per-model table — enough to see where costs are climbing and why.
- **Development with [Claude Code](https://claude.com/claude-code)** — All plugin and config development happens in Claude Code. At first I had Octo debug itself, but a separate Claude Code session turned out to be far better for development, reading logs and troubleshooting.

## 🔧 Self-improvement

Octo has a small but growing set of checks that look for its own drift and quality problems. They run weekly and file GitHub issues for what they find. When I approve an issue, Octo writes a plan; when I approve the plan, Claude Code implements it and Octo opens a pull request for me to review and merge. Nothing merges without my approval, and a separate [Health Check]({{ site.baseurl }}/healthcheck) catches regressions while changes are rolled out.

**[Engineering Harness →]({{ site.baseurl }}/harness)**

---

For how this site is built and published, see [About These Docs]({{ site.baseurl }}/about-docs). For what changed recently, see the [Release Notes]({{ site.baseurl }}/releases/latest).
