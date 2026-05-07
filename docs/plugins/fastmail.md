---
layout: default
title: FastMail tools
nav_order: 2
nav_exclude: true
---

# 📧 FastMail tools

Send email and manage calendar events in Fastmail

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>accountId</code></td><td>string</td><td>Optional</td><td>JMAP account identifier.</td></tr>
    <tr><td><code>jmapToken</code></td><td>string</td><td>Optional</td><td>JMAP API authentication token.</td></tr>
    <tr><td><code>fromEmail</code></td><td>string</td><td>Optional</td><td>Sender email address.</td></tr>
    <tr><td><code>fromName</code></td><td>string</td><td>Optional</td><td>Sender display name.</td></tr>
    <tr><td><code>identityId</code></td><td>string</td><td>Optional</td><td>JMAP identity ID for sending.</td></tr>
    <tr><td><code>draftsId</code></td><td>string</td><td>Optional</td><td>JMAP mailbox ID for drafts.</td></tr>
    <tr><td><code>sentId</code></td><td>string</td><td>Optional</td><td>JMAP mailbox ID for sent mail.</td></tr>
    <tr><td><code>caldavUrl</code></td><td>string</td><td>Optional</td><td>CalDAV server URL.</td></tr>
    <tr><td><code>caldavUsername</code></td><td>string</td><td>Optional</td><td>CalDAV username.</td></tr>
    <tr><td><code>caldavPassword</code></td><td>string</td><td>Optional</td><td>CalDAV password.</td></tr>
    <tr><td><code>caldavCalendarPath</code></td><td>string</td><td>Optional</td><td>CalDAV calendar path.</td></tr>
  </tbody>
</table>
