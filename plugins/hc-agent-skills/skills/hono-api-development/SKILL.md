---
name: hono-api-development
description: Build or modify HTTP APIs using Hono. Use for Hono routes, middleware, request validation, runtime adapters, and API tests; not for frontend-only work.
license: MIT
---

# Develop Hono APIs

## Workflow

1. Inspect the package manager, runtime adapter, app entrypoint, route organization, validation library, and test setup.
2. Extend existing patterns. For a new app, choose the deployment runtime before selecting the Hono starter or adapter.
3. Implement the smallest route or middleware change that satisfies the requested behavior.
4. Validate untrusted params, query values, headers, and bodies before domain work. Reuse the installed validator; use `hono/validator` for simple validation rather than adding a schema dependency.
5. Return explicit response bodies and status codes through the Hono context.
6. Add one focused request-level check with `app.request()`, including the correct `Content-Type` when testing parsed JSON or form bodies.
7. Run the project's existing typecheck and tests.

## Constraints

- Keep portable route logic separate from runtime-specific startup code.
- Preserve chained route definitions when the project relies on Hono RPC or `testClient()` type inference.
- Type runtime bindings or context variables only when used.
- Reuse existing error handling and middleware order.
- Do not add authentication, databases, OpenAPI generation, logging stacks, or new routers unless requested.
