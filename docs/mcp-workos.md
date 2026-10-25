---
layout: default
title: WorkOS Setup
parent: MCP & OctoDot
grand_parent: External Integrations
nav_order: 1
---

# WorkOS setup

[WorkOS AuthKit](https://workos.com/docs/authkit/mcp) is the OAuth authorization server for octo-mcp. It hosts the
sign-in page, stores the account, and signs the access tokens ChatGPT presents. AuthKit is free up to 1 million monthly
active users; nothing here needs a paid feature (enterprise SSO and custom domains are the paid parts).

## Settings

Use the **Production** environment.

| Where | Setting |
|---|---|
| Connect → Configuration | **Client ID Metadata Document**: on (it's off by default) |
| Connect → Configuration | **Dynamic Client Registration**: on |
| Connect → Resource Indicators | Add `https://<funnel-host>/mcp` exactly (no trailing slash), then "…" → **Set as default** |
| Authentication | Enable **Email + Password** or **Magic Auth** |
| Users | Invite the one allowed user, then turn public sign-up off |

The AuthKit domain (`<name>.authkit.app`) is the issuer. octo-mcp is configured with it, and its public metadata shows
whether the settings took:

```bash
curl -s https://<name>.authkit.app/.well-known/oauth-authorization-server
```

Look for `client_id_metadata_document_supported: true`, a `registration_endpoint` (DCR), and `S256` in
`code_challenge_methods_supported`.

## Gotchas we hit

- **Skip the `npx workos@latest` prompt.** The dashboard pushes its installer, which wires AuthKit into a web app's
  code. octo-mcp already does its side; the Connect settings are dashboard-only.
- **"Connect" may not be obvious at first.** It's WorkOS's name for the OAuth-provider features (letting apps like
  ChatGPT sign in through you).
- **An organization invite can be SSO-only.** Inviting the user into an organization showed only "Continue with SSO".
  Enabling Email + Password (or Magic Auth) under Authentication fixed it.
- **"Sign-in successful … configure your app's sign-in callback"** after accepting the invite is harmless: that's
  WorkOS's default app, which we don't use. ChatGPT registers its own callback through CIMD/DCR.
- **The resource indicator must match the MCP URL exactly.** It becomes the token's audience, and octo-mcp rejects any
  other audience. When the server moved from port 8443 to 443, the indicator had to change too.

## Allowing a user

octo-mcp only accepts WorkOS user IDs on its allowlist (`OCTO_MCP_ALLOWED_SUBJECTS` in its LaunchAgent). To find an
ID, sign in from ChatGPT once: the attempt is refused with `403` and the log records the user ID
(`sub=user_…`). Add it, restart the service, and sign in again.
