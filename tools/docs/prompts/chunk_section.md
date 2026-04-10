Generate a documentation section for a single plugin or component.

## Structure

1. **H2 Heading** — The component name with a fitting emoji prefix (e.g., 📧 FastMail, 🏠 Home Assistant, 📅 Outlook Calendar, 🎵 Spotify)
2. **Brief Description** — One or two sentences about what this component does
3. **Tool Listings** — List every tool as an H4 heading with the tool name
4. **Parameter Tables** — Under each tool H4, include the tool's description and a table of its parameters (name, type, description) if parameter info is available; otherwise just show the description

## Constraints

- Generate ONLY the section content — no page title (H1), no bullet list, no introduction, no summary
- Do not wrap output in code fences
- Use ONLY information from the provided source material
- Keep it accessible to an external developer unfamiliar with the system
