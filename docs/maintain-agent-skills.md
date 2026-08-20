# Maintaining Agent Skills

This repository publishes portable Agent Skills through a shared skill directory and thin native plugin wrappers. Each capability has one implementation, regardless of installation method.

## Repository model

Published skills live under `plugins/hankcraft-skills/skills/<skill-name>/`. Each directory contains a required `SKILL.md` and only the scripts, references, or assets that capability uses.

Codex and Claude Code metadata wrap the same plugin directory:

| Client      | Manifest                                             |
| ----------- | ---------------------------------------------------- |
| Codex       | `plugins/hankcraft-skills/.codex-plugin/plugin.json`  |
| Claude Code | `plugins/hankcraft-skills/.claude-plugin/plugin.json` |

Marketplace catalogs live at `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`. They point to `plugins/hankcraft-skills`; they do not contain copies of skill instructions.

Files under `docs/` are project documentation. Because they are not named `SKILL.md`, skill installers do not publish them as capabilities.

## Add or change a skill

1. Read the existing skill, bundled resources, and related repository conventions.
2. Make the smallest change that addresses the intended use case.
3. Keep shared instructions client-neutral. Put vendor-only behavior in plugin metadata when needed.
4. Use relative paths inside the skill and avoid unused resource directories.
5. Validate the skill and both plugin packages before committing.

## Validate

Validate an individual skill:

```bash
uvx --from skills-ref==0.1.0 agentskills validate \
  plugins/hankcraft-skills/skills/<skill-name>
```

Validate Claude Code packaging:

```bash
claude plugin validate .
```

CI validates every published `SKILL.md`, all JSON manifests, and bundled Python syntax.

## Publish and update

Changes merged to GitHub become available to repository-based installers. For a release:

1. Update the version in both native plugin manifests.
2. Commit the release atomically.
3. Tag the repository with the same semantic version.
4. Confirm installation from `hankcraft/hankcraft-skills`.

Do not add a custom installer until supported clients require behavior that the shared Agent Skills installer and native marketplaces cannot provide.
