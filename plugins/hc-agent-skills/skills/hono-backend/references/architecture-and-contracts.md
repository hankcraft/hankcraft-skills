# Architecture and API Contracts

Use this reference for application structure, route composition, validation, OpenAPI, or error handling.

Official sources: [Best Practices](https://hono.dev/docs/guides/best-practices), [Routing](https://hono.dev/docs/api/routing), [Middleware](https://hono.dev/docs/guides/middleware), [Validation](https://hono.dev/docs/guides/validation), [HTTPException](https://hono.dev/docs/api/exception), [Zod OpenAPI](https://hono.dev/examples/zod-openapi).

## Structure

Organize larger applications as feature route modules and mount them with `app.route()`. Prefer handlers inline after route definitions; Hono explicitly discourages Rails-style controller classes because they complicate route inference. Extract HTTP-independent business logic into plain services only when reuse or independent testing justifies it.

```text
src/
├── index.ts
├── routes/
│   ├── users.ts
│   └── auth.ts
├── middleware/
└── services/        # only shared domain logic
```

Build each child application completely before mounting it. `route()` copies routes present at mount time, so adding child routes afterward can produce a hidden 404. Middleware and handlers also run in registration order; register middleware before routes it protects.

## Validation and API Contracts

Validate every untrusted request boundary. Set the matching `Content-Type` when validating JSON or form bodies. Use one schema library already selected by the project; do not add another merely for preference.

Hono's core validator validates requests, not outgoing responses. For documented request and response contracts:

- Prefer `@hono/zod-openapi` when the project uses Zod. Declare named schemas, request inputs, response bodies, and status codes with `createRoute()`, then expose the generated OpenAPI document.
- If the project already uses another Standard Schema library, use the documented `hono-openapi` integration rather than migrating schema libraries solely for OpenAPI.
- Use Hono RPC when server and client share source types. Use OpenAPI for independently deployed or cross-language consumers.

For Hono RPC across monorepo workspaces:

- Enable `strict` in both server and client TypeScript configurations.
- Keep the Hono version aligned across workspaces.
- Export `AppType` through an explicit package export and consume it with `import type`.
- Declare the server or API-contract workspace through the repository's supported workspace protocol; do not rely on dependency hoisting.
- Use TypeScript project references or publish compiled client declarations when direct source-type imports become slow or unstable.

Tests must assert representative response bodies and status codes; an OpenAPI response declaration is not a substitute for runtime output checks.

## Error Flow

- Return expected validation failures from validator middleware.
- Throw `HTTPException` when an expected HTTP failure must escape nested logic.
- In `app.onError`, return `err.getResponse()` for `HTTPException`; log unexpected errors and return a generic 500 response.
- Use `cause` for internal diagnostics. Do not expose it to clients.
- Keep `notFound()` handling separate from internal failures.
- Use one stable JSON error envelope when the API requires machine-readable errors.

Hono sends thrown middleware/handler errors to `onError`; routine `try/catch` around `next()` is unnecessary.
