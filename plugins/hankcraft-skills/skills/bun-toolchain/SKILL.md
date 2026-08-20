---
name: bun-toolchain
description: >
  Build and maintain Bun + TypeScript projects with oxlint, oxfmt, and Lefthook. Use for Bun setup,
  monorepos, bun:test, Bun.serve(), tsconfig, bunfig.toml, linting, formatting, or git hooks. Prefer this
  skill when oxlint, oxfmt, Lefthook, .oxlintrc.json, or lefthook.yml appears.
---

# Bun Toolchain

A composite stack for fast, modern TypeScript projects:

- **Bun** — runtime, package manager, bundler, test runner
- **oxlint** — Rust-based linter (10–100× faster than ESLint)
- **oxfmt** — Rust-based formatter (Prettier-compatible output, much faster)
- **Lefthook** — fast parallel git hooks manager

The whole toolchain is designed to keep the inner loop snappy: lint + format on every commit without slowing the developer down.

---

## Key Principle: Use Bun's Built-ins

Bun ships replacements for most Node.js ecosystem tools. Always prefer them:

| Instead of… | Use… |
|---|---|
| `node` / `ts-node` | `bun` |
| `npm` / `yarn` / `pnpm` | `bun` |
| `jest` / `vitest` | `bun test` |
| `webpack` / `esbuild` | `bun build` |
| `eslint` | `oxlint` |
| `prettier` | `oxfmt` |
| `husky` / `simple-git-hooks` | `lefthook` |
| Framework-free HTTP server | `Bun.serve()` |
| `better-sqlite3` | `bun:sqlite` |
| `pg` / `postgres.js` | `Bun.sql` |
| `dotenv` | automatic (Bun loads `.env`) |
| `execa` | `Bun.$\`cmd\`` |

An existing framework owns its routing and entrypoint shape. Use `Bun.serve()` directly only when no selected framework already provides a Bun entrypoint.

### Composition with Hono

When a Hono skill also applies, this skill owns Bun package management, workspace boundaries, TypeScript baseline, Oxc, Lefthook, and CI orchestration. The Hono skill owns routes, middleware, validation, API contracts, endpoint tests, and adapter details. Keep Hono as the HTTP framework and use its Bun entrypoint; do not replace its routes with a parallel `Bun.serve()` routing table. Prefer Hono's `app.request()` inside `bun test` for endpoint behavior.

---

## 1. Project Initialization

For a new standalone project:

```sh
bun init -y
git init
bun add -d typescript @types/bun
bun add -d --exact oxlint oxfmt lefthook
```

In an existing repository, inspect its workspace layout first. Do not run `bun init` or `git init` again. Install repository-wide tooling at the workspace root; install runtime dependencies in the workspace that imports them.

Pin behavior-sensitive lint/format/hook tools to exact versions and commit `bun.lock`. Keep other dependency version policy project-specific.

---

## 2. TypeScript Configuration

Recommended `tsconfig.json`:

```jsonc
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "target": "ESNext",
    "module": "Preserve",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "strict": true,
    "skipLibCheck": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noEmit": true,
    "verbatimModuleSyntax": true,
    "allowImportingTsExtensions": true,
    "types": ["bun"]
  }
}
```

Add `DOM`/`DOM.Iterable` only for browser targets. Add the JSX mode required by the chosen framework; server-only Bun projects should not expose browser globals by default.

Why these flags:
- `noEmit: true` — Bun transpiles at runtime; tsc only type-checks.
- `moduleResolution: "bundler"` — required for `allowImportingTsExtensions` and matches Bun's resolution.
- `verbatimModuleSyntax: true` — enforces `import type` for type-only imports; eliminates erasure ambiguity and improves performance.
- `noUncheckedIndexedAccess` — surfaces `undefined` from array/record indexing, catches a class of bugs oxlint can't.

Standalone type check:
```sh
bunx --no-install tsc --noEmit
```

In a monorepo, keep shared compiler options in a root base config and let every workspace extend it with its own `types`, `lib`, `jsx`, `include`, and `exclude`. Run each workspace's `typecheck` script rather than checking the repository through one catch-all root project.

---

## 3. `bunfig.toml`

`bunfig.toml` is optional. Use `bun add --exact` for behavior-sensitive tools instead of forcing exact versions for every dependency. Reproducible CI comes from committing `bun.lock` and running `bun ci`.

Add other sections such as preload or test configuration only when the project needs them.

---

## 4. oxlint

oxlint is a Rust-based linter that's roughly 50–100× faster than ESLint. It implements a large subset of ESLint, `typescript-eslint`, `eslint-plugin-unicorn`, etc. — enough to cover the rules most projects actually care about.

### Install

```sh
bun add -d --exact oxlint
```

Pin it. oxlint releases frequently and rules graduate between versions.

