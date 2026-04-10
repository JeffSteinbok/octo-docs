---
layout: default
title: Outlook Mail
parent: Plugins
nav_order: 10
---

📧 Outlook Mail

Search and read Outlook inbox messages using the Microsoft Graph API. This plugin provides tools to list, search, read, and download attachments from Outlook emails.

### outlook_inbox

List recent messages from the Outlook inbox.

| Name   | Type     | Description                                      |
|--------|----------|--------------------------------------------------|
| limit  | integer  | Maximum number of messages to return (default 10). |
| unread | boolean  | If true, return only unread messages.            |

### outlook_search

Search Outlook messages by query text, sender, subject, or date range.

| Name    | Type     | Description                                                    |
|---------|----------|----------------------------------------------------------------|
| query   | string   | Full-text search across subject and body.                      |
| from    | string   | Filter by sender email address.                                |
| subject | string   | Filter by subject (substring match).                           |
| since   | string   | Only messages received on or after this date (YYYY-MM-DD).     |
| before  | string   | Only messages received on or before this date (YYYY-MM-DD).    |
| limit   | integer  | Maximum number of results (default 10).                        |

### outlook_read

Read a specific Outlook message by its ID, including full body content.

| Name       | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| message_id | string | The Microsoft Graph message ID to retrieve. |

### outlook_save_attachments

Download attachments from an Outlook message to a local directory. Also saves the message body as body.html. Useful for processing emails that contain inline images (e.g., USPS Informed Delivery).

| Name         | Type   | Description                                                                |
|--------------|--------|----------------------------------------------------------------------------|
| message_id   | string | The Microsoft Graph message ID.                                            |
| output_dir   | string | Local directory path to save attachments to (created if needed).           |
| content_types| array  | Content type filters (e.g. ['image/*']). Defaults to ['image/*'].          |
