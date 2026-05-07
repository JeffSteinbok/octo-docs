---
layout: default
title: Outlook Mail
nav_order: 11
nav_exclude: true
---

# 📧 Outlook Mail

Search and read messages from Outlook inboxes

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/outlook-mail)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 client secret.</td></tr>
    <tr><td><code>refreshToken</code></td><td>string</td><td>Optional</td><td>Microsoft Graph OAuth2 refresh token.</td></tr>
  </tbody>
</table>

## Example config

Set Outlook Mail under `plugins.entries["outlook-mail"].config`:

```json
{
  "plugins": {
    "entries": {
      "outlook-mail": {
        "enabled": true,
        "config": {
          "clientId": "${OUTLOOK_CLIENT_ID}",
          "clientSecret": "${OUTLOOK_CLIENT_SECRET}",
          "refreshToken": "${OUTLOOK_REFRESH_TOKEN}"
        }
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OUTLOOK_CLIENT_ID` | No | Backing value for plugin config `clientId |
| `OUTLOOK_CLIENT_SECRET` | No | Backing value for plugin config `clientSecret |
| `OUTLOOK_REFRESH_TOKEN` | No | Backing value for plugin config `refreshToken |

## Tools

### `outlook_inbox`

List recent messages from the Outlook inbox, or any other mail folder.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `limit` | integer | Optional | Maximum number of messages to return (default 10). |
| `unread` | boolean | Optional | Only show unread messages. |
| `folder` | string | Optional | Mail folder to read (default: inbox). Well-known folder names: inbox, junkemail, deleteditems, sentitems, drafts, outbox, archive. |

### `outlook_search`

Search Outlook messages by query text, sender, subject, or date range.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Optional | Full-text search across subject and body. |
| `from` | string | Optional | Filter by sender email address. |
| `subject` | string | Optional | Filter by subject (substring match). |
| `since` | string | Optional | Only messages received on or after this date (YYYY-MM-DD). |
| `before` | string | Optional | Only messages received on or before this date (YYYY-MM-DD). |
| `limit` | integer | Optional | Maximum number of results (default 10). |

### `outlook_read`

Read a specific Outlook message by its ID, including full body content.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message_id` | string | Required | The Microsoft Graph message ID to retrieve. |

### `outlook_save_attachments`

Download attachments from an Outlook message to a local directory.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message_id` | string | Required | The Microsoft Graph message ID. |
| `output_dir` | string | Required | Local directory path to save attachments to (created if needed). |
| `content_types` | array | Optional | Content type filters (e.g. ['image/*']). Defaults to ['image/*']. |
