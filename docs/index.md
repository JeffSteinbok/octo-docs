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
  <a class="card" href="{{ site.baseurl }}/services">
    <div class="card-icon">⚙️</div>
    <div class="card-title">Services</div>
    <div class="card-desc">Background daemons that watch for events</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/scheduled-tasks">
    <div class="card-icon">⏰</div>
    <div class="card-title">Scheduled Tasks</div>
    <div class="card-desc">Background jobs that sync data, send reminders, and keep Octo healthy</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/hooks">
    <div class="card-icon">🪝</div>
    <div class="card-title">Hooks</div>
    <div class="card-desc">Event-driven automations triggered by real-world activity</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/clis">
    <div class="card-icon">⌨️</div>
    <div class="card-title">CLI Tools</div>
    <div class="card-desc">Vetted scripts agents run via exec from ~/safebin/</div>
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

<div class="info-box info-box--highlight" markdown="0">
  <h3>🐢 Featured: Carapace Plugin SDK</h3>
  <p>
    <a href="https://github.com/JeffSteinbok/carapace-plugin-sdk">
      <img src="https://raw.githubusercontent.com/JeffSteinbok/carapace-plugin-sdk/main/assets/github-social-preview.png"
           alt="Carapace Plugin SDK"
           style="max-width: 480px; width: 100%; border-radius: 8px; margin-bottom: 12px;" />
    </a>
  </p>
  <p>
    The plugin system that powers OpenClaw is now available as an open-source SDK on npm.
    <strong>Carapace Plugin SDK</strong> gives you everything you need to build, test, and
    ship your own plugins — type-safe tool definitions, config schemas, and automatic CLI
    generation from a single <code>definePlugin()</code> call.
  </p>
  <p><strong>Ecosystem:</strong></p>
  <ul>
    <li><a href="https://www.npmjs.com/package/carapace-plugin-sdk"><strong>carapace-plugin-sdk</strong></a> — the core SDK (<code>npm install carapace-plugin-sdk</code>)</li>
    <li><a href="https://github.com/JeffSteinbok/carapace-plugin-template"><strong>carapace-plugin-template</strong></a> — scaffold a new plugin repo in seconds</li>
    <li><a href="https://github.com/JeffSteinbok/carapace-stock-quotes"><strong>carapace-stock-quotes</strong></a> — a real-world example plugin for stock, ETF, and mutual fund quotes</li>
    <li><a href="https://github.com/JeffSteinbok/carapace-mail-runtime"><strong>carapace-mail-runtime</strong></a> — provider-agnostic mail rule engine</li>
    <li><a href="https://github.com/JeffSteinbok/carapace-package-tracking"><strong>carapace-package-tracking</strong></a> — carrier detection, tracking URLs, and status providers</li>
  </ul>
  <p>
    Every plugin in <a href="https://github.com/JeffSteinbok/openclaw-hub">openclaw-hub</a>
    has been converted to use the Carapace SDK. Want to build your own?
    <a href="https://github.com/JeffSteinbok/carapace-plugin-template">Start from the template →</a>
  </p>
</div>

## 💬 Channels

