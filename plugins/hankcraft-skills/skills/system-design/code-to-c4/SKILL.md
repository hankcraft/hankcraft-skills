---
name: code-to-c4
description: Derive evidence-backed C4/LikeC4 static, dynamic, and deployment views from existing code, or correct model drift found during tracing. Not for greenfield design or code-inventory diagrams.
---

# Code to C4

Recover the architecture the repository implements. Produce the same `c4-model.md` contract as `../c4-modeling/SKILL.md`, then hand it to `../likec4/SKILL.md` for diagrams.

## Use when

Use this skill when a repository needs:

- static C4 views aligned with current responsibilities
- focused sequence views for implemented scenarios
- deployment views backed by manifests or infrastructure code
- correction of architecture-model drift discovered during tracing

Deliberately avoid file/function diagrams, speculative components, and one giant sequence containing every path.

## Boundaries

- Model observed implementation, not desired architecture.
- Treat executable or deployable units as containers. A directory, package, or library alone is not a container.
- Require source evidence for every reconstructed, changed, or shown element and relationship. A dependency declaration alone does not prove a runtime call.
- Mark material interpretation as `inferred`; never present it as observed fact.
- Ignore vendored, generated, fixture, example, and test code unless the user includes it.
- Stop at C4 Component.

## Workflow

### 1. Establish scope

Read repository instructions first. Locate workspace/build manifests, executable entrypoints, runtime commands, deployment manifests, infrastructure definitions, and existing architecture documentation. Find the nearest LikeC4 config, specification, model, and views when present. Use repository search before asking questions.

Ask only when the target system boundary or included applications remains materially ambiguous.

### 2. Reconcile an existing LikeC4 project

When a LikeC4 project exists, preserve its identifiers, kinds, relationships, file organization, and view conventions. Compare its model with implementation evidence before adding views.

- Report drift between current implementation and modeled intent.
- Correct drift only when the user requested model/diagram updates or the requested view would otherwise be false.
- Add an element only for a stable architectural responsibility with its own reason to change.
- Do not blend current implementation with target architecture when intent is unclear.
- Use full FQNs across files.

Views select from the model; they must not hide inaccurate elements or relationships.

### 3. Discover implementation boundaries

Build a small evidence inventory:

- **Systems and actors** — public interfaces, authentication roles, CLI users, incoming webhooks. Treat actors as inferred when code exposes an interface but does not identify its user.
- **Containers** — independently started, built, deployed, or persisted units: web apps, APIs, workers, databases, queues, object stores.
- **Components** — cohesive responsibilities inside one selected container, supported by entrypoint-to-handler/service/repository call paths.
- **External systems** — configured SDK clients, network destinations, managed services, webhook peers.

Prefer runtime and deployment evidence over naming conventions. When sources conflict, use the executed/deployed path and record the conflict.

### 4. Trace relationships and scenarios

Record a relationship only when code or runtime configuration supports it:

| Relationship | Strong evidence |
| --- | --- |
| inbound request | route registration, RPC handler, webhook receiver, subscription |
| synchronous outbound call | constructed client plus call site |
| data access | configured driver plus query/repository call |
| asynchronous message | producer/consumer registration plus topic or queue |
| component call | import/reference plus reachable call path |

Use short verb labels describing observed behavior. Record protocol/technology only when visible in code or configuration.

For a requested scenario, trace entrypoint to completion. Record step order, source and target responsibilities, operation/event/protocol, and code location. Preserve concurrency and asynchronous boundaries; do not force parallel work into a linear sequence.

### 5. Produce `c4-model.md`

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

- `model item` is an element ID, `source -> target`, or `<view-id>#<step-number>` for a dynamic step.
- `status` is `observed` or `inferred`.
- `evidence` uses repository-relative `path:symbol` or `path:line` references.
- In a reconstructed `c4-model.md`, every Element Registry and Relationships row has evidence. In an existing project, every corrected or shown item has evidence.
- Put unresolved but material facts after the table as `Unknown:` bullets. Do not invent nodes to close gaps.

### 6. Generate focused views

When loaded by `system-design`, continue directly to `../likec4/SKILL.md` after the evidence-backed model is complete.

Choose each view by the question it answers:

| Question | View |
| --- | --- |
| What surrounds the system? | landscape or context view |
| What runs independently? | container view |
| What stable responsibilities collaborate inside one container? | scoped component view |
| How does one implemented scenario execute? | dynamic view |
| Where do logical elements run? | deployment view |

Keep static views scoped to one system, container, or responsibility and its direct collaborators. Do not duplicate model relationships solely for a view.

Create dynamic views only for requested, traceable scenarios. Use one view per independently explainable path. Preserve implemented order, use `parallel` for concurrent work, `<-` for responses, and notes for repeated polling/retries when expanding every iteration adds no value. Split success and failure paths when combining them obscures order.

Create deployment views only when manifests or infrastructure code prove the topology. Map logical elements into named `instanceOf` instances; do not infer regions, nodes, or trust boundaries.

Load `../likec4/references/examples.md` only when choosing view syntax or scenario splits requires examples.

### 7. Validate and inspect

Use the installed runner and the validation contract in `../likec4/SKILL.md`. Repeat `--file` for every edited LikeC4 source. Success requires `filteredErrors: 0`; inspect nonzero `totalErrors` and report unrelated project errors separately.

Export affected views to a temporary directory:

```bash
<runner> likec4 export png --flat --outdir <temporary-dir> --filter '<view-id-pattern>' <project-dir>
```

Add `--seq` for dynamic sequence layouts. Inspect every exported image for missing participants, wrong direction/order, ambiguous labels, excessive crossings, unreadable density, and incorrect deployment nesting. Fix selection or layout without changing model truth. If export or image inspection is unavailable, report that visual verification was not completed.

## Done bar

- Every reconstructed, changed, or shown element and relationship maps to implementation evidence.
- No container exists solely because a similarly named directory exists.
- Inferred facts and unknowns are visible.
- Drift is corrected within scope or explicitly reported.
- Every dynamic step maps to scenario evidence and preserves concurrency.
- `c4-model.md` satisfies the sibling handoff contract.
- Generated LikeC4 source passes the validation command required by `../likec4/SKILL.md` for every edited source file.
- Affected views were rendered and inspected, or missing visual verification was disclosed.

## Anti-patterns

| Avoid | Why |
| --- | --- |
| one node per package, class, or folder | mirrors file layout instead of architecture |
| relationship from dependency manifest alone | installation does not prove use or direction |
| invented actor names | code often proves an interface, not its business user |
| full-repository component diagram | unreadable and below useful abstraction |
| claiming completeness from static search | reflection, runtime wiring, and external configuration may hide paths |
