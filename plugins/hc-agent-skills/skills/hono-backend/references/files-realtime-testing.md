# Files, Realtime, and Testing

Use this reference for uploads, WebSockets, or test strategy.

Official sources: [File Upload](https://hono.dev/examples/file-upload), [Body Limit](https://hono.dev/docs/middleware/builtin/body-limit), [WebSocket](https://hono.dev/docs/helpers/websocket), [Testing Guide](https://hono.dev/docs/guides/testing), [Testing Helper](https://hono.dev/docs/helpers/testing).

## File Uploads

Apply `bodyLimit()` before parsing multipart input. Parse with `c.req.parseBody()`, verify the field is a `File`, then validate media type, filename policy, and any per-file constraint before storage. Return 400 for a missing or invalid file and 413 for an oversized request.

`bodyLimit()` limits the whole request body, not each file independently. Prefer runtime storage/streaming facilities over buffering large files in application memory.

## WebSockets

WebSocket setup is adapter-specific. Import `upgradeWebSocket` from the selected runtime adapter and implement only needed lifecycle handlers: `onOpen`, `onMessage`, `onClose`, and `onError`. Release timers, subscriptions, and other resources in `onClose`.

Header-mutating middleware can conflict with upgrade responses; scope it away from the WebSocket route when needed. For Node.js, use WebSocket support from `@hono/node-server`; `@hono/node-ws` is deprecated. Hono RPC can expose a typed WebSocket client when shared source types are appropriate.

## Testing

- Use `app.request()` for direct request/response behavior.
- Use `testClient(app)` when typed route calls improve the test.
- Cover success, invalid input, unauthenticated, unauthorized, not found, and expected error mapping where those paths exist.
- Test feature route applications independently when practical.
- Supply runtime bindings through `app.request()` or the runtime's official harness.
- Use Cloudflare's Workers Vitest integration for Worker-specific behavior.
- Use a runtime-compatible client for WebSocket lifecycle and cleanup tests; `app.request()` alone is insufficient.

Set the matching `Content-Type` in validation tests. A missing JSON/form content type causes Hono to expose an empty parsed object to the validator.
