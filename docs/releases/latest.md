---
layout: default
title: Release Notes
nav_order: 7
---

# Release Notes

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
