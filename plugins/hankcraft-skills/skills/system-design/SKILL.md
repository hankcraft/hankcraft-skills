---
name: system-design
description: Router for system design work. Use when designing a system, architecting a service, clarifying actors/containers/components, or producing C4/LikeC4 diagrams. Two routes only — markdown-first elicitation, then concrete `.c4` source.
---

# System Design

Two-route bundle. Clarify the architecture in plain markdown first, then turn it into concrete `.c4` source. No middle layer and no implementation framework required.

## Routing

| Situation | Load |
| --- | --- |
| Need to clarify a system: identify actors, decide containers, pick components, write it down with ASCII diagrams | `c4-modeling/SKILL.md` |
| Have a structured C4 description (markdown + element/relationship tables) and need `.c4` / `.likec4` source plus views | `likec4/SKILL.md` |

## Default flow

1. Enter at `c4-modeling` for any "design me…", "what does the architecture look like", "what containers should I have" prompt.
2. Walk the three C4 gates (Context → Container → Component). Produce a single `c4-model.md`.
3. Hand off to `likec4`. Generate `.c4` source from the markdown using the handoff mapping in `likec4/SKILL.md`.

This is one continuous workflow. Continue from elicitation through validated `.c4` output without asking the user to invoke the next skill. Pause only for a material unresolved design choice or when the user explicitly requests a markdown-only checkpoint.

Skip directly to `likec4` only when the user already provides a structured architecture description (element list + relationships) or asks a DSL/CLI question about an existing `.c4` file.

## Handoff contract

Exactly one artifact crosses the boundary: `c4-model.md` with four sections.

- **System Context** — prose + ASCII diagram of the system and its actors/external systems.
- **Containers** — prose + ASCII diagram of the system's deployable units and their links.
- **Components** — per-container ASCII zoom-in, optional.
- **Element Registry + Relationships** — two tables. Element table: `id | kind | parent | label | technology | description`. Relationship table: `source | target | label | technology`.

Schema and ASCII conventions defined in `c4-modeling/templates/c4-model.md`. `likec4` reads this contract to produce `.c4` source mechanically.

## Done bar

- `c4-model.md` exists with all required sections filled.
- `.c4` source generated from it validates clean: `likec4 validate --json --no-layout --file <path> <project-dir>` returns `filteredErrors: 0` for every edited source file.
- Every box in the ASCII has a row in the Element Registry. Every relationship arrow has a row in the Relationships table.

## Optional implementation handoff

Architecture output is complete on its own. Do not load implementation skills unless the user asks to build or change code.

When the user requests implementation with Hono, Bun, or both:

1. Complete and validate the architecture first.
2. Load `hono-backend` when Hono owns an API container. It owns routes, middleware, validation, API contracts, endpoint tests, and runtime adapters.
3. Load `bun-toolchain` when Bun owns the runtime or repository toolchain. It owns package management, workspaces, TypeScript, Oxc, hooks, and CI.
4. Treat `c4-model.md` and the validated `.c4` model as implementation constraints. Map containers to deployable workspaces/apps and components to responsibilities; do not invent another container or external dependency silently.
5. If implementation requires an architectural change, update `c4-model.md` and `.c4` source, then revalidate before continuing.

Routine Hono endpoint or Bun tooling work does not require running this architecture workflow unless the user asks for design work or the change crosses an architectural boundary.

## Out of scope

Dynamic flows, deployment topology, ADRs, SLO worksheets, tradeoff matrices. Add them inside `likec4` (dynamic / deployment views) when the design genuinely needs them. Not a default deliverable.
