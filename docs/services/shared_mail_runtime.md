---
layout: default
title: Shared Mail Runtime
parent: Services
nav_order: 2
---

# Shared Mail Runtime

Provider-agnostic mail processing runtime used by OpenClaw's mail pipeline. Provides a normalized envelope model, rule matching engine, action registry, and dispatch loop that any mail source (Fastmail SSE, Outlook, etc.) can plug into.

## Features

- **MailEnvelope** — Normalized message shape consumed by rules and actions
- **Rule engine** — Declarative JSON rules with match conditions (sender, subject, domain, regex, attachments, body)
- **Action registry** — Named action handlers with automatic body fetching and attachment downloading
- **Provider protocol** — `MailProviderClient` interface that sources implement to plug into the pipeline

## How provider-agnostic mail works

The shared runtime separates **where mail comes from** from **what OpenClaw does with it**.

- A provider-specific adapter translates raw provider events into a `MailEnvelope`
- The runtime evaluates the same ordered `mail_rules` regardless of provider
- Named actions run against the normalized envelope, not provider-native payloads
- If an action needs more provider data later, it asks the adapter through `MailProviderClient`

That means FastMail SSE, an Outlook poller, or a webhook source can all reuse the same rule engine and action handlers as long as they:

1. identify new messages
2. build a `MailEnvelope`
3. implement the `MailProviderClient` methods
4. pass rules + actions into `execute_rules(...)`

## Provider-agnostic flow

```mermaid
flowchart LR
    raw["Provider event / message<br/>(FastMail, Outlook, etc.)"]
    adapter["Provider adapter"]
    envelope["MailEnvelope<br/>normalized message"]
    rules["Shared rule matcher<br/>providers/accounts/mailboxes/match"]
    actions["Shared action execution"]
    results["ActionResult(s)"]

    subgraph provider["Provider-specific surface"]
        fetch["fetch_body(...)"]
        list["list_attachments(...)"]
        download["download_attachments(...)"]
    end

    raw --> adapter --> envelope --> rules --> actions --> results
    actions -. lazy provider access .-> fetch
    actions -. attachment access .-> list
    actions -. artifact download .-> download
```

## Source adapter contract

A mail source stays provider-specific only at the edges:

| Adapter responsibility | What it does |
|------|-------------|
| Detect new mail | Poll, stream, or receive provider events |
| Normalize message | Map raw provider fields into `MailEnvelope` |
| Provide lazy access | Implement `MailProviderClient` for body/attachment fetches |
| Register actions | Expose actions like `notify_email`, `detect_tracking`, `process_usps_digest` |
| Dispatch results | Decide how `ActionResult` values become side effects |

In practice, the adapter owns transport and provider APIs; the shared runtime owns matching and action orchestration.

## USPS Subpackage

The `usps/` subpackage implements the full USPS Informed Delivery digest pipeline:

| Module | Purpose |
|--------|---------|
| `parse_digest.py` | Parse Informed Delivery HTML into structured mailpiece data |
| `analyze.py` | Orchestrate digest processing: parse → vision → rules → notify |
| `vision.py` | AI-powered scan image analysis via agent backends |
| `rules.py` | Importance classification rule engine (CRUD + evaluation) |
| `memory.py` | Persistence layer: analysis state, monthly memory files, lookups |
| `notify.py` | Notification routing and delivery via `openclaw message send` |
| `paths.py` | Central path helpers for workspace, memory, and config files |

## Key Types

| Type | Description |
|------|-------------|
| `MailEnvelope` | Normalized message with sender, subject, body, headers, attachments |
| `ActionContext` | Runtime context passed to action handlers (envelope, provider, workspace) |
| `ActionResult` | Structured side effect emitted by an action |
| `MailProviderClient` | Protocol that mail sources implement (fetch body, list/download attachments) |
| `ActionRegistry` | Registry and executor for named mail actions |

### `MailEnvelope`

`MailEnvelope` is the stable contract between providers, rules, and actions. The fields are intentionally generic:

| Field | Meaning |
|------|---------|
| `provider` | Source identifier such as `fastmail` or `outlook` |
| `account_id` | Provider account/mailbox owner identifier |
| `mailbox_id` | Folder/inbox identifier within that provider |
| `sender_name` / `sender_email` | Canonical sender identity |
| `subject` | Normalized subject line |
| `body_text` / `body_html` | Optional body content; can be preloaded or fetched lazily |
| `has_attachments` | Cheap attachment hint for rule matching |
| `raw` | Original provider payload for adapter-specific follow-up |

An action should prefer the normalized fields first and only reach into `raw` when it truly needs provider-specific detail.

### `MailProviderClient`

