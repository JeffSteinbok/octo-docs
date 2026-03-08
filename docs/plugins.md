# Plugins Overview

## Overview

Plugins extend the functionality of the system by providing specialized tools for various tasks, such as managing emails, calendars, home automation, and more. Each plugin is designed to solve a specific problem, offering a set of tools that interact with external services or perform specific actions. This document provides an overview of the available plugins, their purposes, and example use cases.

## Key Concepts

- **Plugins**: Modular components that add specific functionalities to the system.
- **Tools**: Individual actions or endpoints provided by each plugin.
- **Use Cases**: Practical scenarios where plugins can be applied to solve real-world problems.

## Plugin List

| Plugin Name               | Description                                                                                     | Number of Tools |
|---------------------------|-------------------------------------------------------------------------------------------------|-----------------|
| `config-backup`           | Backs up OpenClaw config to Git with SHA-256 change detection.                                  | 1               |
| `fastmail`                | Send email, search/read inbox, manage calendar events via JMAP and CalDAV.                     | 7               |
| `hass-camera-snapshot`    | Take snapshots from Home Assistant cameras via hass-cli and save locally.                      | 2               |
| `homeassistant-cli`       | Control Home Assistant via hass-cli: get/list entity states, call services, and list events.    | 4               |
| `ics-calendar`            | Fetches Nicole's calendar from an ICS feed.                                                    | 1               |
| `opentable`               | Check restaurant availability on OpenTable.                                                    | 0               |
| `opentable-heartbeat`     | Health-check for the OpenTable skill. Alerts on failure via configured notification channel.    | 1               |
| `outlook-calendar`        | Fetch personal and family calendars via Microsoft Graph API.                                   | 1               |
| `outlook-mail`            | Search and read Outlook inbox via Microsoft Graph API.                                         | 3               |
| `outlook-work-calendar`   | Fetches published Outlook work calendar via EWS JSON API (no auth required).                   | 1               |
| `weightwatchers`          | Search foods, log meals, view diary and points budget via the unofficial WW API.               | 5               |

## How It Works

1. **Plugin Selection**: Choose the plugin that matches your use case (e.g., email management, calendar synchronization, home automation).
2. **Tool Execution**: Each plugin provides specific tools (endpoints) that can be executed to perform tasks. For example:
   - Use `fastmail_send` to send an email.
   - Use `ha_service_call` to control a Home Assistant device.
   - Use `ww_search` to find food items in the WeightWatchers database.
3. **Input Parameters**: Provide the required parameters for the selected tool. Each tool has specific input requirements, such as email addresses, dates, or entity IDs.
4. **Output**: The tool returns the requested data or performs the specified action.

## Example Use Cases

- **Email Management**: Use the `fastmail` plugin to send emails, search your inbox, or manage calendar events.
- **Home Automation**: Use the `homeassistant-cli` plugin to control smart home devices, such as turning on lights or checking sensor states.
- **Calendar Integration**: Fetch events from personal, family, or work calendars using the `outlook-calendar`, `ics-calendar`, or `outlook-work-calendar` plugins.
- **Health Monitoring**: Use the `opentable-heartbeat` plugin to ensure the availability of the OpenTable service.
- **Diet Tracking**: Log meals, calculate points, and manage your food diary with the `weightwatchers` plugin.

## Common Pitfalls

- **Missing Parameters**: Ensure all required parameters are provided when using a tool. Refer to the specific tool's documentation for details.
- **Environment Variables**: Some plugins, such as `ics-calendar` and `outlook-work-calendar`, require environment variables to function correctly. Ensure these are configured before using the tools.
- **Tool Availability**: Not all plugins provide tools. For example, the `opentable` plugin does not currently include any tools.
