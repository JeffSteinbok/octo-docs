---
layout: default
title: "Home Assistant \u2013 LLM Vision"
nav_order: 8
nav_exclude: true
---

# 📷 Home Assistant – LLM Vision

Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events.

> **Source:** [JeffSteinbok/openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/llmvision)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>server</code></td><td>string</td><td>Optional</td><td>Home Assistant server URL.</td></tr>
    <tr><td><code>token</code></td><td>string</td><td>Optional</td><td>Home Assistant long-lived access token.</td></tr>
  </tbody>
</table>

## Example config

Set credentials in `plugins.entries["llmvision"].config`:

```json
{
  "plugins": {
    "entries": {
      "llmvision": {
        "enabled": true,
        "config": {
          "server": "http://192.168.1.123:8123",
          "token": "your_long_lived_access_token"
        }
      }
    }
  }
}
```

Uses the same Home Assistant credentials as the homeassistant plugin.

## Tools

### `llmvision_timeline_get`

Get events from the LLM Vision timeline. Returns AI-generated observation events with timestamps, summaries, and descriptions.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days` | number | Optional | Number of days to look back (default: 7). |
| `limit` | integer | Optional | Maximum number of events to return (default: 50, max: 200). |
| `start_time` | string | Optional | Start of query window as ISO 8601. |
| `end_time` | string | Optional | End of query window as ISO 8601. Defaults to now. |

### `llmvision_get_image`

Download a keyframe image from HA LLM Vision media storage. Pass a key_frame path from a timeline event. Returns the local file path.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key_frame` | string | Required | The key_frame path (e.g. /media/llmvision/snapshots/abc123-camera0.jpg). |

### `llmvision_analyze_image`

Trigger an AI image analysis on a Home Assistant camera entity using LLM Vision.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `camera_entity` | string | Required | Camera entity ID (e.g. camera.front_door). |
| `message` | string | Required | Prompt / question to send to the AI about the image. |
| `provider` | string | Required | LLM Vision provider (e.g. 'anthropic', 'openai', 'ollama'). |
| `model` | string | Optional | Specific model override. |
| `store_in_timeline` | boolean | Optional | Whether to save as a timeline event (default: false). |
| `expose_images` | boolean | Optional | Whether to expose the captured image in the timeline event. |
| `generate_title` | boolean | Optional | Whether to auto-generate a title for the timeline event. |
| `response_format` | string | Optional | Response format: 'text' (default) or 'json'. |
| `max_tokens` | integer | Optional | Maximum tokens for the AI response. |

### `llmvision_create_event`

Create a new event in the LLM Vision timeline.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Required | Title of the timeline event. |
| `description` | string | Required | Detailed description or AI summary for the event. |
| `label` | string | Optional | Optional category label (e.g. 'Person', 'Car'). |
| `image_path` | string | Optional | Optional path to an image file to attach. |
| `camera_entity` | string | Optional | Optional camera entity ID to capture an image from. |
| `start_time` | string | Optional | Event start time as ISO 8601 (defaults to now). |
| `end_time` | string | Optional | Event end time as ISO 8601 (defaults to start_time). |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/llmvision
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/llmvision.js --help

## Get events from the LLM Vision timeline. Returns AI-generated observation events with timestamps, summaries, and descriptions.
node dist/bin/llmvision.js llmvision-timeline-get <days> <limit> <start_time> <end_time>

## Download a keyframe image from HA LLM Vision media storage. Pass a key_frame path from a timeline event. Returns the local file path.
node dist/bin/llmvision.js llmvision-get-image <key_frame>

## Trigger an AI image analysis on a Home Assistant camera entity using LLM Vision.
node dist/bin/llmvision.js llmvision-analyze-image <camera_entity> <message> <provider> <model> <store_in_timeline> <expose_images> <generate_title> <response_format> <max_tokens>

## Create a new event in the LLM Vision timeline.
node dist/bin/llmvision.js llmvision-create-event <title> <description> <label> <image_path> <camera_entity> <start_time> <end_time>

## JSON output
node dist/bin/llmvision.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `LLMVISION_SERVER` | Home Assistant server URL |
| `LLMVISION_TOKEN` | Home Assistant long-lived access token |