### `.oxlintrc.json`

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["typescript", "unicorn", "oxc"],
  "categories": {
    "correctness": "error",
    "suspicious": "warn",
    "perf": "warn"
  },
  "ignorePatterns": ["node_modules", "dist", "build", ".plasmo", ".parcel-cache"]
}
```

The `$schema` reference gives editor autocomplete for the config file itself.

**Categories vs individual rules** — start with categories (`correctness`, `suspicious`, `perf`, `pedantic`, `style`, `nursery`). Promote `correctness` to `error` and the rest to `warn` until you've cleaned up the warnings, then promote them too. Drop into individual `rules: { ... }` overrides only when you need to silence a specific rule on a specific file pattern.

### package.json scripts

```json
{
  "scripts": {
    "lint": "oxlint",
    "lint:fix": "oxlint --fix"
  }
}
```

oxlint walks from the cwd by default and respects `.gitignore`. No need for glob arguments in the script.

One root configuration is the monorepo baseline. When a workspace needs different rules, add a nested configuration that explicitly extends the root; nested Oxlint configurations are selected by proximity and are not merged automatically.

### Optional type-aware linting

Oxlint supports type-aware rules through the separate `oxlint-tsgolint` package. Add it only when the project needs rules such as `typescript/no-floating-promises`:

```sh
bun add -d --exact oxlint-tsgolint
bunx --no-install oxlint --type-aware
```

The equivalent root config is:

```json
{
  "options": {
    "typeAware": true
  },
  "rules": {
    "typescript/no-floating-promises": "error"
  }
}
```

Keep `tsc --noEmit` in CI. Oxlint's `--type-check` can report TypeScript diagnostics, but it remains experimental and should not replace the baseline type-check step by default.

`--fix` only applies safe, mechanical fixes. Some lint warnings still need human attention.

---

## 5. oxfmt

oxfmt is a Rust-based formatter from the Oxc project. It aims for Prettier-compatible output but runs much faster.

### Install

```sh
bun add -d --exact oxfmt
```

Pin it. oxfmt is still pre-1.0 — output formatting can shift between minor versions. A pinned version means the whole team produces byte-identical formatting.

### Usage

```sh
oxfmt              # format all files in cwd
oxfmt --check      # exit non-zero if anything would change (CI)
oxfmt path/to/file # format specific files
```

### package.json scripts

```json
{
  "scripts": {
    "format": "oxfmt",
    "format:check": "oxfmt --check"
  }
}
```

### Language support

Oxfmt supports JS, TS, JSX, TSX, JSON, YAML, TOML, HTML, Vue, Svelte, CSS, Markdown, MDX, GraphQL, and more. Some formats use bundled Prettier while native implementations are still being completed; `.svelte` additionally requires the `svelte` package and formatter option. Keep standalone Prettier only when the project depends on unsupported plugin behavior.

Don't run oxlint and oxfmt in conflicting modes. oxlint has stylistic rules in the `style` category that overlap with formatter concerns — keep the `style` category disabled (or warn-only) and let oxfmt own formatting.

---

## 6. Lefthook

Lefthook is a fast, parallel git hooks manager written in Go. Compared to husky:
- Single binary, no Node startup overhead per hook
- Parallel jobs out of the box
- One declarative YAML config
- Built-in `{staged_files}` template — no need to call `lint-staged`

### Install

```sh
bun add -d --exact lefthook
```

Then add a `prepare` script so hooks install on `bun install`:

```json
{
  "scripts": {
    "prepare": "lefthook install"
  }
}
```

`bun install` automatically runs `prepare` after install completes — collaborators get hooks for free on their first `bun install`.

### `lefthook.yml`

```yaml
pre-commit:
  piped: true
  jobs:
    - name: oxlint
      glob: "*.{js,ts,jsx,tsx,vue,svelte,astro,mjs,cjs,mts,cts}"
      run: bunx --no-install oxlint --fix {staged_files}
      stage_fixed: true

    - name: oxfmt
      glob: "*"
      run: bunx --no-install oxfmt --no-error-on-unmatched-pattern {staged_files}
      stage_fixed: true
