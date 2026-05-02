---
layout: default
title: GitHub
parent: Plugins
nav_order: 3
---

# 🐙 GitHub

Manage GitHub issues. Create, read, update, close, comment on, and list issues.

## Configuration Schema

_No plugin config schema documented._

## Example config

No additional configuration is required in `openclaw.json` beyond adding the plugin to `plugins.load.paths`.

## Tools

### `github_create_issue`

Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `title` | string | Required | Issue title. |
| `body` | string | Optional | Issue body (Markdown supported). Defaults to empty string. |
| `labels` | array | Optional | Labels to apply to the issue (must already exist in the repo). |
| `assignees` | array | Optional | GitHub usernames to assign the issue to. |
| `milestone` | integer | Optional | Milestone number to associate with the issue. |

### `github_get_issue`

Get a single GitHub issue by its number. Returns issue details including title, body, state, labels, and assignees.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `issue_number` | integer | Required | Issue number. |

### `github_edit_issue`

Edit an existing GitHub issue. Update title, body, state, labels, assignees, or milestone. At least one field to update must be provided.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `issue_number` | integer | Required | Issue number. |
| `title` | string | Optional | New issue title. |
| `body` | string | Optional | New issue body (Markdown supported). |
| `state` | string | Optional | Issue state (open or closed). Allowed: `open`, `closed`. |
| `labels` | array | Optional | Labels to apply (replaces existing labels). |
| `assignees` | array | Optional | Assignees (replaces existing assignees). |
| `milestone` | integer | Optional | Milestone number. |

### `github_close_issue`

Close or reopen a GitHub issue. By default closes the issue, set reopen=true to reopen it.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `issue_number` | integer | Required | Issue number. |
| `reopen` | boolean | Optional | Set to true to reopen the issue instead of closing it. |

### `github_comment_issue`

Add a comment to a GitHub issue. Returns the comment ID, body, user, and URL.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `issue_number` | integer | Required | Issue number. |
| `body` | string | Required | Comment body (Markdown supported). |

### `github_list_issues`

List GitHub issues with optional filters. Filter by state (open/closed/all), labels, assignee, and milestone. Returns a list of issues and the total count.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `state` | string | Optional | Filter by state (default: open). Allowed: `open`, `closed`, `all`. |
| `labels` | string | Optional | Comma-separated list of labels to filter by. |
| `assignee` | string | Optional | Filter by assignee username. |
| `milestone` | string | Optional | Filter by milestone number or '*' for any milestone. |
| `per_page` | integer | Optional | Results per page (default: 30, max: 100). |
| `page` | integer | Optional | Page number for pagination (default: 1). |
