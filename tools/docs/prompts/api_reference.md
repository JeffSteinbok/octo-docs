Generate an API reference documentation page with the following sections:

## Structure

1. **Title** (H1) — Short, clear page title (e.g. "Auth API Reference")
2. **Overview** — One short paragraph describing the API surface
3. **Endpoints / Types** — For each endpoint or type:
   - Method and path (for HTTP APIs) or type name (for SDKs)
   - Short description
   - Parameters table in Markdown (Name | Type | Required | Description)
   - Response notes if present
   - Example only if provided in source material
4. **Error Handling** — Only if described in source material

## Constraints
- Use Markdown tables for parameters
- Do not invent parameter names, types, or behaviors
- Omit any section with no source data
- Examples only if present in the source
