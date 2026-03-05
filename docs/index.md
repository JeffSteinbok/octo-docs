---
layout: default
title: Home
---

# 🐙 Octo Docs

OpenClaw is a modular AI assistant framework that connects language models to
real-world services through **skills**, **agents**, and **channels**.

## 📊 At a Glance

| | Count |
|---|---|
| 🔧 Skills | 3 |
| ⚙️ Services | 1 |
| 🤖 Agents | 4 |
| 📡 Channels | Telegram, Discord |

## 🧠 How It Works

🤖 **Agents** are personas powered by language models. Each agent has its own
identity, personality, and set of permitted tools. Agents communicate with
users through **channels** — messaging platforms like Telegram or Discord.

🔧 **Skills** are self-contained capabilities that agents can invoke: sending
email, checking restaurant availability, snapping a security camera, and more.
Each skill declares its own dependencies and is independently versioned.

⚙️ **Services** are long-running background daemons that watch for events (like
incoming email) and route notifications through the system.

## 📚 Learn More

- [🔧 Skills](skills.html) — what the system can do
- [⚙️ Services](services.html) — background event processing
- [🏗️ Architecture](architecture.html) — how the pieces fit together