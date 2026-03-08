---
layout: default
title: Home
nav_order: 1
---

<div class="hero" markdown="0">
  <img src="{{ site.baseurl }}/assets/images/Octo_small_trimmed.png" alt="Octo" />
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
    <div class="card-icon">🔧</div>
    <div class="card-title">Plugins</div>
    <div class="card-desc">Modular capabilities — email, cameras, restaurants&hellip;</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/skills">
    <div class="card-icon">🔧</div>
    <div class="card-title">Skills</div>
    <div class="card-desc">Capabilities defined by MD content. Since we disable exec is off these need to not run scripts. </div>
  </a>
  <a class="card" href="{{ site.baseurl }}/services">
    <div class="card-icon">⚙️</div>
    <div class="card-title">Services</div>
    <div class="card-desc">Background daemons that watch for events</div>
  </a>
  <a class="card" href="{{ site.baseurl }}/jobs">
    <div class="card-icon">⏰</div>
    <div class="card-title">Scheduled Jobs</div>
    <div class="card-desc">Automated tasks on a timer</div>
  </a>
</div>

---

This is the documentation for **Octo** 🐙 — [Jeff Steinbok](https://github.com/JeffSteinbok)'s personal instance of
[OpenClaw](https://openclaw.ai), a modular AI assistant framework.

Much of this setup is inspired by [Omar Shahine](https://github.com/omarshahine)'s
work on 🦞 [Lobster](https://lobster.shahine.com) — his docs inspired me to publish
my own.

## 💬 Channels

I talk to Octo via [Telegram](https://telegram.org) and [Discord](https://discord.com). I'd prefer to use iMessage or WhatsApp, but until I've decided for sure that this is useful, I'm not going out and buying a Mac Mini or getting a new phone number.

## 🔒 Security

<div class="info-box" markdown="0">
Security is the most important aspect of this experiment — even above just having fun.
</div>

- **Unprivileged account** — OpenClaw runs under its own dedicated user on Ubuntu with no `sudo` permissions. It can configure itself new plugins, but it cannot install anything on its own.
- **Owner-only access** — Octo only responds to me. Not even family members have access.
- **No secrets in Git** — All tokens and credentials are kept in hidden files that are never synced to version control.

### 📬 Mail & Calendar

- **Full mail read access** — Octo reads Jeff's personal Outlook inbox directly via the Microsoft Graph API (OAuth2). Mail is never injected into the AI as raw content — Octo queries it on demand using structured API calls.
- **Calendar access** — Octo fetches Jeff's personal and family calendars via Graph API, Nicole's calendar via ICS feed, and the work calendar via Exchange/Graph API. Calendars are synced to markdown files in memory every hour (7 AM–5 PM) and at midnight.
- **Dedicated mailbox** — Octo has its own mailbox on [Fastmail](https://www.fastmail.com) (`octo@steinbok.net`) where it sends mail on Jeff's behalf. Incoming mail to that address is monitored via a Python SSE service.

## 💰 Cost

- **Self-hosted** — Runs on an old Lenovo X1 Yoga Gen 3 with 16 GB of RAM running Ubuntu Desktop.
- **Token-conscious** — As much work as possible is pushed to Python plugins to reduce token usage. Primary model is GitHub Copilot Sonnet (covered by the Copilot subscription), with Anthropic and Gemini as fallbacks.

  | Role | Model | Notes |
  |------|-------|-------|
  | Primary | `github-copilot/claude-sonnet-4.6` | Default for all agents (alias: `copilot-sonnet`) |
  | Fallbacks | `claude-haiku-4-5` → `claude-sonnet-4-6` → `gemini-2.5-flash` → `gemini-3-pro-preview` | In priority order |
  | Image | `github-copilot/claude-sonnet-4.6` → `claude-sonnet-4-6` → `gemini-2.5-flash-preview` | |
  | Web search | `gemini-2.5-flash-lite` | |

  GitHub Copilot Sonnet handles the bulk of everyday work at no extra token cost (covered by the Copilot subscription). Anthropic and Gemini are available as fallbacks.

- **Development via [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)** — All plugin and config development is done through Copilot CLI. Initially I had Octo debug itself, but it turned out to be far more effective to use a separate Copilot CLI session for development, log reading, and troubleshooting.
- **Crontab over agent jobs** — Recurring tasks are pushed to crontab whenever possible to avoid spinning up agent sessions. If something fails, the script can send a message to OpenClaw to inform of the error.

## 🦞 How [OpenClaw](https://openclaw.ai) Works — Super High Level ✈️

🤖 **Agents** are personas powered by language models. Each agent has its own
identity, personality, and set of permitted tools. Agents communicate with
users through **channels** — messaging platforms like Telegram or Discord.

🔧 **Plugins** are self-contained capabilities that agents can invoke: sending
email, checking restaurant availability, snapping a security camera, and more.
Each plugin declares its own dependencies and is independently versioned.

⚙️ **Services** are long-running background daemons that watch for events (like
incoming email) and route notifications through the system.

⏰ **Scheduled Jobs** run automatically on a timer — fetching calendars,
backing up config, and other recurring tasks without user intervention.