`MailProviderClient` is the escape hatch for provider-specific I/O without polluting the shared runtime:

- `fetch_body(...)` fills in missing `body_text` / `body_html`
- `list_attachments(...)` exposes lightweight attachment metadata
- `download_attachments(...)` materializes filtered artifacts into a workspace directory

This keeps rule evaluation fast while still letting expensive provider calls happen only when an action requests them.

## Rule Matching

Rules are evaluated in order. Each rule can filter by provider, account, mailbox, and a `match` block supporting:

| Condition | Description |
|-----------|-------------|
| `sender_email` | Exact sender email match |
| `sender_domain` | Domain match (including subdomains) |
| `sender_name_contains` | Substring match on sender name |
| `subject` | Exact subject match |
| `subject_contains` | Substring match on subject |
| `subject_prefix` | Subject starts with value |
| `subject_regex` | Regex match on subject |
| `body_contains` | Substring match on body text/HTML |
| `has_attachments` | Boolean attachment presence check |

By default, processing stops at the first matching rule. Set `"continue": true` on a rule to allow fall-through.

## `mail_rules` shape

The shared runtime expects an ordered list of rule objects. A source adapter decides where that config lives, but the runtime consumes the same structure everywhere.

```json
{
  "mail_rules": [
    {
      "id": "rule-id",
      "providers": ["fastmail"],
      "accounts": ["<account-id>"],
      "mailboxes": ["<mailbox-id>"],
      "match": {
        "sender_domain": "example.com",
        "subject_contains": ["Invoice", "Receipt"]
      },
      "actions": [
        {"name": "notify_email"}
      ],
      "continue": false
    }
  ]
}
```

Common top-level rule fields:

| Field | Meaning |
|------|---------|
| `id` | Human-readable rule identifier for logs/debugging |
| `enabled` | Optional boolean; disabled rules are skipped |
| `providers` | Optional provider filter such as `fastmail` or `outlook` |
| `accounts` | Optional provider-account filter |
| `mailboxes` | Optional mailbox/folder filter |
| `match` | Declarative condition block |
| `actions` | Ordered action list to run when the rule matches |
| `continue` | Keep evaluating later rules after this one |

## Action configuration

Actions can be declared as either a bare name or a `{name, params}` object:

```json
{
  "actions": [
    "notify_email",
    {
      "name": "handoff_to_agent",
      "params": {
        "agent": "main"
      }
    }
  ]
}
```

The shared runtime does not define which action names exist. Each source adapter registers the actions it supports.

## Common rule examples

These examples show the **generic rule structure**. Actual action availability depends on the integrating service.

### Catch-all notification after a more specific action

```json
{
  "mail_rules": [
    {
      "id": "detect-tracking",
      "accounts": ["<account-id>"],
      "actions": [{"name": "detect_tracking"}],
      "continue": true
    },
    {
      "id": "notify-all",
      "accounts": ["<account-id>"],
      "actions": [{"name": "notify_email"}]
    }
  ]
}
```

Put the more specific rule first and set `"continue": true` if both behaviors should run for the same message.

### Meeting-response notifications only

```json
{
  "mail_rules": [
    {
      "id": "notify-meeting-updates",
      "accounts": ["<account-id>"],
      "match": {
        "subject_prefix": ["accepted:", "declined:", "tentative:"]
      },
      "actions": [{"name": "notify_email"}]
    }
  ]
}
```

### Provider-specific override plus generic fallback

```json
{
  "mail_rules": [
    {
      "id": "usps-fastmail",
      "providers": ["fastmail"],
      "match": {
        "sender_domain": "usps.com",
        "subject_contains": ["Informed Delivery", "Daily Digest"]
      },
      "actions": [{"name": "process_usps_digest"}],
      "continue": true
    },
    {
      "id": "notify-all",
      "actions": [{"name": "notify_email"}]
    }
  ]
}
```

This pattern is useful when one provider exposes richer metadata or special actions, but you still want a generic fallback rule afterwards.

## Action execution model

`execute_rules(...)` does four things:

1. selects matching rules in order
2. creates an `ActionContext` for each action
3. lazily fetches bodies and/or downloads attachments if the action declared those needs
4. returns collected `ActionResult` values to the source adapter

The runtime itself does not send notifications, call agents, or mutate provider state directly. Those side effects are represented as `ActionResult` values and interpreted by the integrating service.

## Why this split exists

Without the shared runtime, every mail source would need to reimplement:

- subject/body matching
- rule ordering and fall-through
- lazy body fetching
- attachment staging
- action registration

The provider-agnostic layer keeps that logic in one place, so adding a new source is mostly an adapter problem instead of a full pipeline rewrite.
