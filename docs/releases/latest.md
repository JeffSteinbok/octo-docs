---
layout: default
title: Release Notes
nav_order: 11
---

# Release Notes

## 2026-07-07


### Added

- **Strict plugin manifest validation** — unknown keys, missing required fields (`origin`, `name`, `summary`, `docsMode`), and bad `docsMode` values now fail the docs build instead of being silently skipped or mis-bucketed.
- **Glances service** — documented as a third-party service (server run outside OpenClaw).
- **About These Docs page** — new static-markdown doc page spec (`tools/docs/page_specs/about-docs.yml`).
- **Docs pipeline guide** (`docs/DOCS-PIPELINE.md`) — end-user reference for the extract → render → publish flow.
- **Mail model A/B replay script** (`scripts/mail-model-ab-replay/`) — tooling for replaying mail through different models for evaluation.

### Changed

- **OPENCLAW_CONFIG.md model roles table** — rewritten to match current `config/openclaw.json` (primary `claude-sonnet-4.6`, fallback `gpt-5.4`, image gen `gemini-3-pro-image-preview`, alias `sonnet`).
- **OPENCLAW_CONFIG.md voice/talk config** — documented TTS (Azure Speech, `en-US-AndrewMultilingualNeural`), realtime voice (`gpt-realtime-mini`, WebRTC), and STT (`azure-stt`).
- **Docs nav order** — reordered page specs: Skills→5, CLI Tools→6, Services→7, Hooks→8, Scheduled Tasks→9, Release Notes→11.
- **Services page** — service emoji split into its own column for improved readability.
- **External plugin classification** — author/repository now read from `doc-manifest.json` only (not `openclaw.plugin.json`), fixing obsidian-vault (`carapace-obsidian`) being silently dropped from the plugins page.
- **`config-backup` plugin** — now backs up the `safebin/` directory alongside the OpenClaw config.
- **`static-markdown` strategy** — added to the docs render pipeline for pages that embed a static markdown file as-is.

### Fixed

- **Goodreads plugin manifest** — entry was malformed (`source`/`repo`/`description` keys instead of the standard `origin`/`name`/`summary` shape); now renders correctly in Open Source with a working GitHub link.
- **GitHub plugin `getIssue` / `formatIssue`** — issue body was fetched from the GitHub API but never returned to the tool caller; now included in `IssueResponse`.

## 2026-07-03


### Added

- **Weekly agent-review skill** — periodic self-improvement analysis that reviews recent activity and surfaces suggested improvements.
- **Home Assistant Lovelace dashboard tools** (openclaw-hub) — read and write Lovelace dashboard configuration.

### Changed

- **Docs rendering moved into `octo`** — the bundle pipeline now extracts, sanitizes, **renders the final Jekyll Markdown pages**, and validates them, publishing a `docs-site` artifact and dispatching `docs-site-ready`. Removed dead change-mapping code and stale page specs.
- **`octo-docs` simplified to receive-and-deploy** — dropped ~3,000 lines of local rendering; it now downloads the rendered `docs-site` artifact, secret-scans it, and deploys to GitHub Pages.
- **obsidian-vault split** (openclaw-hub) — refactored into a standalone indexer service plus a read-only plugin.

### Fixed

- **ha-smb skill** — redacted a hardcoded private Home Assistant IP that failed public-bundle validation; reference `HA_SMB_HOST` instead.
- **Docs validation crash** — fixed a `relative_to` error that masked real validation failures with a traceback.
- **GitHub Pages deploy race** — moved the `pages` concurrency guard to the deploy job (top-level concurrency is ignored in reusable workflows), fixing intermittent "Deployment failed, try again later" errors.
- **ReDoS hardening** (openclaw-hub) — replaced regex patterns vulnerable to catastrophic backtracking, including in md-to-html.

### Dependencies

- Routine updates across `octo` and `openclaw-hub`: vite, vitest, esbuild, tsx, @types/node, nodemailer/mailparser, carapace-package-tracking, and `actions/checkout` v7.

## 2026-06-03


### Added

