---
name: create-pr
description: Draft or open a GitHub pull request or GitLab merge request based on the origin remote. Use the repository template, concise Traditional Chinese bullets, and verified test evidence while preserving commits.
---

# Create a PR or MR

Write concise bullets in Traditional Chinese by default. Retain familiar English technical terms. Explain what changed, why it matters, and where reviewers should focus.

## Establish scope and evidence

- Resolve the host and full repository path from `git remote get-url origin`, including HTTPS, SSH, and scp-style URLs. Use GitHub PRs for `github.com` and GitLab MRs for `gitlab.com`. For custom hosts or SSH aliases, confirm the provider from host configuration or authenticated repository metadata. If the destination is still unclear, ask before publishing.
- Read applicable repository instructions. Resolve the current branch, target branch, working-tree state, and included commits. Compare the full change against the repository's integration branch or the requested target. Fetch the target when its remote state matters.
- Preserve individual commits throughout creation and merge. Do not squash or rewrite the feature branch, or include unrelated working-tree changes.
- Resolve the ticket and issue URL from task context, branch, commits, or the configured tracker. Never invent a ticket or URL. Ask if the required ticket or target cannot be established. If the project has no ticket convention, follow its title convention instead of fabricating a ticket.
- Read the relevant OpenSpec proposal, design, task status, and evidence when present. Report the selected tasks' status separately from the whole change. Use `n/a` for an OpenSpec field outside OpenSpec projects. Opening a PR or MR does not authorize archiving a change.
- Trace the changed behavior far enough to explain ownership, compatibility, and impact. Inspect changed files and relevant callers without conducting an unsolicited repository audit. Identify schema, authorization, validation, secrets, external-service, PII, retention, and configuration implications from evidence.
- Reuse existing verification when its revision and scope still apply. Compare relevant source when reusing an older run. Run missing checks required by the repository or justified by the change.
- Distinguish current-HEAD checks, historical acceptance, and pending work. For each material claim, retain the command, result, environment, revision when relevant, and evidence link. Discovery and compilation do not prove runtime behavior. Include meaningful before/after regression results when available. State why new tests were unnecessary when none were added.

## Write the title and body

### Title

- Use `<ticket> <imperative subject>`, such as `ST-12 Reject expired session tokens`.
- Keep the title at most 72 characters, with no trailing period.

### Description

- Read the target repository's template each time. Use the template named by the user or repository. Otherwise look for GitHub's `pull_request_template.md` or `PULL_REQUEST_TEMPLATE/` in the root, `.github/`, or `docs/` (including case variants), or GitLab's `.gitlab/merge_request_templates/*.md`.
- Prefer the platform default (such as GitLab's `Default.md`), then the sole or clearly matching template. If the repository only has a template for the other platform, reuse it. Ask only if ambiguity changes required content. If no template exists, report that and draft concise bullets from the review evidence.
- Keep the template's headings, order, fields, and checklists. When template instructions conflict with this skill, follow the skill for the conflicting part and keep the rest. Fill free-text sections with short bullets, one point per bullet. Mark checklist items complete only with supporting evidence.
- Put the ticket, OpenSpec task status, behavior and ownership changes, compatibility, security impact, test evidence, risks, and rollback details in the relevant template fields. Add missing information when repository rules or material review needs require it. Do not impose a fixed set of extra sections.
- Explain what changes and why. Name review hotspots and material tradeoffs. Link detailed logs rather than pasting them.

Use complete sentences where compression would obscure meaning. Summarize the change as a whole. Include its history only when it explains a material decision.

## Publish only within the request

- A request for title/body text authorizes drafting only. A request to open a PR or MR authorizes the necessary feature-branch push and request creation, subject to repository rules.
- Check for an open request with the same target repository, source repository, and branches. Reuse it and update metadata only within the requested scope.
- Finish the title, body, and required checks first. Honor draft status and repository readiness rules. Pass the resolved repository and branches explicitly. For CLI publication, write the body to a UTF-8 temporary file.
- **GitHub** — Prefer connected GitHub tools when sufficient. Otherwise use authenticated `gh pr create` with `--body-file` and report the fallback. If asked to merge, select an allowed merge method that keeps the commits.
- **GitLab** — Use authenticated `glab mr create` with `--description-file` and `--squash-before-merge=false`, or the GitLab API with `squash=false`. Verify the MR's effective squash setting on readback.
- If either platform requires squashing, report the policy conflict and leave the request unmerged.
- Read the request back. Verify its title, complete body, target branch, head commit, and draft status. Confirm the working tree contains no unintended changes.
- Return the PR or MR URL, target branch, verification result, and material pending checks or risks. Report running CI as pending. Waiting for CI, merging, enabling auto-merge, and changing project settings require separate authorization.
