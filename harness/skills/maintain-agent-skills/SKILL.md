---
name: maintain-agent-skills
description: Create or update portable Agent Skills and their distribution metadata. Use when maintaining SKILL.md packages shared across Codex, Claude Code, Antigravity, or similar clients.
license: MIT
---

# Maintain Agent Skills

Keep each capability in one canonical `SKILL.md` directory. Treat client plugin manifests as thin packaging around that shared implementation.

Requires Git. Distribution commands using `npx` also require Node.js.

## Workflow

1. Read the target skill and its bundled scripts, references, and callers before editing.
2. Make the smallest change that addresses a demonstrated need.
3. Keep core instructions client-neutral; isolate vendor-only behavior in plugin metadata or clearly named references.
4. Validate the changed skill and any affected plugin manifests.
5. Commit the change atomically and bump the plugin version only for a release.

## Distribution

- Publish the repository through Git.
- Use the shared `skills/` tree for cross-client installers.
- Keep `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` as wrappers; do not duplicate skill bodies.
- Add hooks, MCP servers, agents, or apps only when a skill cannot provide the required capability.

## Constraints

- Preserve portable `name` and `description` frontmatter.
- Use relative paths within a skill.
- Avoid client-specific tool names in shared instructions.
- Do not add empty resource directories or speculative adapters.
