# Authentication, Security, and Operations

Use this reference for authentication, authorization, cookies, sessions, or production middleware.

Official sources: [JWT](https://hono.dev/docs/middleware/builtin/jwt), [JWK](https://hono.dev/docs/middleware/builtin/jwk), [Bearer Auth](https://hono.dev/docs/middleware/builtin/bearer-auth), [Cookie](https://hono.dev/docs/helpers/cookie), [Combine](https://hono.dev/docs/middleware/builtin/combine), [Third-party Middleware](https://hono.dev/docs/middleware/third-party).

## Authentication and Authorization

Choose the smallest matching mechanism:

- `bearerAuth()` for fixed or application-verified API tokens.
- `jwt()` for JWT verification with a configured secret or key.
- `jwk()` for tokens issued through a JWKS endpoint.
- A documented ecosystem integration for OAuth, OIDC, or persistent sessions.

Validate issuer, audience, expiration, and an explicit algorithm allowlist where applicable. Read secrets from runtime bindings or environment configuration, never source literals.

Authentication proves identity. Put roles, permissions, resource ownership, and tenant checks in custom middleware after token verification. Store the authenticated principal in request context for downstream handlers. Reuse policies with `createMiddleware()`; use `every()`, `some()`, or `except()` only when AND, OR, or exclusion composition is actually needed.

## Cookies and Sessions

Use Hono cookie helpers rather than manual header parsing. Use signed cookies when tamper detection is required. Authentication cookies should normally use `HttpOnly`, `Secure`, an appropriate `SameSite` value, path `/`, and preferably the `__Host-` prefix. Signed cookies provide integrity, not confidentiality.

Hono core has no prescribed session store. When sessions are required, select a maintained integration from Hono's third-party middleware catalog and follow that integration's official storage and rotation guidance.

## Production Middleware Baseline

Select only what the application needs, in deliberate order:

- `requestId()` for correlation.
- `logger()` or the platform's structured logger.
- `secureHeaders()` for response security headers.
- Restrictive `cors()` before affected routes; source deployment-specific origins from configuration.
- `timeout()` for bounded non-streaming endpoints.
- `bodyLimit()` at request-body boundaries.
- `timing()` for diagnostic `Server-Timing` metrics.

Middleware that mutates the same headers is order-sensitive. Timeout middleware is not the normal solution for streams; close streams explicitly. Hono has no single first-party OpenTelemetry architecture, so load the selected provider's official integration rather than inventing a generic setup.
