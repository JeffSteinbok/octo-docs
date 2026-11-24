---
layout: default
title: Home Assistant Events
nav_order: 2
nav_exclude: true
---

# 🪝 Home Assistant Events

When a Home Assistant automation spots something at the house (motion, a person, vehicle or animal picked up by LLM Vision, or a doorbell press), it posts the event to OpenClaw. The `hass-hooks` agent decides whether it matters and, if it does, sends the owner a short, casual line over iMessage built from LLM Vision's own description, with the camera pictures attached.

## How an event gets here

1. A Home Assistant automation posts the event as JSON to the [Webhook Proxy](../services/webhook-proxy)'s `/hass` route over the home network, with its own token in the `Authorization` header.
2. The proxy checks that token and forwards the event to the Gateway's `/hooks/hass` endpoint with OpenClaw's hooks token added.
3. OpenClaw's hook mapping turns the JSON into a plain-text message (source, camera, title, summary, key frame, and yes/no flags for motion, person, vehicle, animal and doorbell) and starts a turn for the `hass-hooks` agent.

## What the agent does

1. **Filters.** Events with nothing detected, such as "No Activity Observed" or routine blueprint triggers, end without a message.
2. **Checks who's home.** A stranger in the driveway matters more when nobody is home.
3. **Gets the pictures.** It fetches the key frame LLM Vision saved at the moment of the event (or takes a fresh snapshot from the triggering camera), and puts it on top of a collage of all the outdoor cameras as they look now.
4. **Writes the alert from LLM Vision's description.** The event's title and summary describe the moment of detection, so the agent rewrites them as one or two casual sentences and adds nothing of its own. It doesn't re-describe the pictures: a later look at the cameras used to change the story (a parked car, a "delivery" that wasn't one). Only for a doorbell press with no title or summary does an image model describe the photo, and the alert says so; when there's no key frame, it says the photo is from just now.
5. **Sends one message.** A single iMessage to the owner, with the collage attached.

## Safety

- Event text is treated as untrusted input: the agent never follows instructions that appear inside it.
- The agent's tools are limited to camera snapshots and collages, presence and state lookups, image analysis (only for events without a description), LLM Vision images and sending messages. It has no file access, shell or browser.

## At a glance

- **Endpoint:** `/hooksproxy/hass`
- **Agent:** `hass-hooks` (see [Agents & Channels](../agents-channels))
