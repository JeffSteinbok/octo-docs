---
layout: default
title: Usps Mail
parent: Plugins
nav_order: 15
---

📬 Usps Mail

Analyze USPS Informed Delivery digest emails by parsing mailpiece scans, performing vision classification, applying importance rules, writing memory, and sending notifications.

### usps_process_digest

Process a USPS Informed Delivery digest email. Given a folder containing body.html and mailpiece scan images, parses the HTML, vision-analyzes each image via the configured vision agent, applies importance rules, optionally writes memory, and sends routed notifications. Use vision_backend='provided' and pass an analysis array if you have already analyzed the images yourself.

| Name            | Type    | Description                                                                                                                                                                                                                 |
|-----------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| folder          | string  | Path to directory containing body.html and image files.                                                                                                                               |
| analysis        | array   | Optional pre-computed analysis. Array of objects, one per image (in filename sort order), each with: sender, addressee, description, type, importance, mail_class, address_method.     |
| date            | string  | Override delivery date (YYYY-MM-DD). Auto-detected if omitted.                                                                                                                        |
| dry_run         | boolean | If true, skip sending notifications (print instead).                                                                                                                                  |
| vision_backend  | string  | 'auto' (configured agent, default), 'provided' (use analysis arg), 'skip' (parsing only, no vision).                                                                                  |
| message_id      | string  | Outlook Graph API message ID of this digest. Used for state tracking and deduplication across runs.                                                                                   |
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                                                                                                   |
| memory_agent    | string  | Agent workspace that owns long-term mail memory markdown.                                                                                                                             |
| vision_agent    | string  | Agent that performs USPS scan-image vision analysis.                                                                                                                                  |

### usps_lookup

Search past USPS mailpiece analysis history. Find mail by partial GUID, date, or text search across all fields (sender, addressee, description).

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| guid            | string  | Partial GUID to match (first 8 chars is typical).                                                             |
| date            | string  | Date or partial date to match (YYYY-MM-DD or YYYY-MM).                                                        |
| search          | string  | Text to search for in any field.                                                                              |
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

### usps_update_rule

Add, remove, or test importance rules for USPS mail classification. Use action='add' with conditions and importance to create a new rule. Use action='remove' with index or comment_match. Use action='test' with a mailpiece dict to see which rule would match.

| Name           | Type    | Description                                                                                                   |
|----------------|---------|---------------------------------------------------------------------------------------------------------------|
| action         | string  | What to do. Values: 'add', 'remove', 'test'.                                                                 |
| conditions     | object  | Rule conditions (for 'add'). Keys like sender_contains, addressee_contains, description_not_contains, etc.     |
| importance     | string  | Target importance level (for 'add'). Values: 'urgent', 'high', 'medium', 'low', 'junk', 'ad'.                |
| comment        | string  | Human-readable description of the rule (for 'add').                                                           |
| index          | integer | Rule index to remove (for 'remove').                                                                          |
| comment_match  | string  | Remove rule whose comment contains this text (for 'remove').                                                  |
| mailpiece      | object  | Mailpiece info dict to test against rules (for 'test').                                                       |
| workspace_agent| string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

### usps_rules

List all USPS mail importance rules, or test which rule matches a specific mailpiece.

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| test_mailpiece  | object  | Optional mailpiece to test. Provide sender, addressee, etc. Returns which rule matches and the resulting importance. |
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

### usps_stats

Show statistics for all analyzed USPS mail: total pieces, delivery days, breakdown by importance, top senders, and top addressees.

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |

### usps_status

Check the USPS mail workflow state: when mail was last checked, the last processed message ID, and how many digests have been processed. Use this before polling to determine the 'since' date.

| Name            | Type    | Description                                                                                                   |
|-----------------|---------|---------------------------------------------------------------------------------------------------------------|
| workspace_agent | string  | Agent workspace that owns USPS rules, config, analysis history, and workflow state.                           |
