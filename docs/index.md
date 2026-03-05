---
layout: default
title: Home
nav_order: 1
---

<img src="{{ site.baseurl }}/assets/images/Octo_small.png" alt="Octo" width="180" style="float: right; margin: 0 0 1em 1.5em;" />

# All About Octo...

This is the documentation for **Octo** 🐙 — [Jeff Steinbok](https://github.com/JeffSteinbok)'s personal instance of
[OpenClaw](https://openclaw.ai), a modular AI assistant framework that connects
language models to real-world services through **skills**, **agents**, and **channels**.

Much of this setup is inspired by [Omar Shahine](https://github.com/omarshahine)'s
work on 🦞 [Lobster](https://lobster.shahine.com) — his docs inspired me to publish
my own.

## 🔒 Security

Security is the most important aspect of this experiment — even above just having fun.

- **Unprivileged account** — OpenClaw runs under its own dedicated user on Ubuntu with no `sudo` permissions. It can configure itself new skills, but it cannot install anything on its own.
- **Owner-only access** — Octo only responds to me. Not even family members have access.
- **No secrets in Git** — All tokens and credentials are kept in hidden files that are never synced to version control.

## 🧠 How It Works

🤖 **Agents** are personas powered by language models. Each agent has its own
identity, personality, and set of permitted tools. Agents communicate with
users through **channels** — messaging platforms like Telegram or Discord.

🔧 **Skills** are self-contained capabilities that agents can invoke: sending
email, checking restaurant availability, snapping a security camera, and more.
Each skill declares its own dependencies and is independently versioned.

⚙️ **Services** are long-running background daemons that watch for events (like
incoming email) and route notifications through the system.

⏰ **Scheduled Jobs** run automatically on a timer — fetching calendars,
backing up config, and other recurring tasks without user intervention.