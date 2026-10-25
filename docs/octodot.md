---
layout: default
title: OctoDot
parent: Connected Apps
grand_parent: External Integrations
nav_order: 2
---

# OctoDot

OctoDot is an [OpenAI Dot](https://openai.com/index/introducing-dots/), set up in ChatGPT, that can work with Octo.

## How it connects

OctoDot uses a custom MCP connector in ChatGPT. The connector calls Octo's own MCP server, octo-mcp, which requires a
WorkOS AuthKit sign-in and accepts only Octo's owner. See [MCP & OctoDot](mcp) for how it works, and
[ChatGPT connector](mcp-chatgpt) for setup and troubleshooting.

## What it can do

| Tool | Status | What it does |
|---|---|---|
| `ping` | Live | Confirms the connection works |
| `ask_octo` | Planned | Sends a question to a dedicated `octodot` agent with Home Assistant read and control and calendar read |

OctoDot used to connect through the OpenClaw web chat, paired as an operator device with full admin access. That
pairing will be removed once `ask_octo` works.
