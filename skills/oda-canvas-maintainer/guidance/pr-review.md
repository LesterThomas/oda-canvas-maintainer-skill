---
name: pr-review
description: Generic pull request review workflow and checklist, used for every PR in every repo, before the repo-specific checks.
last_updated: 2026-09-28
---

# PR review

## Workflow

1. **Understand the intent before judging the code.**
   - Read the PR description, the linked issues and any ADR it cites.
   - Summarise in one sentence what the PR is *for*.
   
   *Why:* alignment (criterion 1) can't be judged without knowing the purpose, and a clear summary helps the maintainer decide fast.
2. **Check what already exists.** Read:
   - CI status;
   - co-maintainer reviews;
   - Copilot review comments;
   - unresolved threads;
   - attached test reports.
   
   Don't repeat points already made. Say which Copilot comments are worth acting on and which are noise.
3. **Run the deterministic checks.** Run the repo's script if it has one (`canvas_pr_checks.py` for `oda-canvas`), then read the diff.
4. **Assess alignment, then quality** (see `approval-criteria.md`). Classify every finding as blocking or non-blocking.
5. **Decide the verdict:**
   - **Approve:** aligned, no blocking findings, required CI green. Pending or long-running BDD runs are acceptable only if test evidence is attached.
   - **Request changes:** at least one blocking finding the author must fix.
   - **Comment:** alignment is uncertain, an ADR is needed, or questions must be answered before a verdict.
   
   Never recommend Approve while required CI fails, or while blocking findings remain. If the maintainer wants to override, state what they are overriding.
6. **Draft the outputs:**
   - the summary comment;
   - inline comments;
   - follow-up issues for non-blocking points worth tracking;
   - the command lines.

## Checklist

- **Scope.** The PR does one thing and matches its description and linked issue. Bundled topics are fine when they are justified (#573), but they must be explained.
- **Correctness.** Logic, edge cases, error handling, and behaviour on upgrade and delete paths. For operators, check idempotency, and that status and finalizers are handled correctly on delete.
- **Tests and evidence.** Behaviour changes need BDD scenarios or unit tests that would fail without the change. The evidence can be CI `run_tests_job`, or a test-report PDF attached to the PR. The full BDD suite is long, and maintainers attach local reports, so treat an attachment as valid evidence.
- **Docs.** README, use case or design docs are updated when behaviour changes. Missing docs for a new capability is usually a follow-up, not a blocker.
- **Security.**
  - secrets in code or values;
  - RBAC broader than needed in *new* resources;
  - `latest` image tags;
  - unpinned third-party Actions;
  - broad workflow `permissions:`;
  - `pull_request_target` misuse;
  - new network exposure.
- **Dependencies.** New dependencies are justified, maintained and Apache-2.0 compatible.
- **Hygiene.**
  - no committed planning or scratch files (`PLAN-*.md`, notes, `*.orig`, oddly named files such as `-w`);
  - no formatting churn mixed into logic changes;
  - no hand-edits to generated files.
- **CI.** Tell a real failure apart from a known flake or an infrastructure limit. Lint failures in code the PR didn't touch are **out of scope** for the PR (Lester, #573/#596).

## Evidence discipline

Every finding cites evidence: `path:line`, a CI job name, or a quoted line. If the diff was truncated, or files weren't read, say so under "Not verified". Never imply tests were run when they weren't.

## Change log

- 2026-09-28 — added — seed from spec §7.2 and `research/review-norms.md`
