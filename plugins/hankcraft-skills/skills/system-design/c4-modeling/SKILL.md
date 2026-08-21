---
name: c4-modeling
description: Model C4 system context, containers, and components in markdown. Use when the user explicitly asks for C4 modeling or when the system-design skill needs its modeling stage. Produces `c4-model.md`; does not write application code or LikeC4 DSL.
---

# C4 Modeling

Elicit a C4 model in plain markdown. Three gates. ASCII diagrams. No code. Output feeds the `likec4` skill.

## Purpose

Turn a vague request ("design me X") into a structured architecture description following the C4 model's first three abstractions:

- **C1 System Context** — the system, its human users, its external system dependencies.
- **C2 Containers** — the deployable / runnable units inside the system (web app, API, worker, DB, cache, queue).
- **C3 Components** — the internal pieces inside a container worth zooming into.

The deliverable is one markdown file (`c4-model.md`) following the template in `templates/c4-model.md`. The `likec4` skill turns that markdown into `.c4` source.

## Scope rules

- **No code, no DSL.** Plain English + ASCII boxes and arrows.
- **No dynamic flows.** Sequence diagrams, parallel fan-out, failure paths live in `likec4` dynamic views, not here.
- **No deployment topology.** Regions / AZs / nodes are out of scope. Add deployment views in `likec4` only when rollout topology materially matters.
- **No class diagrams.** C4 stops at Component (L3). Internal classes (L4) are not elicited.
- **Skip Component for off-the-shelf containers.** Don't zoom into a managed DB, cache, or queue — there are no user-authored components to draw.

## Workflow

Run three gates in order. Each gate ends with a section appended to `c4-model.md` (created on first gate). Use the client's user-input mechanism only for facts that cannot be inferred safely from the prompt or repository. Don't ask what the user already stated.

### Gate 1 — System Context (C4 L1)

Goal: name the system; list every actor and external system that crosses its boundary.

Ask only what is missing:

1. **System under design** — name + one-sentence purpose.
2. **Human actors** — who uses it? Roles (customer, admin, support, ops).
3. **External systems** — what other systems does it call or get called by? (Auth provider, payment gateway, email service, legacy mainframe, third-party API.)
4. **Top cross-boundary interactions** — 3–5 verbs per arrow. "Customer views balance via system", "system sends email via Postmark".

Append a `## System Context` section to `c4-model.md` with:

- One paragraph of prose describing the system's purpose and its place among actors/external systems.
- An ASCII diagram following the conventions below.
- Each box added must have a row in the Element Registry table (see below). Each arrow must have a row in the Relationships table.

### Gate 2 — Containers (C4 L2)

Goal: open the system box; list every deployable/runnable unit inside.

Ask only what is missing:

1. **Frontend surfaces** — SPA, mobile app, CLI, none?
2. **Backend tier** — single API, multiple services, BFF + workers?
3. **Async workers / jobs** — anything that runs off the request path?
4. **Data stores** — primary DB, read replicas, cache, search index, object storage?
5. **Messaging / streaming** — queue, topic, event bus?
6. **Technology choice per container** — language/runtime + framework. "Java + Spring", "Node + Fastify", "Postgres 16", "Redis 7".
7. **Protocol per link** — HTTPS/JSON, gRPC, SQL, AMQP, S3 API.

Append a `## Containers` section. ASCII diagram opens the system boundary and shows containers nested inside, plus arrows from external actors/systems where they enter the system.

Mandatory: every container gets a row in the Element Registry with `kind`, `parent` (the system), `technology`, `description`.

### Gate 3 — Components (C4 L3, optional per container)

Goal: zoom into containers where internal structure matters.

For each container the user wants to zoom into:

1. **Candidate components** — controllers, services, facades, adapters, repositories, security/auth pieces.
2. **Responsibility per component** — one sentence.
3. **Technology per component** — Spring Bean, FastAPI route, Lambda handler.
4. **Inbound calls** — which sibling components or external containers call it?

Append one `## Components — <container-id>` section per zoomed container. ASCII diagram opens the container boundary, shows components nested, plus the inbound arrows from sibling containers.

Skip a container when it is off-the-shelf (managed DB, Redis, S3, SQS) or when the user explicitly says "containers are enough for now". Record the skip in the section heading: `## Components — <container-id> (skipped: <reason>)`.

## ASCII conventions

Fixed character set so the `likec4` skill can parse it mechanically.

### Box

```
+----------------------------+
| <id>                       |
| [<kind>]                   |
| <label>                    |
+----------------------------+
```

`<id>` matches the Element Registry `id` column. `<kind>` is one of `person`, `softwaresystem`, `existingsystem`, `container`, `database`, `queue`, `spa`, `mobileApp`, `component`.

### Boundary (system or container being opened)

```
+= <id> : <label> ===========================+
|                                            |
|   +-------+      +-------+                 |
|   | childA|      | childB|                 |
|   +-------+      +-------+                 |
|                                            |
+============================================+
```

Outer boundary uses `=`. Children are normal `+--+` boxes indented inside. Only the level being explained gets opened — outer levels stay collapsed.

### Relationship arrows

- Forward: `<sourceId> --[<label> / <technology>]--> <targetId>`
- Reverse (rare in static views): `<sourceId> <--[<label> / <technology>]-- <targetId>`
- Technology after slash is optional but recommended. `--[publishes / AMQP]-->`

Each arrow drawn must have a row in the Relationships table. The diagram is the picture; the table is the source of truth.

## Element Registry (required, at end of file)

Columns:

| id | kind | parent | label | technology | description |
| --- | --- | --- | --- | --- | --- |

Rules:

- `id` must be a valid LikeC4 identifier: letters, digits, hyphens, underscores; no dots; can't start with a digit. (Dots are reserved for FQN in `.c4` source.)
- `parent` is empty for root elements (system, person, external system) and otherwise references another `id` from the table.
- `kind` matches the LikeC4 specification kinds. Stick to the set used in ASCII boxes above.
- `technology` empty for `person` and `softwaresystem` root nodes; required for containers and components.

## Relationships table (required, at end of file)

Columns:

| source | target | label | technology |
| --- | --- | --- | --- |

Rules:

- `source` and `target` are `id` values from the Element Registry.
- `label` is the verb phrase shown on the arrow. Keep it short.
- `technology` empty when the protocol is implied by the target kind (e.g. `person` → `spa` is obviously HTTPS/HTML); fill in when ambiguous.

## Handoff

When all three gates are done and the registry + relationships tables are complete:

1. Resolve any material ambiguity with the user. Skip a separate confirmation when the prompt and repository already make the design clear.
2. When loaded by `system-design`, continue directly to `likec4` with `c4-model.md` as input.
3. When invoked directly, stop at `c4-model.md` unless the user also requests LikeC4 output.

Worked end-to-end example lives in `templates/c4-model.md`. Copy it as the starting point for a new design.

## Anti-patterns

| Anti-pattern | Why bad | Do this instead |
| --- | --- | --- |
| Drawing sequence steps / parallel flows | C4 static views show structure, not order | Defer to `likec4` dynamic views |
| Listing classes inside a component | Below the C4 abstraction line | Stop at component responsibility |
| Naming AWS regions / AZs in container diagram | That is deployment, not container | Defer to `likec4` deployment views |
| Skipping Element Registry, hand-drawing only ASCII | Breaks the `likec4` handoff | Always fill both tables |
| Using `id` values with dots (`payment.api`) | Not a valid LikeC4 identifier | Use hyphen: `payment-api` |
| Asking every question even when prompt already answers it | Burns user trust | Infer first, ask only on real ambiguity |
