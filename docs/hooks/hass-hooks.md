---
layout: default
title: Home Assistant Events
nav_order: 2
nav_exclude: true
---

# 🪝 Home Assistant Events

When a Home Assistant automation spots something at the house (motion, a person, vehicle or animal picked up by LLM Vision, or a doorbell press), it posts the event to OpenClaw. The `hass-hooks` agent decides whether it matters and, if it does, sends the owner a short, casual summary on Discord with the camera snapshot attached.

## How an event gets here

1. A Home Assistant automation posts the event as JSON to the [Webhook Proxy](../services/webhook-proxy)'s `/hass` route over the home network, with its own token in the `Authorization` header.
2. The proxy checks that token and forwards the event to the Gateway's `/hooks/hass` endpoint with OpenClaw's hooks token added.
3. OpenClaw's hook mapping turns the JSON into a plain-text message (source, camera, title, summary, key frame, and yes/no flags for motion, person, vehicle, animal and doorbell) and starts a turn for the `hass-hooks` agent.

## What the agent does

1. **Filters.** Events with nothing detected, such as "No Activity Observed" or routine blueprint triggers, end without a message.
2. **Checks who's home.** A stranger in the driveway matters more when nobody is home.
3. **Gets the pictures.** It fetches the key frame LLM Vision saved at the moment of the event (or takes a fresh snapshot from the triggering camera), plus a collage of all the outdoor cameras as they look now.
4. **Summarizes.** An image model looks at both pictures and writes one or two casual sentences, such as "Just a delivery driver dropping off a package."
5. **Sends one message.** A single Discord DM to the owner, with the key frame attached.

## Safety

- Event text is treated as untrusted input: the agent never follows instructions that appear inside it.
- The agent's tools are limited to camera snapshots and collages, presence and state lookups, image analysis, LLM Vision images and sending messages. It has no file access, shell or browser.

## At a glance

- **Endpoint:** `/hooks/hass`
- **Agent:** `hass-hooks` (see [Agents & Channels](../agents-channels))
