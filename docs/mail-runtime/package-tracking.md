---
layout: default
title: Package Tracking Core
nav_exclude: true
nav_order: 2
---

# 📦 Package Tracking Core

Shared package tracking logic used by the mail runtime's `detect_tracking` action and the `package-tracking` plugin. Handles carrier detection, tracking URL generation, and package storage.

> **Source:** [`openclaw-hub/libs/ts/package_tracking_core`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/libs/ts/package_tracking_core)

---

## How it works in the mail pipeline

When `detect_tracking` fires on an incoming email:

1. **Sender allowlist check** — only known shipping senders are scanned
2. **Regex scan** — body text checked for carrier tracking patterns
3. **URL extraction** — tracking numbers parsed from embedded shipping URLs
4. **Narvar fetch** — if a Narvar link exists without inline tracking, the page is fetched
5. **Auto-add** — found packages are registered in tracking
6. **Auto-remove** — delivery confirmation emails remove the package

---

## Built-in carrier patterns

| Carrier | Pattern |
|---------|---------|
| UPS | `1Z[A-Z0-9]{16}` |
| FedEx | 12, 15, or 20-digit numbers |
| USPS | 20-22 digits (starts with 94, 92, 93, or 95) |

---

## Shipping sender allowlist

Emails from these senders trigger scanning:

`ups.com` · `fedex.com` · `usps.com` · `dhl.com` · `ontrac.com` · `lasership.com` · `amazon.com` · `amazonlogistics.com` · `narvar.com` · `aftership.com` · `shipbob.com` · `shipstation.com` · `easypost.com` · `noreply@nespresso.com`

---

## URL extraction patterns

| Source | Tracking parameter |
|--------|-------------------|
| `narvar.com/…` | `?tracking_numbers=…` |
| `ups.com/track…` | `?tracknum=…` |
| `fedex.com/…track…` | `?trknbr=…` |
| `usps.com/…` | `?qtc_tLabels1=…` |

---

## Public API

| Function | Purpose |
|----------|---------|
| `detect_carrier(number)` | Identify carrier from tracking number |
| `get_tracking_url(number, carrier)` | Generate browser-friendly tracking URL |
| `scan_text_for_tracking_numbers(text)` | Regex scan for all carriers |
| `extract_tracking_from_urls(html)` | Parse tracking from embedded URLs |
| `add_package(pkg)` | Register a package for tracking |
| `remove_package(number)` | Remove a delivered package |
| `list_packages()` | List all tracked packages |
| `is_shipping_sender(email)` | Check sender against allowlist |

---

## Pluggable status providers

The plugin supports carrier status providers for live tracking lookups. Providers are external ESM modules:

```typescript
export const register = (registry) => {
  registry.register({
    name: 'MyCarrier',
    carriers: ['MyCarrier'],
    async getStatus(trackingNumber) {
      return { tracking_number: trackingNumber, carrier: 'MyCarrier', status: 'In Transit', delivered: false };
    },
  });
};
```

Load via config: `"status_providers": ["/path/to/provider/dist/index.js"]`

> See the full [carrier providers guide](https://github.com/JeffSteinbok/openclaw-hub/blob/main/libs/ts/package_tracking_core/carrier-providers.md) for interface details and examples.

---

## Storage

Packages are stored in `~/.openclaw/package_tracking.json` — a flat JSON file managed by the core library.

---

## Related

- [Mail Runtime Core]({{ site.baseurl }}/mail-runtime/shared_mail_runtime) — rule engine that fires `detect_tracking`
- [USPS Mail Runtime]({{ site.baseurl }}/mail-runtime/usps) — separate USPS-specific processing
- [FastMail SSE]({{ site.baseurl }}/services/fastmail-sse) — extraction pipeline details
