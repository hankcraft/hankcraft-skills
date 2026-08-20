# hc-agent-skills

Portable Agent Skills with native Codex and Claude Code plugin packaging.

## Install

Install the shared skill into Codex, Claude Code, Antigravity, or another supported client:

```bash
npx skills add hankchiu/hc-agent-skills \
  --skill maintain-agent-skills \
  --agent '*' \
  --global
```

Install the native Codex plugin:

```bash
codex plugin marketplace add hankchiu/hc-agent-skills
codex plugin add hc-agent-skills@hc-agent-skills
```

Install the native Claude Code plugin from inside Claude Code:

```text
/plugin marketplace add hankchiu/hc-agent-skills
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
```

Add each capability once under `plugins/hc-agent-skills/skills/<skill-name>/`. Keep vendor-specific configuration in plugin manifests.

## Validate

```bash
uvx --from skills-ref==0.1.0 agentskills validate \
  plugins/hc-agent-skills/skills/maintain-agent-skills
claude plugin validate .
```

Release by updating both plugin manifest versions together, committing the change, and tagging the repository with the same semantic version.
