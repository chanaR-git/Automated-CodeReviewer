---
name: git-version-control
description: 'Use when managing Git version control in a GitHub repository: inspect status and history, create or switch branches, stage and commit changes, sync with a remote, or push a branch to origin.'
argument-hint: 'Describe the Git operation you want, such as reviewing changes, committing, or pushing a branch.'
---

# Git Version Control

Use this skill to perform requested Git operations safely in the current repository, including working-tree inspection, branch management, staging, commits, and pushing to a GitHub remote.

## Safety Rules

- Perform only the Git operations the user requested or previously authorized. When a coherent coding task is complete and validated, recommend a commit as the normal professional next step, but do not create it unless the user requested or authorized committing.
- Before changing repository state, inspect the current branch, working tree, staged changes, and relevant remote/tracking configuration. Preserve pre-existing and unrelated user changes.
- Review the exact staged diff before committing. Stage only files relevant to the requested commit; prefer explicit paths over `git add .` or `git add -A`.
- Never include credentials, tokens, private keys, `.env` files, or other secrets in a commit. Do not print, request, or transmit credentials. Let Git's configured credential manager handle authentication.
- Do not run destructive commands such as `git reset --hard`, `git clean`, deleting branches, rewriting history, or force-pushing unless the user explicitly requests that specific operation. Explain the consequence and confirm before proceeding if the request is ambiguous or the operation could discard or overwrite work.
- Do not use `--force` as a routine fix. Prefer a normal push and investigate divergence or rejection first. If force-pushing is explicitly requested and appropriate, use `--force-with-lease` and verify the target branch and remote first.
- Never assume the remote is named `origin`, the default branch is `main`, or that the current branch is safe to push. Inspect configuration and confirm the target.
- Do not change global Git configuration. Ask before changing repository configuration that affects future Git behavior.

## Procedure

1. **Understand the request.** Identify whether the user wants inspection, branch creation/switching, staging, a commit, synchronization, a push, or a pull request. Resolve the intended commit contents, commit message, and push target from the request and repository context. Ask a concise question only if an ambiguity could cause the wrong changes to be committed, pushed, or proposed for merge.
2. **Inspect repository state.** Run these separately and review the results:

   ```sh
   git status --short --branch
   git branch --show-current
   git remote -v
   git branch -vv
   git diff
   git diff --cached
   ```

   Use only the relevant inspection commands when the request is narrower. If this is not a Git repository, stop and explain what is missing.
3. **Check repository guidance and ignore rules when relevant.** Review project-specific Git instructions, `.gitignore`, and likely generated or sensitive files before staging. Do not stage files just because they are modified.
4. **Prepare the requested change.** For branch creation or switching, check for uncommitted work first and preserve it. For staging, add only the requested paths, for example `git add path/to/file`. For sync operations, inspect upstream and divergence before choosing `fetch`, `pull`, or rebase behavior. Do not silently resolve conflicts or discard edits.
5. **Verify staged content.** Run `git status --short` and `git diff --cached`; confirm the staged paths and patch match the user's intent and contain no secrets or unrelated changes. Unstage unintended paths without altering their working-tree contents.
6. **Commit at meaningful checkpoints.** A commit is suitable when a small feature, bug fix, refactor, or documentation change forms a coherent unit, its relevant checks pass, and the staged diff has been reviewed. For a larger task, prefer separate commits for independently understandable, working milestones rather than one oversized commit or a trail of trivial commits. Avoid committing incomplete, known-broken, or unrelated work unless the user explicitly requests a work-in-progress checkpoint. Use a concise message that says what the change does. Create the commit only when requested or authorized; otherwise, tell the user the work is ready for a commit. After committing, verify with `git status --short --branch` and `git log -1 --oneline`. If a hook rejects the commit, inspect its output and address the relevant issue; do not bypass hooks unless explicitly requested.
7. **Push only when requested or authorized.** Confirm the remote and destination branch from repository configuration and the user's request. Prefer the configured upstream when it matches the request; otherwise use an explicit remote and branch, such as `git push origin feature-branch`. If no upstream exists, set one only for the confirmed target, e.g. `git push --set-upstream origin feature-branch`. If the push is rejected, inspect the reason and report it; do not force-push or rewrite history to make it pass.
8. **Use a pull request workflow for reviewable changes.** Unless the repository or user specifies otherwise, start from the current default branch, fetch and update it using the project's established merge/rebase policy, and create a descriptive branch for the task. Keep the branch focused; make reviewable commits at the checkpoints described above; run relevant tests and checks before pushing. Push the feature branch, then open a PR targeting the repository's default branch only when the user requested or authorized PR creation. The PR should have a concise title, context and rationale, a summary of behavior changes, test/check results, and any known risks or follow-up work. Link relevant issues when supplied; do not invent issue references. After opening it, report the PR URL and target. For review feedback, inspect the comment in context, make the requested change when clear, rerun relevant checks, commit and push updates only as authorized, and report what changed. Do not merge a PR unless explicitly requested. Before merging, verify the target, required reviews, CI/check status, and conflicts; use the repository's normal merge method. Delete a remote branch only when requested or clearly part of an explicitly authorized merge workflow and confirmed safe.
9. **Report the outcome.** State the branch, files or commit affected, remote/branch pushed and PR URL when applicable, and the result of each command or verification. Distinguish completed operations from ones blocked by authentication, conflicts, hooks, CI, review requirements, or remote errors.

## Common Commands

Run commands individually and inspect output before proceeding:

```sh
git status --short --branch
git log --oneline -n 10
git switch -c feature/short-description
git switch existing-branch
git add path/to/file
git diff --cached
git commit -m "Describe the change"
git fetch origin
git push origin feature-branch
```

Use the actual remote and branch names found in the repository. Avoid `git pull` without first checking the upstream and the repository's expected merge or rebase policy.

## Commit Message Guidance

- Prefer a short imperative subject, such as `Add retry handling to GitHub client` or `Fix empty configuration parsing`.
- Keep each commit focused on one logical change. Include tests with the behavior they verify.
- Follow any commit-message convention already used by the repository (for example, Conventional Commits) instead of imposing a new one.
- Do not amend or rewrite commits that may already be shared unless the user explicitly requests it and the consequences are understood.