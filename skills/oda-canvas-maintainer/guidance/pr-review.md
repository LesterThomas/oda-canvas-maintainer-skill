---
name: pr-review
description: Generic pull request review workflow and checklist, used for every PR in every repo, before the repo-specific checks.
last_updated: 2026-09-28
---

# PR review

## Workflow

1. **Understand the intent before judging the code.**
   - Read the PR description and any ADR it cites.
   - **Read every comment on the PR, and every comment on each associated issue**: closing issues, and issues referenced in the PR body or title. `gather_item.py` returns them in `linked_issue_threads`.
     *Why:* decisions are often made in the issue discussion after the title and description were written. A review based only on the title or description can flag a deliberate decision as a defect. (learned 2026-09-28 from oda-canvas#613)
   - Summarise in one sentence what the PR is *for*.
   
   *Why:* alignment (criterion 1) can't be judged without knowing the purpose, and a clear summary helps the maintainer decide fast.
2. **Give maintainers' comments extra weight.** A comment from a maintainer (the maintainer themselves or a `co_maintainers` member) on the PR or an associated issue counts as the project's position.
   - When such a comment conflicts with the PR or issue title or description, trust the comment, and treat the later maintainer comment as the current decision.
   - Assess the PR against that decision, not against the stale wording.
   - A title or description that no longer matches the decision is at most a **non-blocking** suggestion to update it.
   
   *Why:* maintainers set scope and direction for the project, so their recorded decisions outrank a contributor's original framing. (learned 2026-09-28 from oda-canvas#613)
3. **Check what already exists.** Read:
   - CI status;
   - co-maintainer reviews;
   - Copilot review comments;
   - unresolved threads;
   - attached test reports.
   
   Don't repeat points already made. Say which Copilot comments are worth acting on and which are noise.
4. **Run the deterministic checks.** Run the repo's script if it has one (`canvas_pr_checks.py` for `oda-canvas`), then read the diff.
5. **Assess alignment, then quality** (see `approval-criteria.md`). Classify every finding as blocking or non-blocking.
6. **Decide the verdict.** First check the **base branch**. A PR into a branch other than `main` (for example `feature/ai-canvas-experimental-changes`) needs **no approval**: recommend **Comment**, and review on substance. Rules enforced on `main`, such as prerelease suffixes and CI checks, don't apply to the feature branch itself. If the PR fixes something that is also broken on `main`, **close the PR and open a maintainer-owned issue against `main`** that lists the fixes to carry over, credits the author, and says what is left out and why (for example unexplained or incorrect changes). Don't ask the contributor to re-raise it against `main`. Draft both the issue and a short closing comment that points to it and invites the author to pick up any item. *Why:* the maintainer keeps control of what reaches `main`, the useful fixes don't wait on the contributor, and the contributor is still credited. (learned 2026-09-29 from oda-canvas#601) *Why:* feature branches belong to their owners, and approval gates `main`, but fixes shouldn't be stranded on a side branch. (learned 2026-09-29 from eval review, oda-canvas#601)

   For PRs into `main`:
   - **Approve:** aligned, no blocking findings, required CI green. Pending or long-running BDD runs are acceptable only if test evidence is attached.
   - **Request changes:** at least one blocking finding the author must fix that needs judgement or real work. A lone *mechanical* fix, such as a version bump, is Approve with the fix requested (see `approval-criteria.md`).
   - **Comment:** alignment is uncertain, an ADR is needed, or questions must be answered before a verdict.
   
   Never recommend Approve while required CI fails, or while blocking findings remain. If the maintainer wants to override, state what they are overriding.
7. **Draft the outputs:**
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

- 2026-09-29 — changed — non-`main` PRs whose fixes belong on `main`: close, and open a maintainer-owned issue listing the fixes to carry over (replaces "ask the author to port to main") — Lester, #601
- 2026-09-29 — added — PRs into non-`main` branches: Comment only, and suggest applying the fixes to `main` too — Lester's review of the #601 eval runs
- 2026-09-28 — changed — verdict: a lone mechanical fix means Approve with the fix requested, not Request changes — Lester, #613
- 2026-09-28 — added — read all comments on the PR and associated issues; weight maintainer comments above titles and descriptions — Lester: the #613 review flagged the deliberate removal of `sse` because #612's discussion wasn't read
- 2026-09-28 — added — seed from spec §7.2 and `research/review-norms.md`
