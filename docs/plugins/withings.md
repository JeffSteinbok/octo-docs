---
layout: default
title: Withings
nav_order: 19
nav_exclude: true
---

# Withings

Fetch health data from Withings devices (weight, body composition, heart rate, sleep, activity)

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>clientId</code></td><td>string</td><td>Optional</td><td>Withings OAuth2 App Client ID.</td></tr>
    <tr><td><code>clientSecret</code></td><td>string</td><td>Optional</td><td>Withings OAuth2 App Client Secret (use env var WITHINGS_CLIENT_SECRET).</td></tr>
    <tr><td><code>redirectUri</code></td><td>string</td><td>Optional</td><td>OAuth redirect URI registered with the Withings developer app.</td></tr>
  </tbody>
</table>

## Example config

Set Withings under `plugins.entries["withings"].config`:

```json
{
  "plugins": {
    "entries": {
      "withings": {
        "enabled": true,
        "config": {
          "clientId": "${WITHINGS_CLIENT_ID}",
          "clientSecret": "${WITHINGS_CLIENT_SECRET}",
          "redirectUri": "${WITHINGS_REDIRECT_URI}"
        }
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WITHINGS_CLIENT_ID` | No | Backing value for plugin config `clientId |
| `WITHINGS_CLIENT_SECRET` | No | Backing value for plugin config `clientSecret |
| `WITHINGS_REDIRECT_URI` | No | Backing value for plugin config `redirectUri |

## Tools

### `withings_auth_url`

Generate a Withings OAuth2 authorization URL. Open this URL in a browser to link a Withings account.

### `withings_auth_complete`

Complete Withings OAuth2 flow by exchanging the authorization code for tokens.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | string | Required | The authorization code from the Withings redirect URL. |

### `withings_auth_status`

Check whether a Withings account is currently linked and whether the access token is valid.

### `withings_get_measurements`

Fetch body measurements from Withings: weight, body fat %, BMI, blood pressure, heart rate, and more.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days_back` | integer | Optional | How many days of history to fetch (default: 7). |
| `meastypes` | string | Optional | Optional comma-separated measurement type IDs (e.g. '1,6' for weight and fat ratio). |

### `withings_get_activity`

Fetch daily activity summaries from Withings: steps, distance, calories, and active/light/moderate/intense minutes.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days_back` | integer | Optional | How many days of history to fetch (default: 7). |

### `withings_get_sleep`

Fetch sleep summary data from Withings: total sleep time, REM, deep sleep, light sleep, sleep score, snoring, and wake count.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days_back` | integer | Optional | How many days of history to fetch (default: 7). |

### `withings_get_heart`

Fetch heart rate and ECG records from Withings, including AFib classification where available.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days_back` | integer | Optional | How many days of history to fetch (default: 7). |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/withings
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/withings.js --help

## Generate a Withings OAuth2 authorization URL. Open this URL in a browser to link a Withings account.
node dist/bin/withings.js withings-auth-url

## Complete Withings OAuth2 flow by exchanging the authorization code for tokens.
node dist/bin/withings.js withings-auth-complete <code>

## Check whether a Withings account is currently linked and whether the access token is valid.
node dist/bin/withings.js withings-auth-status

## Fetch body measurements from Withings: weight, body fat %, BMI, blood pressure, heart rate, and more.
node dist/bin/withings.js withings-get-measurements <days_back> <meastypes>

## Fetch daily activity summaries from Withings: steps, distance, calories, and active/light/moderate/intense minutes.
node dist/bin/withings.js withings-get-activity <days_back>

## Fetch sleep summary data from Withings: total sleep time, REM, deep sleep, light sleep, sleep score, snoring, and wake count.
node dist/bin/withings.js withings-get-sleep <days_back>

## Fetch heart rate and ECG records from Withings, including AFib classification where available.
node dist/bin/withings.js withings-get-heart <days_back>

## JSON output
node dist/bin/withings.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `WITHINGS_CLIENT_ID` | Withings OAuth2 App Client ID |
| `WITHINGS_CLIENT_SECRET` | Withings OAuth2 App Client Secret (use env var WITHINGS_CLIENT_SECRET) |
| `WITHINGS_REDIRECT_URI` | OAuth redirect URI registered with the Withings developer app |
