---
layout: default
title: Services
nav_order: 5
---

# Services

OpenClaw services are background processes that keep long-running automations available between conversations.


## Service Summary

| Service | Description | Docs |
|---------|-------------|------|
| 📡 FastMail SSE Service | Real-time email notification daemon using JMAP EventSource | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) |
| ⚙️ Octo Satellite | Local secrets broker providing credentialed access to Amazon and Monarch Money without exposing passwords or session cookies to the gateway | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 🗂️ OneDrive Sync | Keeps the Obsidian vault and other files synced to Microsoft OneDrive via the abraunegg/onedrive Linux client | [Read more →](services/onedrive-sync) |
| 📝 Obsidian Vault Indexer | Long-running indexer that maintains a SQLite FTS5 index of the Obsidian vault for full-text search | [Read more →](services/obsidian-indexer) |
