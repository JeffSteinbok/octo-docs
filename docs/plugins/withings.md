---
layout: default
title: Withings
parent: Plugins
nav_order: 17
---

# Withings

Fetch health data from Withings devices (weight, body composition, heart rate, sleep, activity)

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/withings)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WITHINGS_CLIENT_ID` | Yes | Withings OAuth app client ID |
| `WITHINGS_CLIENT_SECRET` | Yes | Withings OAuth app client secret |
| `WITHINGS_REDIRECT_URI` | Yes | OAuth redirect URI registered with the Withings app |

## Tools

### `withings_auth_url`

Generate a Withings OAuth2 authorization URL. Open this URL in a browser to link a Withings account. After authorizing, call withings_auth_complete with the code from the redirect URL.

### `withings_auth_complete`

Complete Withings OAuth2 flow by exchanging the authorization code for tokens. Pass the 'code' query parameter from the redirect URL.

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
| `meastypes` | string | Optional | Optional comma-separated Withings measurement type IDs to filter (e.g. '1,6' for weight and fat ratio). |

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
