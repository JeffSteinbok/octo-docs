---
layout: default
title: Llmvision
parent: Plugins
nav_order: 6
---

# 🖼️ Llmvision

Home Assistant LLM Vision integration enables AI-powered analysis of camera images, querying the vision timeline, and creating timeline events.

### llmvision_timeline_get

Get events from the LLM Vision timeline (calendar.llm_vision_timeline). Returns a list of AI-generated observation events with timestamps, summaries, and descriptions. Useful for reviewing what the cameras have seen recently.

| Name        | Type     | Description                                                                                   |
|-------------|----------|-----------------------------------------------------------------------------------------------|
| start_time  | string   | Start of the query window as ISO 8601 (e.g. '2026-04-09T00:00:00+00:00'). Defaults to now.    |
| end_time    | string   | End of the query window as ISO 8601. Defaults to start_time + days.                           |
| days        | integer  | Number of days ahead to include when end_time is not set (default: 7).                        |
| limit       | integer  | Maximum number of events to return (default: 50, max: 200).                                   |

### llmvision_analyze_image

Trigger an AI image analysis on a Home Assistant camera entity using LLM Vision. Sends the current camera snapshot to the specified AI provider with a custom prompt and returns the AI-generated description. Can optionally store the result in the timeline.

| Name              | Type     | Description                                                                                  |
|-------------------|----------|----------------------------------------------------------------------------------------------|
| camera_entity     | string   | Camera entity ID to analyze (e.g. camera.front_door).                                         |
| message           | string   | Prompt / question to send to the AI about the image.                                          |
| provider          | string   | LLM Vision provider to use (e.g. 'anthropic', 'openai', 'ollama').                           |
| model             | string   | Specific model override (optional, uses provider default if omitted).                        |
| store_in_timeline | boolean  | Whether to save the result as a timeline event (default: false).                              |
| expose_images     | boolean  | Whether to expose the captured image in the timeline event.                                   |
| generate_title    | boolean  | Whether to auto-generate a title for the timeline event.                                      |
| response_format   | string   | Response format from the AI: 'text' (default) or 'json'.                                      |
| max_tokens        | integer  | Maximum tokens for the AI response.                                                           |

### llmvision_create_event

Create a new event in the LLM Vision timeline. Use this to manually log observations or detections with optional camera image, label category, and time range.
