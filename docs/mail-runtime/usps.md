---
layout: default
title: USPS Mail Runtime
nav_exclude: true
nav_order: 3
---

# 📮 USPS Mail Action

Shared USPS Informed Delivery processing — parses digests, runs scan-image vision, applies classification rules, routes notifications, and writes mail memory.

> **Source:** [`openclaw-hub/libs/ts/mail_action_usps`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/libs/ts/mail_action_usps)

---

## Two-phase processing

| Phase | What happens |
|-------|-------------|
| **Phase 1** (mail pipeline) | `mail_rules` match a USPS digest email → fire `process_usps_digest` action |
| **Phase 2A** (vision) | Each scan image is analyzed by a vision agent → structured mailpiece data |
| **Phase 2B** (classification) | USPS rules classify importance → notifications sent → memory written |

---

## Entry points

1. **Automatic:** The mail pipeline fires `process_usps_digest` when an email matches (sender `usps.com`, subject contains "Informed Delivery")
2. **Manual:** The [`usps-mail` plugin]({{ site.baseurl }}/plugins) exposes tools like `usps_process_digest`, `usps_lookup`, and `usps_rules`

---

## Agent boundaries

| Agent | Owns |
|-------|------|
| `workspace_agent` (mail) | USPS config, rules, analysis history, workflow state |
| `vision_agent` | Scan-image staging + vision analysis |
| `memory_agent` (main) | Long-term searchable mail memory |

---

## Two rule systems

| Layer | Scope | File |
|-------|-------|------|
| Mail pipeline rules | **Per email** — when to invoke USPS processing | `fastmail-sse-config.json` |
| USPS classification rules | **Per mailpiece** — how important each scan is | `workspace/usps-mail/rules.json` |

---

## USPS classification rules

Rules live at `~/.openclaw/agents/<workspace_agent>/workspace/usps-mail/rules.json`:

```json
{
  "version": "1.2",
  "rules": [
    { "addressee_contains": "former resident", "importance": "low" },
    { "sender_contains": "county assessor", "importance": "high" }
  ]
}
```

**Operators:** `<field>_contains`, `<field>_not_contains`, `<field>_equals`, `<field>_not_equals`

**Fields:** `addressee`, `sender`, `description`, `mail_class`, `address_method`

**Evaluation:** First match wins.

**Importance levels:** `urgent`, `high`, `medium`, `low`, `junk`, `ad`, `unknown`

---

## Pipeline stages

For one digest, `process_digest(...)` runs:

1. Parse `body.html` → detect delivery date
2. Find scan images
3. Analyze each image via vision backend
4. Apply USPS classification rules
5. Persist structured history
6. Write monthly mail memory
7. Send notifications based on routing config
8. Update workflow state for dedup

---

## Notification routing

Config at `workspace/usps-mail/config.json`:

```json
{
  "routing": {
    "jeff": { "channel": "discord", "target": "<id>" },
    "nicole": { "channel": "discord", "target": "<id>" },
    "default": { "channel": "discord", "target": "<id>" }
  }
}
```

Only higher-priority pieces trigger direct notifications; lower-priority items remain in history/memory.

---

## Related

- [Mail Runtime Core]({{ site.baseurl }}/mail-runtime/shared_mail_runtime) — the rule engine that dispatches to this action
- [FastMail SSE]({{ site.baseurl }}/services/fastmail-sse) — the adapter that triggers USPS processing
- [Custom rules guide](https://github.com/JeffSteinbok/openclaw-hub/blob/main/libs/ts/mail_action_usps/docs/custom-rules.md) — detailed patterns and testing
