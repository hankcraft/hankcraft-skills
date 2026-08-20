# hc-agent-skills

Portable Agent Skills with native Codex and Claude Code plugin packaging.

## Install

Install the shared skill into Codex, Claude Code, Antigravity, or another supported client:

```bash
npx skills add hankcraft/hc-agent-skills
```

Install the native Codex plugin:

```bash
codex plugin marketplace add hankcraft/hc-agent-skills
codex plugin add hc-agent-skills@hc-agent-skills
```

Install the native Claude Code plugin from inside Claude Code:

```text
/plugin marketplace add hankcraft/hc-agent-skills
/plugin install hc-agent-skills@hc-agent-skills
```

## Update

```bash
npx skills update --global --yes
codex plugin marketplace upgrade hc-agent-skills
```

For Claude Code, run `/plugin marketplace update hc-agent-skills`.

## Structure

```text
.agents/plugins/marketplace.json          Codex marketplace
.claude-plugin/marketplace.json           Claude Code marketplace
plugins/hc-agent-skills/
├── .codex-plugin/plugin.json             Codex package metadata
├── .claude-plugin/plugin.json            Claude Code package metadata
└── skills/                               Canonical portable skills
harness/
└── maintain-agent-skills.md              Project-only harness fixture
```

Published skills use `SKILL.md` under `plugins/hc-agent-skills/skills/`. Harness fixtures use other filenames so skill installers ignore them.

## Validate

```bash
uvx --from skills-ref==0.1.0 agentskills validate \
  plugins/hc-agent-skills/skills/hono-api-development
claude plugin validate .
```

Release by updating both plugin manifest versions together, committing the change, and tagging the repository with the same semantic version.
