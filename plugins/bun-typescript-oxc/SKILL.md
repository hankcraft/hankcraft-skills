---
name: bun-typescript-oxc
description: >
  Modern, production-ready practices for building TypeScript projects with Bun plus the Oxc toolchain
  (oxlint, oxfmt) and Lefthook git hooks. Use this skill whenever the user is working with Bun + TypeScript
  AND any of: oxlint, oxfmt, lefthook, .oxlintrc.json, lefthook.yml, pre-commit hooks, fast Rust-based
  linting/formatting, or setting up a new Bun project that needs lint/format/hooks wired up. Prefer this
  skill over plain bun-typescript whenever oxlint, oxfmt, or lefthook appear in the project (devDependencies,
  config files, or scripts), even if the user doesn't mention them explicitly. Covers monorepos, catalogs,
  bun:test, Bun.serve(), tsconfig, bunfig.toml, and the full lint/format/hook integration.
---

# Bun + TypeScript + Oxc + Lefthook

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
| `express` / `fastify` | `Bun.serve()` |
| `better-sqlite3` | `bun:sqlite` |
| `pg` / `postgres.js` | `Bun.sql` |
| `dotenv` | automatic (Bun loads `.env`) |
| `execa` | `Bun.$\`cmd\`` |

---

## 1. Project Initialization

```sh
bun init -y
bun add -d @types/bun oxlint oxfmt lefthook
```

Pin lint/format/hook tools to **exact** versions (see §4) — these are dev tools where reproducible behavior matters more than getting patch updates.

---

## 2. TypeScript Configuration

Recommended `tsconfig.json`:

```jsonc
{
  "compilerOptions": {
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "jsx": "preserve",
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

Why these flags:
- `noEmit: true` — Bun transpiles at runtime; tsc only type-checks.
- `moduleResolution: "bundler"` — required for `allowImportingTsExtensions` and matches Bun's resolution.
- `verbatimModuleSyntax: true` — enforces `import type` for type-only imports; eliminates erasure ambiguity and improves performance.
- `noUncheckedIndexedAccess` — surfaces `undefined` from array/record indexing, catches a class of bugs oxlint can't.

Type check:
```sh
bunx tsc --noEmit
```

---

## 3. `bunfig.toml`

```toml
[install]
exact = true
```

`exact = true` is important when you're using oxlint/oxfmt/lefthook — these are pre-1.0 / fast-moving tools and floating ranges will cause confusing CI drift. Pin everything.

Add other sections (preload, test config) as needed — see the `bun-typescript` skill for the full reference.

---

## 4. oxlint

oxlint is a Rust-based linter that's roughly 50–100× faster than ESLint. It implements a large subset of ESLint, `typescript-eslint`, `eslint-plugin-unicorn`, etc. — enough to cover the rules most projects actually care about.

### Install

```sh
bun add -d oxlint
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

### What oxlint does NOT do

- **Type-aware rules** — oxlint is not type-aware. Rules like `no-floating-promises` that need the TS type checker are not (yet) supported. Run `tsc --noEmit` in CI to catch what oxlint can't.
- **Auto-fix everything** — `--fix` only applies safe, mechanical fixes. Some lint warnings still need human attention.

Don't try to make oxlint do ESLint's full job. The right mental model: oxlint catches ~80% of bugs at 1% of the cost; tsc + tests catch the rest.

---

## 5. oxfmt

oxfmt is a Rust-based formatter from the Oxc project. It aims for Prettier-compatible output but runs much faster.

### Install

```sh
bun add -d oxfmt
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

### What oxfmt does NOT (yet) do

oxfmt is younger than oxlint. As of this writing it covers JS/TS/JSX/TSX/JSON well, but support for `.vue`, `.svelte`, `.md`, etc. is uneven. Check the latest release notes if you need exotic file types — and keep Prettier as a fallback for file types oxfmt doesn't handle yet.

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
bun add -d lefthook
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
  parallel: true
  jobs:
    - name: oxlint
      glob: "*.{js,ts,jsx,tsx,vue,mjs,cjs}"
      run: bunx oxlint --fix {staged_files}
      stage_fixed: true

    - name: oxfmt
      glob: "*.{js,ts,jsx,tsx,vue,mjs,cjs,json}"
      run: bunx oxfmt {staged_files}
      stage_fixed: true
```

