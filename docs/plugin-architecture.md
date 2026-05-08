---
layout: default
title: Plugin Architecture
nav_order: 5
---

# Plugin Architecture

This page describes how OpenClaw plugins are structured, how they load into the gateway, and how they can also function as standalone command-line tools.

## Overview

OpenClaw plugins are TypeScript packages that register **tools** (functions) with the gateway. Each tool has a name, description, parameter schema, and an `execute()` function. The gateway calls these tools on behalf of agents.

```
┌────────────────────────────────────────────────┐
│ OpenClaw Gateway                               │
│                                                │
│  Loads plugin via adapter.js                   │
│       ↓                                        │
│  Calls createEntry().register(api)             │
│       ↓                                        │
│  Plugin registers tools with api.registerTool  │
│       ↓                                        │
│  Agents invoke tools via the gateway           │
└────────────────────────────────────────────────┘
```

## Plugin structure

Every TypeScript plugin follows this layout:

```
plugins/<name>/
├── openclaw.plugin.json   # Manifest (id, entry, configSchema, activation)
├── package.json           # Node package metadata
├── tsup.config.ts         # Build configuration
├── src/
│   ├── index.ts           # Plugin logic — exports createEntry()
│   ├── adapter.ts         # Gateway adapter — wraps createEntry() with SDK
│   └── handlers.ts        # Pure business logic (optional, enables CLI)
├── dist/                  # Build output (gitignored)
│   ├── adapter.js
│   ├── index.js
│   ├── handlers.js
│   └── bin/
│       └── <name>.js      # Auto-generated CLI entry
└── tests/
    └── index.test.ts
```

## The `createEntry()` contract

The core of every plugin is the `createEntry()` function. It returns metadata and a `register()` callback:

```ts
export function createEntry() {
  return {
    id: "my-plugin",
    name: "My Plugin",
    description: "What this plugin does",
    configSchema: {
      properties: {
        apiKey: { type: "string", description: "API key" },
      },
    },
    register(api) {
      api.registerTool({
        name: "my_tool",
        description: "Does something",
        parameters: {
          type: "object",
          properties: {
            input: { type: "string", description: "The input" },
          },
          required: ["input"],
        },
        async execute(toolCallId, params) {
          // Business logic here
          return { result: "done" };
        },
      });
    },
  };
}
```

### Key fields

| Field | Purpose |
|-------|---------|
| `id` | Unique plugin identifier (kebab-case) |
| `name` | Human-readable name |
| `description` | Short description shown in docs and CLI help |
| `configSchema` | JSON Schema-like object describing configuration fields |
| `register(api)` | Callback that registers tools with the gateway |

## Configuration

Plugins receive configuration from two sources depending on how they run:

| Context | Config source | Mechanism |
|---------|---------------|-----------|
| Gateway | `openclaw.json` | `api.pluginConfig.fieldName` |
| CLI | Environment variables | `PLUGIN_PREFIX_FIELD_NAME` |

The **handler extraction pattern** decouples business logic from config sourcing — handlers accept a typed config object regardless of where it came from.

## Handler extraction pattern

For plugins that also serve as CLIs, we split logic into layers:

```
handlers.ts  — Pure functions (testable, no framework deps)
     ↑
index.ts     — Plugin shim (builds config from pluginConfig)
     ↑
adapter.ts   — Gateway adapter (SDK wrapper)

     ↑ (separate path)
dist/bin/    — CLI entry (builds config from env vars)
```

**`handlers.ts`** exports pure functions:

```ts
export interface MyConfig { apiKey?: string; }
export async function doThing(config: MyConfig, input: string) {
  // Pure logic — easily unit tested
}
```

**`index.ts`** delegates to handlers:

```ts
import { doThing } from "./handlers.js";

export function createEntry() {
  return {
    // ...
    register(api) {
      const config = { apiKey: api.pluginConfig?.apiKey };
      api.registerTool({
        name: "do_thing",
        async execute(_id, params) {
          return doThing(config, params.input);
        },
      });
    },
  };
}
```

## CLI generation

Every plugin can also run as a standalone CLI — **without writing per-plugin CLI code**. The `@openclaw/cli-shared` library handles this automatically.

### Build pipeline

```bash
tsup                    # Compile TypeScript → dist/
generate-cli            # Introspect createEntry() → emit dist/bin/<name>.js
```

### What the generator does

1. Imports the compiled `createEntry()` from `dist/index.js`
2. Calls `register()` to capture all tool definitions
3. Maps each tool → a CLI subcommand
4. Maps parameter schemas → positional args and flags
5. Maps `configSchema` → environment variable names
6. Emits a one-liner that bootstraps the runtime

### Tool → Subcommand mapping

| Registered tool | CLI subcommand | Rule |
|-----------------|----------------|------|
| `stock_quote` | `stock-quote` | Underscores → hyphens |
| `stock_quotes` | `stock-quotes` | Same convention |

### Config → Environment variables

Convention: `<PLUGIN_PREFIX>_<FIELD_IN_SCREAMING_SNAKE>`

| Plugin ID | Config field | Env var |
|-----------|-------------|---------|
| `stock-quotes` | `finnhubApiKey` | `STOCK_QUOTES_FINNHUB_API_KEY` |
| `spotify` | `clientId` | `SPOTIFY_CLIENT_ID` |

### CLI features

- **`--help`** — auto-generated from tool descriptions and parameter schemas
- **`--json`** — outputs raw JSON from execute()
- **Pretty output** — default formatted text with symbols and colors
- **Exit codes** — 0 on success, 1 on error, 2 on usage error

### Example

```bash
$ stock-quotes --help
stock-quotes — Fetch current stock, ETF, and mutual fund quotes

Usage:
  stock-quotes <command> [args...] [--json]

Commands:
  stock-quote    <symbol>       Get the latest quote for a stock symbol.
  stock-quotes   <symbols...>   Get quotes for multiple symbols.

Environment:
  STOCK_QUOTES_FINNHUB_API_KEY   Optional Finnhub API key for premium data

$ stock-quotes stock-quote AAPL
AAPL  $198.11  ▲ +1.23 (+0.63%)  [REGULAR]

$ stock-quotes stock-quotes MSFT GOOGL --json
[
  { "symbol": "MSFT", "price": 420.77, ... },
  { "symbol": "GOOGL", "price": 397.99, ... }
]
```

## Lifecycle

1. **Discovery** — Gateway reads `openclaw.plugin.json` from each plugin directory
2. **Loading** — Imports `dist/adapter.js` which calls `createEntry()`
3. **Registration** — Plugin's `register()` adds tools to the gateway's tool registry
4. **Execution** — When an agent invokes a tool, the gateway calls its `execute()` with params
5. **Response** — Return value is serialized and sent back to the agent

## Adding a new plugin

See the full checklist in the [plugins README](https://github.com/JeffSteinbok/openclaw-hub/blob/main/plugins/README.md).

Quick start:
1. Copy an existing plugin directory
2. Update `openclaw.plugin.json` with new id/name/description
3. Write your handlers and register tools in `createEntry()`
4. Add to `tsup.config.ts` entry array
5. `npm run build` && `npm test`
6. Add to gateway's `openclaw.json` plugin entries
