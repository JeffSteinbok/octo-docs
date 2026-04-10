---
layout: default
title: Package Tracking
parent: Plugins
nav_order: 12
---

📦 Package Tracking

Track packages from UPS, FedEx, USPS, and Amazon using direct carrier URLs.

### package_track

Get tracking information for a package by tracking number. Automatically detects carrier (UPS, FedEx, USPS, Amazon) from tracking number format. Returns tracking URL that can be opened in a browser. If the package is saved in the tracking list, returns saved info. Otherwise, generates tracking info on-the-fly.

| Name            | Type   | Description                                                                                  |
|-----------------|--------|----------------------------------------------------------------------------------------------|
| tracking_number | string | Package tracking number (e.g., 1Z999AA10123456784, 940000000000000000000, TBA012345678901US) |
| carrier         | string | Optional carrier override: UPS, FedEx, USPS, or Amazon                                      |

### package_add

Add a package to the tracking list for easy access later. Automatically detects carrier from tracking number format. Optionally add a label/description for the package (e.g., 'iPhone case', 'Birthday gift'). Saved packages can be listed with package_list and tracked with package_track.

| Name            | Type   | Description                                             |
|-----------------|--------|---------------------------------------------------------|
| tracking_number | string | Package tracking number                                 |
| carrier         | string | Optional carrier override: UPS, FedEx, USPS, or Amazon  |
| label           | string | Optional label/description for the package              |

### package_remove

Remove a package from the tracking list. Use this when a package has been delivered and you no longer need to track it.

| Name            | Type   | Description                          |
|-----------------|--------|--------------------------------------|
| tracking_number | string | Package tracking number to remove     |

### package_list

List all packages currently being tracked. Returns tracking numbers, carriers, URLs, labels, and when each package was added. Use this to see all your active shipments at a glance.

### package_scan

Scan text (email body, message, etc.) for tracking numbers. Automatically detects UPS, FedEx, USPS, and Amazon tracking numbers. Returns list of found tracking numbers with carrier and tracking URL. Useful for extracting tracking info from shipping notifications.

| Name | Type   | Description                                    |
|------|--------|------------------------------------------------|
| text | string | Text to scan for tracking numbers (e.g., email body) |
