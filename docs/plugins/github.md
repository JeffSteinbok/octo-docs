---
layout: default
title: Github
parent: Plugins
nav_order: 3
---

🐙 Github

Manage GitHub issues. Create, read, update, close, comment on, and list issues.

### github_create_issue

Create a new issue in a GitHub repository. Acts as the authenticated OpenClaw user (GITHUB_TOKEN). Returns the issue number, URL, and state.

| Name      | Type    | Description                                              |
|-----------|---------|----------------------------------------------------------|
| owner     | string  | Repository owner (user or organisation name)             |
| repo      | string  | Repository name                                          |
| title     | string  | Issue title                                              |
| body      | string  | Issue body (Markdown supported). Defaults to empty string.|
| labels    | array   | Labels to apply to the issue (must already exist in the repo)|
| assignees | array   | GitHub usernames to assign the issue to                  |
| milestone | integer | Milestone number to associate with the issue             |

### github_get_issue

Get a single GitHub issue by its number. Returns issue details including title, body, state, labels, and assignees.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |

### github_edit_issue

Edit an existing GitHub issue. Update title, body, state, labels, assignees, or milestone. At least one field to update must be provided.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |
| title        | string  | New issue title                             |
| body         | string  | New issue body (Markdown supported)         |
| state        | string  | Issue state (open or closed)                |
| labels       | array   | Labels to apply (replaces existing labels)  |
| assignees    | array   | Assignees (replaces existing assignees)     |
| milestone    | integer | Milestone number                            |

### github_close_issue

Close or reopen a GitHub issue. By default closes the issue, set reopen=true to reopen it.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |
| reopen       | boolean | Set to true to reopen the issue instead of closing it |

### github_comment_issue

Add a comment to a GitHub issue. Returns the comment ID, body, user, and URL.

| Name         | Type    | Description                                 |
|--------------|---------|---------------------------------------------|
| owner        | string  | Repository owner (user or organisation name)|
| repo         | string  | Repository name                             |
| issue_number | integer | Issue number                                |
| body         | string  | Comment body (Markdown supported)           |

### github_list_issues

List GitHub issues with optional filters. Filter by state (open/closed/all), labels, assignee, and milestone. Returns a list of issues and the total count.

| Name      | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| owner     | string  | Repository owner (user or organisation name)        |
| repo      | string  | Repository name                                     |
| state     | string  | Filter by state (default: open)                     |
| labels    | string  | Comma-separated list of labels to filter by         |
| assignee  | string  | Filter by assignee username                         |
| milestone | string  | Filter by milestone number or '*' for any milestone |
| per_page  | integer | Results per page (default: 30, max: 100)            |
| page      | integer | Page number for pagination (default: 1)             |