- **Obsidian Vault plugin** — read-only access to an Obsidian vault with 6 tools: search, read, recent, tags, backlinks, related notes. Full-text search via FTS5, symlink-safe path resolution.
- **Fastmail threading support** — `In-Reply-To` and `References` headers in `fastmail_send` for proper email reply threading.
- **`monarch_get_investments`** tool in octo-satellite — query investment holdings from Monarch Money.
- **Mail-actions improvements** — quote original email in self-email replies, Discord DM notifications after sending replies, proper reply-all parsing, Message-ID passthrough for threading.
- **Full backup script** — `scripts/backup.sh` for complete system backup.
- **Carapace Plugin SDK** — initial release through 1.0.4 on npm. Includes CLI generation, source metadata injection, contracts auto-discovery, npm trusted publishing, and `definePluginEntry()` contracts preservation fix.
- **Carapace Package Tracking** — URL-first extraction to reduce false-positive tracking detection, OIDC trusted publishing, released through 1.0.4.
- **Doc-manifest entries** for obsidian-vault and screenshot-capture plugins.

### Changed

- **Docs pipeline decoupled** from openclaw-hub — external plugin/service configs, doc-manifest is now the single source of truth for plugin inventory.
- **openclaw-hub CI** — lockfile now resolves `carapace-plugin-sdk` from npm registry (local dev uses `npm link`).
- **USPS mail docs** restructured into usage guide + architecture.
- Migrated `octo-satellite` and `weightwatchers` plugins to openclaw-hub (open-sourced).
- Converted all openclaw-hub plugins to Carapace SDK with updated READMEs.

### Fixed

- **Fastmail JMAP headers** — preserve angle brackets in `In-Reply-To` / `References` (JMAP expects them intact).
- **Mail-actions reply threading** — pass Message-ID in self-email handoff, fix reply-all parsing and notify ordering.

## 2026-05-09


### Added

