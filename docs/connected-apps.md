---
layout: default
title: Connected Apps
parent: External Integrations
nav_order: 2
has_children: true
---

# Connected Apps

Apps outside OpenClaw that talk to Octo directly. Unlike [channels](agents-channels#channels), which OpenClaw connects out to, these connect in, and what they can do depends on how they authenticate and which agent they reach.

| Integration | What it is | How it connects |
|-------------|------------|-----------------|
| [Hassonic](hassonic) | Native iOS app for Home Assistant | Paired gateway device, talking only to the dedicated `hassonic` agent |
| [OctoDot](mcp) | An [OpenAI Dot](https://openai.com/index/introducing-dots/) in ChatGPT | Custom MCP connector to Octo's MCP server, signed in through WorkOS, answered by the dedicated `external` agent. See [MCP & OctoDot](mcp) |

This section doesn't cover webhooks. Systems that trigger agents with one-way events, such as Home Assistant camera alerts and GitHub issues, are documented under [Hooks](hooks).
