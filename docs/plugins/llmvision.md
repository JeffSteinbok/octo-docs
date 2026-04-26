---
layout: default
title: "Home Assistant \u2013 LLM Vision"
parent: Plugins
nav_order: 5
---

# 🖼️ Home Assistant – LLM Vision

Home Assistant LLM Vision integration: analyze camera images with AI, query the vision timeline, and create timeline events.

### `llmvision_get_image`

Download a keyframe image from HA LLM Vision media storage. Pass a key_frame path from a timeline event (e.g. /media/llmvision/snapshots/xxx.jpg). Returns the local file path for use with the image or message tools.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key_frame` | string | Required | The key_frame path from a timeline event (e.g. /media/llmvision/snapshots/abc123-camera0.jpg). |

### `llmvision_timeline_get`

Get events from the LLM Vision timeline (calendar.llm_vision_timeline). Returns a list of AI-generated observation events with timestamps, summaries, and descriptions. Useful for reviewing what the cameras have seen recently.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `start_time` | string | Optional | Start of the query window as ISO 8601 (e.g. '2026-04-09T00:00:00+00:00'). Defaults to now minus days. |
| `end_time` | string | Optional | End of the query window as ISO 8601. Defaults to now. |
| `days` | integer | Optional | Number of days to look back when start_time is not set (default: 7). |
| `limit` | integer | Optional | Maximum number of events to return (default: 50, max: 200). |

### `llmvision_analyze_image`

Trigger an AI image analysis on a Home Assistant camera entity using LLM Vision. Sends the current camera snapshot to the specified AI provider with a custom prompt and returns the AI-generated description. Can optionally store the result in the timeline.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `camera_entity` | string | Required | Camera entity ID to analyze (e.g. camera.front_door). |
| `message` | string | Required | Prompt / question to send to the AI about the image. |
| `provider` | string | Required | LLM Vision provider to use (e.g. 'anthropic', 'openai', 'ollama'). |
| `model` | string | Optional | Specific model override (optional, uses provider default if omitted). |
| `store_in_timeline` | boolean | Optional | Whether to save the result as a timeline event (default: false). |
| `expose_images` | boolean | Optional | Whether to expose the captured image in the timeline event. |
| `generate_title` | boolean | Optional | Whether to auto-generate a title for the timeline event. |
| `response_format` | string | Optional | Response format from the AI: 'text' (default) or 'json'. Allowed: `text`, `json`. |
| `max_tokens` | integer | Optional | Maximum tokens for the AI response. |

### `llmvision_create_event`

Create a new event in the LLM Vision timeline. Use this to manually log observations or detections with optional camera image, label category, and time range.