I talk to Octo via [Telegram](https://telegram.org) and [Discord](https://discord.com). I'd prefer to use iMessage or WhatsApp, but until I've decided for sure that this is useful, I'm not going out and buying a Mac Mini or getting a new phone number.

## 🔒 Security

<div class="info-box" markdown="0">
Security is the most important aspect of this experiment — even above just having fun.
</div>

- **Unprivileged account** — OpenClaw runs under its own dedicated user on Ubuntu with no `sudo` permissions. It can configure itself new plugins, but it cannot install anything on its own.
- **Owner-only access** — Octo only responds to me. Not even family members have access.
- **No secrets in Git** — All tokens and credentials are kept in hidden files that are never synced to version control.
- **No exec on the main agent** — Octo's primary agent does not have `exec` permissions, meaning it cannot run arbitrary shell commands. If something truly dangerous needs to happen, I have to explicitly ask the **root** agent, which is the only one with elevated privileges. This also means we rely more heavily on purpose-built plugins rather than skills — since skills can't execute code without `exec`, every real-world interaction needs a proper plugin behind it.

### 📬 Mail & Calendar

- **Full mail read access** — Octo reads Jeff's personal Outlook inbox directly via the Microsoft Graph API (OAuth2). Mail is never injected into the AI as raw content — Octo queries it on demand using structured API calls.
- **Calendar access** — Octo fetches Jeff's personal and family calendars via Graph API, Nicole's calendar via ICS feed, and the work calendar via Exchange/Graph API. Calendars are synced to markdown files in memory every hour (7 AM–5 PM) and at midnight.
- **Dedicated mailbox** — Octo has its own mailbox on [Fastmail](https://www.fastmail.com) where it sends mail on Jeff's behalf. Incoming mail to that address is monitored via a Python SSE service.

## 💰 Cost

- **Self-hosted** — Runs on an old Lenovo X1 Yoga Gen 3 with 16 GB of RAM running Ubuntu Desktop.
- **Token-conscious** — As much work as possible is pushed to Python plugins to reduce token usage. Primary model is GitHub Copilot Sonnet (covered by the Copilot subscription), with Anthropic and Gemini as fallbacks. Ongoing effort goes into keeping per-run costs low:
    - Recurring tasks that don't need reasoning are rewritten as plain shell scripts executed via `exec`, eliminating model tokens entirely (e.g., calendar fetching dropped from ~75 s with 5 tool calls to ~6 s with zero tokens).
    - Cron jobs use `lightContext: true` to strip session history from the context window, cutting input tokens on every scheduled run.
    - Tool-allow lists (`toolsAllow`) are scoped narrowly on cron entries so agents can't accidentally reach for expensive tools.
    - The general pattern is: push work into scripts, let agents just interpret results.

  | Role | Model | Notes |
  |------|-------|-------|
  | Primary | `github-copilot/claude-sonnet-4.6` | Default for all agents (alias: `copilot-sonnet`) |
  | Fallbacks | `claude-haiku-4-5` → `claude-sonnet-4-6` → `gemini-2.5-flash` → `gemini-3-pro-preview` | In priority order |
  | Image | `github-copilot/claude-sonnet-4.6` → `claude-sonnet-4-6` → `gemini-2.5-flash-preview` | |
  | Web search | `gemini-2.5-flash-lite` | |

- **Development via [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)**— All plugin and config development is done through Copilot CLI. Initially I had Octo debug itself, but it turned out to be far more effective to use a separate Copilot CLI session for development, log reading, and troubleshooting.
- **Crontab over agent jobs** — Recurring tasks are pushed to crontab whenever possible to avoid spinning up agent sessions. If something fails, the script can send a message to OpenClaw to inform of the error.

## 🦞 How [OpenClaw](https://openclaw.ai) Works — Super High Level ✈️

🤖 **Agents** are personas powered by language models. Each agent has its own
identity, personality, and set of permitted tools. Agents communicate with
users through **channels** — messaging platforms like Telegram or Discord.

💬 **Channels** are the messaging platforms that connect agents to users.
Each channel is bound to a specific agent and handles message routing
between the platform (e.g. Telegram, Discord) and the agent's conversation loop.

🧩 **Plugins** are self-contained capabilities that agents can invoke: sending
email, checking restaurant availability, snapping a security camera, and more.
Each plugin declares its own dependencies and is independently versioned.

🎯 **Skills** are lightweight, markdown-defined capabilities. Unlike plugins,
skills don't run code — they provide structured prompts and instructions that
guide an agent's behavior. Think of plugins as _tools_ and skills as _knowledge_.

⚙️ **Services** are long-running background daemons that watch for events (like
incoming email) and route notifications through the system.

🪝 **Hooks** are event-driven entry points — camera webhooks and other
signals that kick off targeted automations the moment something happens.
