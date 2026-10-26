---
layout: default
title: LAN Notify Relay
nav_order: 3
nav_exclude: true
---

# 🪝 LAN Notify Relay

Services on the home network post short notifications to the Gateway's `/hooks/notify` endpoint, and the `notify` agent forwards each one to the owner over iMessage, word for word. It's a way for scripts and machines on the network to reach the owner without each one needing its own messaging setup.

## What arrives

Each notification comes pre-formatted, with the sending machine's name and a title on the first line and the message below:

```
📢 **[COMPUTERNAME] Title**
Message body here
```

## What the agent does

It sends the text exactly as received, with no commentary, rewording or summarizing, and then ends the turn without a reply.

## Safety

Notification text is untrusted, so the agent's only tool is sending a message. It can't read files, run commands or browse, which means a crafted notification can't make it do anything except pass the text along.

## At a glance

- **Endpoint:** `/hooks/notify`
- **Agent:** `notify` (see [Agents & Channels](../agents-channels))
