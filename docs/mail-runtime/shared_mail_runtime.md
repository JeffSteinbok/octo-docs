---
layout: default
title: Mail Runtime Core
nav_exclude: true
nav_order: 1
---

# 📬 Mail Runtime Core

Provider-agnostic mail processing runtime. Separates **where mail comes from** from **what OpenClaw does with it** — any mail source (FastMail, Outlook, webhooks) shares the same rule engine and action handlers.

> **Source:** [`openclaw-hub/libs/ts/mail_runtime_core`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/libs/ts/mail_runtime_core)

---

## How it works

1. A **provider adapter** (e.g. FastMail SSE) detects new mail and builds a `MailEnvelope`
2. The **rule engine** evaluates `mail_rules` top-to-bottom
3. Matched rules fire **actions** — named handlers in the `ActionRegistry`
4. Actions return **`ActionResult`** values (notifications, agent handoffs, tracking updates)
5. The adapter **dispatches** results into real side effects

> The runtime never sends notifications directly. All side effects flow through `ActionResult` values that the adapter interprets.

---

## MailEnvelope

The normalized message shape shared by rules and actions:

| Field | Type | Description |
|-------|------|-------------|
| `provider` | `string` | Source identifier (`"fastmail"`, `"outlook"`) |
| `account_id` | `string` | Provider account/mailbox owner |
| `message_id` | `string` | Unique message identifier |
| `sender_name` | `string` | Display name of sender |
| `sender_email` | `string` | Email address of sender |
| `subject` | `string` | Normalized subject line |
| `body_text` | `string?` | Plain text body (lazy-loaded) |
| `body_html` | `string?` | HTML body (lazy-loaded) |
| `has_attachments` | `boolean` | Cheap hint for rule matching |
| `auth_results` | `AuthResults?` | Parsed DKIM/SPF/DMARC |
| `headers` | `Record<string, string>` | Normalized headers |

---

## Rule Engine

Rules are declarative JSON — no code required:

```json
{
  "id": "shipping-tracking",
  "match": {
    "sender_domain": ["fedex.com", "ups.com", "usps.com"]
  },
  "actions": [{ "name": "detect_tracking" }],
  "continue": true
}
```

### Match conditions

| Condition | Description |
|-----------|-------------|
| `sender_email` | Exact email match |
| `sender_domain` | Domain match (includes subdomains) |
| `sender_name_contains` | Substring on display name |
| `subject_contains` | Substring on subject |
| `subject_prefix` | Subject starts with |
| `subject_regex` | Regex match |
| `body_contains` | Substring on body |
| `has_attachments` | Boolean |
| `dkim_pass` | Require DKIM authentication |
| `spf_pass` | Require SPF authentication |
| `dmarc_pass` | Require DMARC authentication |

### Evaluation

- Rules evaluate **top to bottom**
- First match fires; processing **stops** unless `"continue": true`
- Multiple rules can fire for the same message via `continue`

---

## Actions

### Registered actions

| Action | Source | Description |
|--------|--------|-------------|
| `notify_email` | Built-in | Formats envelope into a notification message |
| `detect_tracking` | Built-in | Scans body for tracking numbers/URLs, manages packages |
| `process_usps_digest` | Library | USPS Informed Delivery: downloads images, runs vision, sends alerts |
| `process_amazon_shipment` | External plugin | Amazon shipping: extracts order IDs + tracking |
| `process_self_email` | External plugin | Self-sent email: hands off body as a task |

### Action types

| Type | How registered |
|------|---------------|
| **Built-in** | `registerBuiltinActions()` at service startup |
| **Library** | Shared library's `register()` export (e.g. `mail_action_usps`) |
| **External plugin** | Loaded from `action_plugins` paths in config |

> External plugins don't need to live in openclaw-hub. Any ESM module exporting `register(registry)` works.

### ActionResult kinds

| Kind | Side effect |
|------|-------------|
| `message` | Discord/Telegram notification |
| `agent_handoff` | Agent session created |
| `tracking_update` | Package list updated |

---

## Authentication (DKIM/SPF/DMARC)

The envelope carries parsed `Authentication-Results`, enabling rules to gate actions on email authenticity:

```json
{
  "id": "self-email-command",
  "match": {
    "sender_email": "me@example.com",
    "dkim_pass": true,
    "spf_pass": true
  },
  "actions": [{ "name": "process_self_email" }]
}
```

**Why this matters:** Without DKIM/SPF checks, an attacker could forge a `From:` header and trigger sensitive actions through your assistant.

---

## Provider Protocol

Adapters implement `MailProviderClient`:

| Method | Purpose |
|--------|---------|
| `fetch_body(envelope)` | Fills in body (called lazily when action needs it) |
| `list_attachments(envelope)` | Returns attachment metadata |
| `download_attachments(envelope, filter, dir)` | Materializes files to disk |

This keeps rule evaluation fast — expensive provider calls only happen when actions explicitly request them.

---

## Writing a Custom Action

```typescript
import type { ActionPlugin, ActionRegistry } from '@openclaw/mail-runtime-core';

export const register: ActionPlugin['register'] = (registry) => {
  registry.register('my_action', async (ctx, params) => {
    const body = await ctx.fetchBody();
    return [{ kind: 'message', payload: { text: `Got: ${ctx.envelope.subject}` } }];
  }, { needs_body: true });
};
```

Load via config:
```json
{
  "action_plugins": ["/path/to/my-plugin/dist/index.js"]
}
```

---

## Config hot-reload

The [FastMail SSE service]({{ site.baseurl }}/services/fastmail-sse) watches the config file and hot-reloads `mail_rules` without restart. Adding new `action_plugins` or `accounts` still requires a restart.

---

## Related

- [Package Tracking Core]({{ site.baseurl }}/mail-runtime/package-tracking) — carrier detection and tracking storage
- [USPS Mail Runtime]({{ site.baseurl }}/mail-runtime/usps) — USPS digest processing action
- [FastMail SSE]({{ site.baseurl }}/services/fastmail-sse) — primary provider adapter