- **Built-in carrier status providers** — USPS, FedEx, and UPS status lookups now ship with `package_tracking_core` and auto-register when the plugin loads. No configuration needed. Uses [Camoufox](https://github.com/nichochar/camoufox) (stealth Firefox) to scrape carrier tracking pages.
- **Amazon status provider** — queries the octo-satellite `/amazon/orders/:id` endpoint to get Amazon package delivery status. Configured as an external provider via `status_providers`.
- **Provider registry with fallback chain** — providers are tried in reverse registration order; external/API providers override built-ins. If a provider returns `null`, the next one is tried.
- **Amazon mail action update** — `process_amazon_shipment` handoff prompt now includes `order_id` when calling `package_add`, enabling the Amazon provider to look up order details.
- **Satellite tracking endpoints** — FedEx and Amazon tracking endpoints added to octo-satellite plugin.

## 2026-05-08


### Changed

- **Calendar fetch cron** rewritten to use CLI binaries directly via shell script (`scripts/calendar_fetch.sh`) instead of an agent tool-call loop — ~6s vs ~75s, no LLM tokens for fetching.
- **Upgrade cron notifications** rerouted from `#root` main channel to the `#Upgrade` thread.
- **Finance agent** given `web_fetch` and `web_search` tool access.

### Fixed

- `outlook-work-calendar` plugin: adapter was reading `pluginConfig.calendarUrl` but schema declared field as `url` — fixed to match.

## 2026-05-07


### Added

- **CLI generation system** — all plugins can now run as standalone CLIs without writing per-plugin CLI code. The `@openclaw/cli-shared` library introspects `createEntry()` metadata and generates CLI entry points at build time.
- Added `libs/ts/cli_shared` to both openclaw-hub and octo with runtime + build-time generator.
- Extracted `handlers.ts` (pure business logic) from all 19 plugins across both repos.
- Added CLI Usage sections to all plugin READMEs and PLUGIN_README_SHAPE.md.
- Created [Plugin Architecture](https://octo.steinbok.net/plugin-architecture) docs site page.
- Auto-generated CLI Usage sections in docs pipeline for all plugin pages.
- Created READMEs for fastmail and usps-mail plugins.

### Changed

- All plugin `package.json` files now include `bin` field and `generate-cli` build step.
- All plugin `tsup.config.ts` files now include `src/handlers.ts` in entry array.
- Plugin `src/index.ts` files refactored to thin shims delegating to handlers.
- openclaw-hub README now notes all plugins support CLI usage.

### Fixed

- WeightWatchers plugin handler extraction and CLI generation.

### Migrated

- Moved `octo-satellite` and `weightwatchers` plugins to [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub) (open-sourced).

## 2026-05-06


### Added

- Added [octo-satellite](https://github.com/JeffSteinbok/octo-satellite) plugin with Amazon order tools and Monarch Money tools (`monarch_get_accounts`, `monarch_get_net_worth`, `monarch_get_spending`).
- Added **mail-actions** service with Amazon shipment email action and self-email capability, wired into the FastMail SSE pipeline.
- Added **html-to-pdf** plugin to [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub) with release manifest and CI support.
- Added **package-tracking** plugin with pluggable carrier status providers and README documentation.
- Added DKIM/SPF/DMARC authentication checks on incoming mail in the FastMail SSE mail runtime.
- Added USPS custom rules guide with patterns, ordering, and testing tips.
- Added dynamic action plugin loading and pluggable carrier status providers to the mail pipeline.
- Added **ha-smb** skill for Home Assistant SMB file operations (ls, read, write).
- Added `@openclaw/plugin-utils` shared library extracted from duplicated plugin boilerplate in [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub).
- Added Node mock API for extracting tool metadata from TypeScript plugins in the docs bundle pipeline.

### Changed

- Migrated plugin tests across openclaw-hub to mock `@openclaw/plugin-utils` instead of raw `node:http/https`.
- Removed `dist/` from git tracking in openclaw-hub; plugins now build from source only.
- Restructured the openclaw-hub README and added DEVELOPMENT.md.
- Collapsed left-nav entries for plugins, skills, and mail runtime children on the [docs site](https://octo.steinbok.net).
- Improved runtime plugin inventory script to read manifest IDs and emoji fields.

### Fixed

- Fixed Withings token refresh to use `action=requesttoken`.
- Fixed llmvision image fetch to use binary-safe buffer collection.
- Fixed plugin origin detection in docs pipeline to use manifest ID lookup instead of directory name.
- Fixed satellite plugin ID and description in bundle-visibility config.
- Fixed health-check job to use `withings_get_measurements` instead of `withings_auth_status`.
- Fixed nav arrow rendering on docs site by adjusting parent/nav_exclude settings on child pages.

## 2026-05-03


### Added

- Complete Python → TypeScript migration of all shared libs, plugins, and the fastmail-sse service in [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub).
- TypeScript ports of `mail_action_usps`, `mail_runtime_core`, and `package_tracking_core` shared libraries.
- New plugins: **Withings**, **Glances**, and **restaurant-cli** (replaces opentable).
- Vitest test suites for all migrated TypeScript plugins and libraries.

## 2026-04-27


### Added

- Added [runtime plugin inventory pipeline](https://github.com/JeffSteinbok/octo/blob/main/tools/docs/extract/runtime_plugin_inventory.py) that auto-discovers all enabled plugins and emits structured docs metadata.
- Added all five repo-local plugins to the [docs inventory](https://octo.steinbok.net/plugins.html): **[Config Backup](https://octo.steinbok.net/plugins/config-backup.html)**, **[GitHub](https://octo.steinbok.net/plugins/github.html)**, **[OpenTable](https://octo.steinbok.net/plugins/opentable.html)**, **[OpenTable Heartbeat](https://octo.steinbok.net/plugins/opentable-heartbeat.html)**, and **[WeightWatchers](https://octo.steinbok.net/plugins/weightwatchers.html)**.
- Added test suites for all shared Python libraries, plugins, services, and scripts in [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub).
- Added [satellite docs bundle pipeline](https://github.com/JeffSteinbok/openclaw-hub) in openclaw-hub for hub-sourced plugin documentation.

### Changed

- Moved hub-sourced plugins (fastmail, homeassistant, llmvision, etc.) to [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub) only — the octo repo no longer duplicates their source.
- Sourced stock-quotes plugin from openclaw-hub instead of maintaining a local copy.
- Bumped dependencies across both repos: TypeScript 6, @types/node 25, Actions checkout v6, setup-python v6, setup-node v6, upload-artifact v7, github-script v9.
- Simplified [plugin catalog](https://octo.steinbok.net/plugins.html) layout on the docs site.
- Hardened [octo-docs](https://github.com/JeffSteinbok/octo-docs) gitops scripts with comprehensive tests.

## 2026-04-19


### Added

- Added an artifact export pipeline that can build self-contained plugin and service bundles with vendored shared Python libs.
- Added script-level tests covering plugin/service export and shared-lib dependency closure.
- Added missing README coverage for `llmvision` and the shared `repo_paths` bootstrap package.

### Changed

- Updated the packaging docs to describe how publishable artifacts are exported from the monorepo layout.
- Clarified that `octo` is the canonical private source repo while `openclaw-hub` holds mirrored public source for selected plugins, services, and shared libs.

## 2026-04-10


### Added

- Added shared mail runtime documentation, USPS runtime documentation, and dedicated docs bundle coverage for those pages.
- Added broader public docs coverage for agents, hooks, services, and related mail-runtime architecture.

### Changed

- Simplified the USPS plugin into a companion wrapper around the shared USPS runtime implementation.
- Clarified the mail pipeline and USPS processing model with explicit two-phase documentation, Mermaid diagrams, and clearer README structure.
- Improved cross-linking between FastMail docs, shared mail runtime docs, and USPS-specific docs.

### Fixed

- Fixed missing or incomplete README coverage for hooks, services, and USPS internals.
- Refreshed plugin docs and addressed related review findings, including a missing OpenTable heartbeat import.

## 2026-04-09


### Added

- Added richer Outlook calendar event details and working hass-hooks behavior for vision-driven DM delivery.
- Added USPS Informed Delivery mail rules to the FastMail configuration.

### Changed

- Refactored the USPS mail flow and improved calendar refresh behavior, including direct file output and faster parallel refresh support.
- Disabled Telegram integration as part of ongoing surface-area cleanup.

### Fixed

- Fixed GitHub workflow/plugin test issues, OpenTable slug lookup behavior, and calendar markdown output details.

## 2026-04-05


### Added

- Added an initial round of voice-call, speech-to-text, and text-to-speech integration work.

### Changed

- Removed the voice chat configuration again to keep the stack simpler while the rest of the platform evolved.

## 2026-03-28


### Fixed

- Reduced false-positive package tracking detection by skipping placeholder Amazon tracking numbers in FastMail shipping scans.

## 2026-03-14


### Added

- Added stock quotes and package tracking plugins.
- Added CI coverage for plugins and expanded automated test coverage across the repo.
- Added FastMail SSE multi-mailbox and multi-account support, per-account mail rules, package tracking detection, richer example config, and comprehensive daemon tests.
- Added richer service extraction and docs-page support for service documentation.
- Added TripIt support and broader ICS calendar fetch options.

### Changed

- Expanded FastMail automation into a more capable mail-processing service with deterministic tracking extraction and automatic package lifecycle updates.
- Broadened the docs bundle so services and related operational surfaces are better represented.
- Extended config backup coverage to include FastMail service configuration.

### Fixed

- Fixed stock quote edge cases, FastMail tracking-path issues, and multiple privacy problems caused by hardcoded personal identifiers or names.
- Reduced dependence on per-email LLM reasoning for shipping detection by moving to a rules-based extraction pipeline.

## 2026-03-10


### Added

- Added GitHub issue tooling, new Home Assistant helper tools, and additional Weight Watchers commands.
- Added support for freeform note extraction into the docs bundle.

### Changed

- Simplified note discovery by scanning root markdown files instead of requiring a dedicated notes directory.
- Updated cron and backup behavior to better match the evolving repo layout.

### Fixed

- Fixed note extraction edge cases, camera capture ignore rules, and backup workflow failures around rebasing with local changes.

## 2026-03-08


### Added

- Added major new integrations including Weight Watchers, Outlook calendar/mail, ICS calendar, Spotify, and OpenTable.
- Added the root and family agent structure, home-music knowledge, and improved plugin/workspace organization.
- Added the docs bundle pipeline with extraction support for plugins, skills, jobs, services, and structured configuration data.
- Added secret scanning and stronger repository automation around docs and config handling.

### Changed

- Shifted the repo toward a plugin-first architecture with npm workspaces and a root build flow.
- Moved calendar handling toward Graph API and clarified local-vs-shared repo conventions in the docs.
- Reworked documentation structure across README, STRUCTURE, config docs, and generated plugin docs.

### Fixed

- Fixed plugin registration details, timezone handling, Spotify redirect behavior, secret-scan workflow issues, and family-agent messaging/binding behavior.
- Improved extraction reliability by switching plugin docs parsing to a static approach instead of subprocess execution.

## 2026-03-05


### Added

- Established the early OpenClaw mail foundation with FastMail SSE support, mail-agent wiring, calendar cache handling, and backup/config documentation.
- Added repository guardrails, security-oriented agent guidance, and cleanup rules for generated Python/cache artifacts.

### Changed

- Rebranded the assistant from BoBot to Octo across naming, identity, assets, and email-related behavior.
- Shifted more configuration from hardcoded values into environment- and config-driven setup.

### Fixed

- Removed secrets from tracked configuration and tightened repo hygiene around generated files and ignored local artifacts.
- Fixed early mail and calendar issues including attachment handling and related code review findings.
