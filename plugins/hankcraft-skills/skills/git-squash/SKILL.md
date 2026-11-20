---
name: git-squash
description: Rewrite a local feature branch into atomic commits. Use when asked to squash, split, or regroup existing commits before review, including branches with OpenSpec tasks.
---

# Squash a feature branch

Preserve the feature tip's exact Git tree. Each new commit should deliver one independently reviewable change, with its tests, callers, and fixtures.

## Identify the range

1. Use the named local feature branch, defaulting to the current branch. Identify its integration target from the request, PR base, or repository conventions. A feature branch's tracking remote often points to the feature itself. Ask if the target is ambiguous or the selected branch is protected.
2. Record the short branch name as `feature` and resolve `old` with `git rev-parse --verify "refs/heads/$feature^{commit}"`. Use `git merge-base --all "$target" "$old"` to find the fork point, `base`. Start the replacement history there, even if the integration target has advanced. Resolve a missing or ambiguous fork point before rewriting.
3. Inspect `git log --graph --oneline "$base..$old"` and `git diff --stat "$base" "$old"`, then read the patches. Check merge parents for another branch's history before flattening a merge. Clarify any history that must retain its ancestry. Leave the branch in place if the range is empty or its commits already satisfy the grouping rules below.

## Group the changes

Order commits by dependency. Fold fixups into the change they fix. Split mixed commits at hunk level, even when two behaviors share a file. Use `<type>(<scope>): <subject>` and include the root cause in bug-fix messages.

When the branch contains an OpenSpec change, read its proposal, specs, and task list alongside the implementation diff.

- Commit new planning artifacts together before implementation. In that planning snapshot, introduce new tasks unchecked and preserve task states inherited from the base.
- Map every newly checked task to the commit that completes and verifies it. Stage its `[ ]` to `[x]` edit with the corresponding code and tests. Tasks that need the same indivisible change can share a commit. Leave unfinished tasks open.
- Reconstruct intermediate versions of `tasks.md` when the original branch checked several boxes at once. For example, the commit implementing task 1.1 checks only 1.1. The commit implementing 1.2 checks 1.2. If a checked task lacks supporting work or verification, flag the mismatch before replacing the branch.

## Rebuild and verify

1. Inspect the feature worktree for a merge, rebase, or other Git operation in progress. Defer moving its branch until the operation finishes. Create a uniquely named local backup with `git branch "$backup" "$old"` and a detached scratch worktree with `git worktree add --detach "$scratch" "$base"`. Leave the user's index, working files, and untracked files alone.
2. Build each planned commit in the scratch worktree. Restore whole paths from `old` when they belong to one commit. For shared paths, reconstruct only the current commit's hunks. Review `git diff --cached`, run the relevant checks against that snapshot, and commit. Keep later tasks' changes out of the scratch worktree until their turn.
3. Record the candidate tip as `new`. Inspect `git log --reverse -p "$base..$new"` for commit boundaries and task ticks. Require identical tree IDs from `git rev-parse "$old^{tree}"` and `git rev-parse "$new^{tree}"`. On any mismatch or failed required check, keep the feature ref at its original tip.
4. After verification, run `git update-ref -m "squash feature commits" "refs/heads/$feature" "$new" "$old"`. The expected old tip protects concurrent commits. If the update fails, stop and inspect the branch. After success, remove the clean scratch worktree and retain the backup.

Report the base, rewritten commits, checks, and backup branch. Rewriting changes commit IDs. Leave remotes alone unless the user explicitly requests a push.
