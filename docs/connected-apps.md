---
layout: default
title: Connected Apps
parent: Agents & Channels
nav_order: 1
has_children: true
---

# Connected Apps

Apps and agents outside OpenClaw that connect to the gateway as paired devices. Unlike [channels](agents-channels#channels), which OpenClaw connects out to, these connect in, and what they can do depends on the device's scopes and the agent it reaches.

| Integration | What it is | How it connects |
|-------------|------------|-----------------|
| [Hassonic](hassonic) | Native iOS app for Home Assistant | Paired gateway device, talking only to the dedicated `hassonic` agent |
| [OctoDot](octodot) | An [OpenAI Dot](https://openai.com/index/introducing-dots/) | Custom MCP connector in ChatGPT, signed in through WorkOS ([MCP & OctoDot](mcp)) |

This section doesn't cover webhooks. Systems that trigger agents with one-way events, such as Home Assistant camera alerts and GitHub issues, are documented under [Hooks](hooks).
