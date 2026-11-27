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
3. OpenClaw's hook mapping turns the JSON into a plain-text message (source, camera, title, summary, key frame, and yes/no flags for motion, person, vehicle, animal and doorbell) and starts a turn for the `hass-hooks` agent. Home Assistant derives the flags from camera sensors. The agent bases its decision on the title and summary, with a separate rule to alert on a doorbell ring.

## What the agent does

1. **Filters.** Events with nothing detected, such as "No Activity Observed" or routine blueprint triggers, end without a message.
2. **Checks who's home.** A stranger in the driveway matters more when nobody is home.
3. **Gets the pictures.** It fetches the key frame LLM Vision saved at the moment of the event (or takes a fresh snapshot from the triggering camera), and puts it on top of a collage of all the outdoor cameras as they look now.
4. **Writes the alert from LLM Vision's description.** The event's title and summary describe the moment of detection, so the agent rewrites them as one or two casual sentences and adds nothing of its own. It doesn't re-describe the pictures: a later look at the cameras used to change the story (a parked car, a "delivery" that wasn't one). Only for a doorbell press with no title or summary does an image model describe the photo, and the alert says so; when there's no key frame, it says the photo is from just now.
5. **Sends one message.** A single iMessage to the owner, with a collage from `~/.openclaw/media/camera_captures` or an event frame from `~/.openclaw/media/llmvision/snapshots`. Sends fall back to text if no image is available. The Hass Alert Gate plugin enforces the recipient and attachment paths in both decision modes.

## Safety

- Event text is treated as untrusted input: the agent never follows instructions that appear inside it.
- The agent can use camera snapshots and collages, presence and state lookups, image analysis for events without a description, LLM Vision images, messaging, and skill tools. The `read` tool is workspace-only. Granting it also lets `message` attach files from OpenClaw’s temporary directory, anywhere in its media cache, and its delivery-queue media directory. Attachments must be verified image, audio, video, PDF, or office files. Attachment checks block `.env` files, secrets, and files in other agents’ workspaces.

## At a glance

- **Endpoint:** `/hooksproxy/hass`
- **Agent:** `hass-hooks` (see [Agents & Channels](../agents-channels))