Why this shape:

- **`parallel: true`** — oxlint and oxfmt don't conflict on the same file (lint reads, format rewrites), and on a multi-core machine you want them running concurrently.
- **`glob:` per job** — restricts each job to file types it actually handles. Without it, oxfmt would be called on `.png` files and waste time exiting.
- **`{staged_files}` template** — Lefthook expands this to only the files staged for this commit, not the entire repo. Keeps the hook fast even on large repos.
- **`stage_fixed: true`** — when `--fix` rewrites a file, Lefthook re-stages it so the fix is part of the commit. Without this, the user has to commit, see the unstaged fixes, and commit again.
- **`bunx`** — uses the locally pinned version. Don't use globally installed binaries in hooks; they drift between machines.

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
bun add -d @types/bun oxlint oxfmt lefthook
```

Then create:

**`bunfig.toml`**
```toml
[install]
exact = true
```

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
git init        # if not already
```

Make a test commit — you should see oxlint and oxfmt run in parallel.

---

## 8. CI/CD

GitHub Actions example that mirrors the local hooks plus the slower checks:

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest

      - run: bun install --frozen-lockfile

      # Fast checks (mirror the pre-commit hook)
      - run: bun run lint
      - run: bun run format:check

      # Slower checks that don't fit pre-commit
      - run: bun run typecheck
      - run: bun test --coverage
      - run: bun --filter '*' build      # in a monorepo
```

`format:check` (not `format`) is critical in CI — you want a non-zero exit code if formatting drift slipped through, not silent rewrites.

---

## 9. Monorepo Notes

In a Bun workspace monorepo (`workspaces: ["packages/*"]`), keep oxlint, oxfmt, and lefthook **at the root** as devDependencies. They operate on file paths and don't care about package boundaries.

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
  },
  "devDependencies": {
    "@types/bun": "latest",
    "lefthook": "2.1.5",
    "oxfmt": "0.45.0",
    "oxlint": "1.60.0"
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

For everything else about Bun monorepos (workspace protocol, `--filter` scripts, per-package tsconfig extension, etc.), see the standalone `bun-typescript` skill.

---

## 10. Bun-Native APIs (Quick Reference)

This skill is focused on the lint/format/hooks layer; for the full Bun API surface (`Bun.serve`, `bun:sqlite`, `Bun.sql`, `Bun.file`, `Bun.$`, WebSockets, HTML imports, Docker), see the `bun-typescript` skill. Brief reminders:

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

- **Pinning** — `[install] exact = true` plus exact versions in `package.json` for oxlint/oxfmt/lefthook. These tools change behavior between minor versions; floating ranges cause confusing "works on my machine" formatting drift.
- **oxlint is not type-aware** — keep `tsc --noEmit` in CI. Don't expect oxlint to catch floating promises or unsafe `any` flow.
- **oxfmt vs oxlint stylistic rules** — disable oxlint's `style` category (or keep it warn-only); let oxfmt own formatting concerns. Two tools fighting over the same file is a recipe for hook loops.
- **Pre-commit speed** — keep hooks under ~3 seconds. Move tsc and tests to pre-push or CI.
- **`stage_fixed: true`** — always set this on jobs that auto-fix. Otherwise the fix lives outside the commit.
- **`bunx` in hooks, not global binaries** — version pinning is meaningless if the hook calls a globally installed `oxlint`.
- **`prepare` script** — don't forget `"prepare": "lefthook install"`. Without it, collaborators clone the repo and silently have no hooks.
- **`--no-verify`** — if you're reaching for it, the hook is too slow or too strict. Fix the hook, not the workaround.
