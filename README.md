# hankcraft-skills

Portable Agent Skills with native Codex and Claude Code plugin packaging.

## Install

Install the shared skills into Codex, Claude Code, Antigravity, or another supported client:

```bash
npx skills add hankcraft/hankcraft-skills
```

Install the native Codex plugin:

```bash
codex plugin marketplace add hankcraft/hankcraft-skills
codex plugin add hankcraft-skills@hankcraft-skills
```

Install the native Claude Code plugin from inside Claude Code:

```text
/plugin marketplace add hankcraft/hankcraft-skills
/plugin install hankcraft-skills@hankcraft-skills
```

## Update

```bash
npx skills update --global --yes
codex plugin marketplace upgrade hankcraft-skills
```

For Claude Code, run `/plugin marketplace update hankcraft-skills`.

## Structure

```text
.agents/plugins/marketplace.json          Codex marketplace
.claude-plugin/marketplace.json           Claude Code marketplace
plugins/hankcraft-skills/
├── .codex-plugin/plugin.json             Codex package metadata
├── .claude-plugin/plugin.json            Claude Code package metadata
└── skills/                               Canonical portable skills
docs/
└── maintain-agent-skills.md              Maintenance documentation
```

Published skills use `SKILL.md` under `plugins/hankcraft-skills/skills/`. See [Maintaining Agent Skills](docs/maintain-agent-skills.md) for the repository workflow.

## Included skills

- `hono-backend` — Build and maintain production Hono backends.
- `bun-toolchain` — Configure Bun TypeScript projects with Oxlint, Oxfmt, and Lefthook.

## Validate

```bash
uvx --from skills-ref==0.1.0 agentskills validate \
  plugins/hankcraft-skills/skills/hono-backend
uvx --from skills-ref==0.1.0 agentskills validate \
  plugins/hankcraft-skills/skills/bun-toolchain
claude plugin validate .
```

Release by updating both plugin manifest versions together, committing the change, and tagging the repository with the same semantic version.
