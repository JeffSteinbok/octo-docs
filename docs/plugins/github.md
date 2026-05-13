---
layout: default
title: GitHub
nav_order: 2
nav_exclude: true
---

# 🐙 GitHub

Manage GitHub issues. Create, read, update, close, comment on, and list issues.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>token</code></td><td>string</td><td>Optional</td><td>GitHub personal access token or fine-grained token.</td></tr>
  </tbody>
</table>

## Example config

Set credentials in `plugins.entries["github"].config`:

```json
{
  "plugins": {
    "entries": {
      "github": {
        "enabled": true,
        "config": {
          "token": "ghp_your_personal_access_token"
        }
      }
    }
  }
}
```

## Tools

### `github_list_issues`

List GitHub issues with optional filters. Filter by state (open/closed/all), labels, assignee, and milestone. Returns a list of issues and the total count.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `state` | string | Optional | Filter by state (default: open). |
| `labels` | string | Optional | Comma-separated list of labels to filter by. |
| `assignee` | string | Optional | Filter by assignee username. |
| `milestone` | string | Optional | Filter by milestone number or '*' for any milestone. |
| `per_page` | integer | Optional | Results per page (default: 30, max: 100). |
| `page` | integer | Optional | Page number for pagination (default: 1). |

### `github_get_issue`

Get a single GitHub issue by its number. Returns issue details including title, body, state, labels, and assignees.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `issue_number` | integer | Required | Issue number. |

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

### `github_edit_issue`

Edit an existing GitHub issue. Update title, body, state, labels, assignees, or milestone. At least one field to update must be provided.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner` | string | Required | Repository owner (user or organisation name). |
| `repo` | string | Required | Repository name. |
| `issue_number` | integer | Required | Issue number. |
| `title` | string | Optional | New issue title. |
| `body` | string | Optional | New issue body (Markdown supported). |
| `state` | string | Optional | Issue state (open or closed). |
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

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/github
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/github.js --help

## List GitHub issues with optional filters. Filter by state (open/closed/all), labels, assignee, and milestone. Returns a list of issues and the total count.
node dist/bin/github.js github-list-issues <owner> <repo> <state> <labels> <assignee> <milestone> <per_page> <page>

## Get a single GitHub issue by its number. Returns issue details including title, body, state, labels, and assignees.
node dist/bin/github.js github-get-issue <owner> <repo> <issue_number>

## Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.
node dist/bin/github.js github-create-issue <owner> <repo> <title> <body> <labels...> <assignees...> <milestone>

## Edit an existing GitHub issue. Update title, body, state, labels, assignees, or milestone. At least one field to update must be provided.
node dist/bin/github.js github-edit-issue <owner> <repo> <issue_number> <title> <body> <state> <labels...> <assignees...> <milestone>

## Close or reopen a GitHub issue. By default closes the issue, set reopen=true to reopen it.
node dist/bin/github.js github-close-issue <owner> <repo> <issue_number> <reopen>

## Add a comment to a GitHub issue. Returns the comment ID, body, user, and URL.
node dist/bin/github.js github-comment-issue <owner> <repo> <issue_number> <body>

## JSON output
node dist/bin/github.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub personal access token or fine-grained token |
