---
layout: default
title: Connected Apps
parent: External Integrations
nav_order: 2
has_children: true
---

# Connected Apps

Apps outside OpenClaw that talk to Octo directly, over the public entry point described in [External Integrations](external-integrations). Unlike [channels](agents-channels#channels), which OpenClaw connects out to, these connect in, and what they can do depends on how they authenticate and which agent they reach.

| Integration | What it is | How it connects |
|-------------|------------|-----------------|
| [Hassonic](hassonic) | Native iOS app for Home Assistant | Paired Gateway device, talking only to the dedicated `hassonic` agent |
| [OctoDot](mcp) | An [OpenAI Dot](https://openai.com/index/introducing-dots/) in ChatGPT | Custom MCP connector to the Octo MCP, signed in through WorkOS; reads come back condensed and changes go through the dedicated `external` agent |

This section doesn't cover webhooks. Systems that trigger agents with one-way events, such as Home Assistant camera alerts and GitHub issues, are documented under [Hooks](hooks).
