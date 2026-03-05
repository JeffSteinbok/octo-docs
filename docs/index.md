---
layout: default
title: Home
nav_order: 1
---

<p align="center">
  <img src="{{ site.baseurl }}/assets/images/Octo_small.png" alt="Octo" width="200" />
</p>

# 🐙 Octo Docs

OpenClaw is a modular AI assistant framework that connects language models to
real-world services through **skills**, **agents**, and **channels**.

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

## 📚 Learn More

- [🔧 Skills](skills.html) — what the system can do
- [🏗️ Architecture](architecture.html) — how the pieces fit together
- [⚙️ Services](services.html) — background event processing
- [⏰ Scheduled Jobs](jobs.html) — automated recurring tasks