```

Why this shape:

- **`piped: true`** — `oxlint --fix` and oxfmt both rewrite files. Run lint fixes first, then format their output to avoid races and lost edits.
- **`glob:` per job** — restrict oxlint to supported source files. Let oxfmt select supported formats; `--no-error-on-unmatched-pattern` makes unsupported staged files a no-op.
- **`{staged_files}` template** — Lefthook expands this to only the files staged for this commit, not the entire repo. Keeps the hook fast even on large repos.
- **`stage_fixed: true`** — when `--fix` rewrites a file, Lefthook re-stages it so the fix is part of the commit. Without this, the user has to commit, see the unstaged fixes, and commit again.
- **`bunx --no-install`** — requires the locally pinned version instead of silently downloading a missing package.

### What NOT to put in pre-commit

Pre-commit hooks should be **fast** (< a few seconds total). Anything slower belongs in pre-push or CI:

| Check | Where |
|---|---|
| oxlint, oxfmt | pre-commit |
| `tsc --noEmit` | pre-push or CI (slow on cold cache) |
| `bun test` | pre-push or CI |
| Build | CI only |

If pre-commit takes more than ~3 seconds on a typical change, developers will start passing `--no-verify` and the hook becomes worse than nothing.

### Skipping hooks (rare, intentional)

```sh
LEFTHOOK=0 git commit -m "wip"        # skip all hooks
git commit -m "wip" --no-verify       # same effect
```

Reserve this for genuine emergencies. Don't normalize `--no-verify`.

---

## 7. Putting It Together: New Project Checklist

```sh
bun init -y
git init
bun add -d typescript @types/bun
bun add -d --exact oxlint oxfmt lefthook
```

Then create:

**`.oxlintrc.json`** — see §4

**`lefthook.yml`** — see §6

**`package.json` scripts**
```json
{
  "scripts": {
    "lint": "oxlint",
    "lint:fix": "oxlint --fix",
    "format": "oxfmt",
    "format:check": "oxfmt --check",
    "typecheck": "tsc --noEmit",
    "prepare": "lefthook install"
  }
}
```

Then:

```sh
bun install     # also runs `prepare` → installs hooks
```

Make a test commit — you should see oxlint run before oxfmt.

---

## 8. CI/CD

GitHub Actions example that mirrors the local hooks plus the slower checks:

Pin Bun in `package.json` so local tooling and CI share an explicit version:

```json
{
  "packageManager": "bun@1.3.14"
}
```

Update that version intentionally with the project. `setup-bun` reads it automatically:

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2

      - run: bun ci

      # Fast checks (mirror the pre-commit hook)
      - run: bun run lint
      - run: bun run format:check

      # Slower checks that don't fit pre-commit
      - run: bun --filter '*' typecheck
      - run: bun test --coverage
      - run: bun --filter '*' build      # in a monorepo
```

`format:check` (not `format`) is critical in CI — you want a non-zero exit code if formatting drift slipped through, not silent rewrites.

---

## 9. Monorepo Notes

In a Bun workspace monorepo, keep oxlint, oxfmt, and lefthook **at the root** as devDependencies. Keep application and library runtime dependencies in the workspace that imports them; do not rely on hoisting or a root dependency to make undeclared imports work.

The lefthook config (one `lefthook.yml` at the root) handles every package's staged files automatically — `{staged_files}` is repo-wide.

For shared dependency versions across workspaces, use Bun's catalogs:

```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": {
    "packages": ["packages/*"],
    "catalog": {
      "typescript": "^5.4.0"
    }
  }
}
```

Workspace packages can reference catalog versions:
```json
{
  "devDependencies": {
    "typescript": "catalog:"
  }
}
```

Declare dependencies between workspaces with `workspace:*`. Give each workspace its own scripts and TypeScript configuration:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "bun test",
    "build": "bun build ./src/index.ts --outdir ./dist"
  }
}
```

Run scripts from the root with filters:

```sh
bun --filter '*' typecheck
bun --filter '*' test
bun --filter '*' build
```

Only define scripts a workspace supports. Narrow the filter when a command applies to one application or package group.

---

## 10. Bun-Native APIs (Quick Reference)

This skill is focused on the lint/format/hooks layer. Brief Bun-native API reminders:

```ts
// HTTP
Bun.serve({ port: 3000, routes: { "/": () => new Response("hi") } });

// SQLite
import { Database } from "bun:sqlite";
const db = new Database("app.db");

// File I/O
const data = await Bun.file("./data.json").json();
await Bun.write("./out.json", JSON.stringify(data));

// Shell
import { $ } from "bun";
await $`ls -la`.text();
```

---

## Common Gotchas

- **Pinning** — install oxlint/oxfmt/lefthook with `bun add --exact`, commit `bun.lock`, and use `bun ci`. Do not impose exact versions on unrelated dependencies without a project policy.
- **Type-aware oxlint** — install `oxlint-tsgolint` and enable `typeAware` only when needed. Keep `tsc --noEmit` as the default CI type check.
- **oxfmt vs oxlint stylistic rules** — disable oxlint's `style` category (or keep it warn-only); let oxfmt own formatting concerns. Two tools fighting over the same file is a recipe for hook loops.
- **Pre-commit speed** — keep hooks under ~3 seconds. Move tsc and tests to pre-push or CI.
- **Sequential writers** — run `oxlint --fix` before oxfmt; never let both rewrite the same staged file in parallel.
- **`stage_fixed: true`** — always set this on jobs that auto-fix. Otherwise the fix lives outside the commit.
- **`bunx --no-install` in hooks** — version pinning is meaningless if a missing local binary can fall back to an automatic download.
- **`prepare` script** — don't forget `"prepare": "lefthook install"`. Without it, collaborators clone the repo and silently have no hooks.
- **`--no-verify`** — if you're reaching for it, the hook is too slow or too strict. Fix the hook, not the workaround.
