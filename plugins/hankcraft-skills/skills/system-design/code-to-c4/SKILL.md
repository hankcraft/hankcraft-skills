---
name: code-to-c4
description: Reconstruct C4 architecture from an existing codebase and produce evidence-backed `c4-model.md` input for LikeC4. Use when users want diagrams or architectural understanding of implemented code, not greenfield design.
---

# Code to C4

Recover the architecture the repository implements. Produce the same `c4-model.md` contract as `../c4-modeling/SKILL.md`, then hand it to `../likec4/SKILL.md` for diagrams.

## Boundaries

- Model observed implementation, not desired architecture.
- Treat executable or deployable units as containers. A directory, package, or library alone is not a container.
- Require source evidence for every element and relationship. A dependency declaration alone does not prove a runtime call.
- Mark material interpretation as `inferred`; never present it as observed fact.
- Ignore vendored, generated, fixture, example, and test code unless the user includes it.
- Stop at C4 Component. Do not turn classes or files into diagram nodes.

## Workflow

### 1. Establish scope

Read repository instructions first. Locate workspace/build manifests, executable entrypoints, runtime commands, deployment manifests, infrastructure definitions, and existing architecture documentation. Use repository search before asking questions.

Ask only when the target system boundary or included applications remains materially ambiguous.

### 2. Discover implementation boundaries

Build a small evidence inventory:

- **Systems and actors** — public interfaces, authentication roles, CLI users, incoming webhooks. Treat actors as inferred when code exposes an interface but does not identify its user.
- **Containers** — independently started, built, deployed, or persisted units: web apps, APIs, workers, databases, queues, object stores.
- **Components** — cohesive responsibilities inside one selected container, supported by entrypoint-to-handler/service/repository call paths.
- **External systems** — configured SDK clients, network destinations, managed services, webhook peers.

Prefer runtime and deployment evidence over naming conventions. When sources conflict, use the executed/deployed path and record the conflict.

### 3. Trace relationships

Record a relationship only when code or runtime configuration supports it:

| Relationship | Strong evidence |
| --- | --- |
| inbound request | route registration, RPC handler, webhook receiver, subscription |
| synchronous outbound call | constructed client plus call site |
| data access | configured driver plus query/repository call |
| asynchronous message | producer/consumer registration plus topic or queue |
| component call | import/reference plus reachable call path |

Use short verb labels describing observed behavior. Record protocol/technology only when visible in code or configuration.

### 4. Produce `c4-model.md`

Follow `../c4-modeling/templates/c4-model.md` for System Context, Containers, optional Components, Element Registry, and Relationships. Append:

```markdown
## Implementation Evidence

| model item | status | evidence | reason |
| --- | --- | --- | --- |
| api | observed | apps/api/src/main.ts:serve | HTTP server entrypoint |
| api -> database | observed | apps/api/src/db.ts:createClient | database client and call sites |
| customer | inferred | apps/web/src/routes.ts | public UI exists; role is not encoded |
```

Rules:

- `model item` is an element ID or `source -> target`.
- `status` is `observed` or `inferred`.
- `evidence` uses repository-relative `path:symbol` or `path:line` references.
- Every Element Registry and Relationships row has at least one evidence row.
- Put unresolved but material facts after the table as `Unknown:` bullets. Do not invent nodes to close gaps.

### 5. Generate views

When loaded by `system-design`, continue directly to `../likec4/SKILL.md` after the evidence-backed model is complete.

Default view set:

- landscape/context for system boundary and external dependencies
- container view for executable and deployable units
- component view only for a user-selected or architecturally important container

Add dynamic views only for requested flows backed by a traceable path. Add deployment views only when deployment or infrastructure files support the topology.

## Done bar

- Every modeled element and relationship maps to implementation evidence.
- No container exists solely because a similarly named directory exists.
- Inferred facts and unknowns are visible.
- `c4-model.md` satisfies the sibling handoff contract.
- Generated LikeC4 source passes the validation command required by `../likec4/SKILL.md` for every edited source file.

## Anti-patterns

| Avoid | Why |
| --- | --- |
| one node per package, class, or folder | mirrors file layout instead of architecture |
| relationship from dependency manifest alone | installation does not prove use or direction |
| invented actor names | code often proves an interface, not its business user |
| full-repository component diagram | unreadable and below useful abstraction |
| claiming completeness from static search | reflection, runtime wiring, and external configuration may hide paths |
