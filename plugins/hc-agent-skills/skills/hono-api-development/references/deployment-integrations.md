# Deployment and Integrations

Use this reference when starting a project, selecting a runtime, deploying, serving static files, or adding an external system.

Official sources: [Getting Started](https://hono.dev/docs/getting-started/basic), [Node.js](https://hono.dev/docs/getting-started/nodejs), [Deployment Targets](https://hono.dev/docs), [Third-party Middleware](https://hono.dev/docs/middleware/third-party).

## Runtime and Deployment

Start with `npm create hono@latest` and choose the actual deployment target. Follow that target's Hono guide for its entrypoint, bindings, local development, static-file adapter, WebSocket adapter, and deployment command. Do not present a Node entrypoint as portable to edge runtimes.

For Node containers, follow Hono's documented multi-stage build: install reproducibly, build, prune development dependencies, copy built output into the runtime image, and run as a non-root user. Keep secrets outside the image. Use platform bindings or environment configuration for runtime values.

## External Integrations

Do not prescribe an ORM, database, authentication provider, GraphQL server, queue, email service, or observability vendor without a user requirement or existing project choice.

When an integration is required:

1. Check Hono's official third-party middleware catalog.
2. Reuse an existing installed integration when suitable.
3. Read the integration's own official documentation for current setup and lifecycle rules.
4. Label ecosystem packages as third-party rather than Hono core.
5. Keep integration objects outside route handlers when reuse and runtime lifecycle permit; inject request-specific bindings through context middleware.

Use built-in Hono middleware before adding an external package that solves the same problem.
