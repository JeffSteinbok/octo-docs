---
layout: default
title: USPS Mail Analyzer
nav_order: 17
nav_exclude: true
---

# 📬 USPS Mail Analyzer

Analyze USPS Informed Delivery digest emails: parse mailpiece scans, vision-classify, apply rules, write memory, send notifications

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail)

## Configuration Schema

_No plugin config schema documented._

## Tools

### `usps_process_digest`

Process a USPS Informed Delivery digest folder and classify each mailpiece.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `folder` | string | Required | Path to directory containing body.html and image files. |
| `workspace_agent` | string | Required | Agent workspace that owns USPS rules, config, analysis history, and workflow state. |
| `analysis` | array | Optional | Optional pre-computed analysis. Array of objects, one per image (in filename sort order), each with: sender, addressee, description, type, importance, mail_class, address_method. |
| `date` | string | Optional | Override delivery date (YYYY-MM-DD). Auto-detected if omitted. |
| `dry_run` | boolean | Optional | If true, skip sending notifications (print instead). |
| `vision_backend` | string | Optional | 'auto' (configured agent, default), 'provided' (use analysis arg), 'skip' (parsing only, no vision). |
| `message_id` | string | Optional | Outlook Graph API message ID of this digest. Used for state tracking and deduplication across runs. |
| `memory_agent` | string | Optional | Agent workspace that owns long-term mail memory markdown. |
| `vision_agent` | string | Optional | Agent that performs USPS scan-image vision analysis. Required when vision_backend is auto. |

### `usps_lookup`

Search saved USPS mail history by GUID, date, or text.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `workspace_agent` | string | Required | Agent workspace that owns USPS rules, config, analysis history, and workflow state. |
| `guid` | string | Optional | Partial GUID to match (first 8 chars is typical). |
| `date` | string | Optional | Date or partial date to match (YYYY-MM-DD or YYYY-MM). |
| `search` | string | Optional | Text to search for in any field. |

### `usps_update_rule`

Add, remove, or test USPS mail classification rules.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | string | Required | What to do. |
| `workspace_agent` | string | Required | Agent workspace that owns USPS rules, config, analysis history, and workflow state. |
| `conditions` | object | Optional | Rule conditions (for 'add'). Keys like sender_contains, addressee_contains, description_not_contains, etc. |
| `importance` | string | Optional | Target importance level (for 'add'). |
| `comment` | string | Optional | Human-readable description of the rule (for 'add'). |
| `index` | integer | Optional | Rule index to remove (for 'remove'). |
| `comment_match` | string | Optional | Remove rule whose comment contains this text (for 'remove'). |
| `mailpiece` | object | Optional | Mailpiece info dict to test against rules (for 'test'). |

### `usps_rules`

List USPS classification rules or test a sample mailpiece.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `workspace_agent` | string | Required | Agent workspace that owns USPS rules, config, analysis history, and workflow state. |
| `test_mailpiece` | object | Optional | Optional mailpiece to test. Provide sender, addressee, etc. Returns which rule matches and the resulting importance. |

### `usps_stats`

Show summary statistics for processed USPS mail.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `workspace_agent` | string | Required | Agent workspace that owns USPS rules, config, analysis history, and workflow state. |

### `usps_status`

Show the current USPS mail workflow state.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `workspace_agent` | string | Required | Agent workspace that owns USPS rules, config, analysis history, and workflow state. |
