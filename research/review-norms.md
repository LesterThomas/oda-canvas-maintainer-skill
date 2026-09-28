# Review norms observed in oda-canvas (task 1.3)

**Sample** (collected 2026-09-28):
- the last 60 closed PRs (#5xx–#608, created 2025-06 → 2026-09): 56 merged, 4 closed without merging;
- the last 100 inline review comments;
- the last 40 closed issues;
- all 67 open issues and all 8 open PRs.

Lester's own reviews are weighted most heavily, because this skill is personal (spec §2). This file is the main input to the seed guidance in Phase 2.

## 1. How Lester reviews: the patterns to reproduce

These patterns come from Lester's reviews on #513, #573, #581, #596, #598, #602, #603 and #608.

1. **Approve, and move the non-blocking points into follow-up issues.** This is the strongest pattern. Lester approves when the PR is valuable and good enough, and raises *separate issues* for the rest instead of holding the PR:
   - #603: approved, while creating #611 (docs, tests, image builds), #610 (RBAC too broad) and #609 (future role-based access);
   - #598: "doesn't have to be addressed as part of this PR";
   - #602: "These don't need to be fixed for the demo…, but we should look to apply as a fix at a later date."

   → The seed rule for `approval-criteria.md` and `pr-review.md`: *when the only concerns are non-blocking, recommend Approve and draft follow-up issue text for each concern.*
2. **Warm, specific praise that names the contributor and the value.**
   - "This is an excellent contribution - the first demonstration of a Carbon Management operator working in the Canvas." (#602)
   - "Kudos to @RJ-acc for such an impressive contribution." (#603)
   - "Thanks @arusakov-rh, good catch." (#608)

   The praise is never generic. It says *what* is good and *why* it matters to the Canvas.
3. **Explains the reasoning in domain terms.** #608 explains *why* the fix is right: the CRD schema, the required field, and how later steps override the default. The approval shows the reviewer understood the change.
4. **Architectural alignment is where Lester adds most value.** His substantive comments are almost all about ODA/Canvas design fit, not code style:
   - **Portability of Custom Resources.** CRs shouldn't embed Canvas-internal service URLs. Use fixed, well-known Canvas URLs instead (for example `info.canvas.svc.cluster.local`), so CRs run on *any* Canvas (#602).
   - **Consistency across the component segments.** A change to `coreFunction` should probably apply to `managementFunction` and `securityFunction` as well (#581, #573).
   - **CRD semantics.** If v4 and v5 of an API become two `ExposedAPI` resources, then the `specification` array should go (#581).
   - **Don't break reasonable downstream assumptions.** Sub-resource names are expected to match the Component definition, and changing them broke the ProductCatalog reference component and the DependentAPI operator (#573).
   - **Keep the base Canvas small.** Heavy capabilities, such as the observability stack, are optional charts that aren't installed by default (#518).
   - **Right layer, right data.** The Resource Inventory translates the Kubernetes API and stores nothing, so it shouldn't get a MongoDB (#513).
5. **Pragmatic about timing.** For example: "It would be good to merge before the DTW demo's on Tuesday." Event and demo deadlines are a legitimate reason to approve now and fix later.
6. **Keep PRs scoped, but accept a justified bundle.** Lester accepted a reviewer's "two topics in one PR" objection only partly, explaining why the bundle was needed (#573). He also treats **lint fixes in untouched code as out of scope** (#573, #596: "I'll leave lint errors until after the PR is reviewed").
7. **Tests as evidence.** Because the BDD suite is long and flaky on GitHub runners, Lester attaches local **test-report PDFs** to PRs (#518, #573). A PR changing behaviour should show BDD evidence, either from CI or attached.
8. **Directs coding agents directly.** Lester comments "@copilot - follow the instructions in docs/developer/work-with-dockerimages.md to…" (#571). Copilot SWE agent PRs are a normal contribution path, and the skill may draft instructions *to an agent* as well as to a human.

**Tone:** friendly, direct and brief. Lester writes in the first person ("I'm happy to approve", "I've added some issues…"), uses @-mentions, and doesn't use Conventional Comments labels himself. Short approvals such as "LGTM" or "Looks good to me" are normal for small or trusted PRs.

→ **Decision for `comment-style.md`:** Conventional Comments labels are used for **inline** comments, where blocking versus non-blocking matters. The **summary** comment is written in Lester's natural voice with no labels. The spec §5.3 wording should be adjusted to match.

## 2. What the other maintainers check (the unwritten checklist)

These points come from inline comments by ferenc-hechler and brian-burton. Each seeds a check in `repos/oda-canvas.md`:

- **Prerelease suffixes must be cleared before merge** (#596). CI enforces this; reviewers remind authors.
- **Chart patch versions must be bumped** for chart changes (#516: "Some charts need their patch versions bumped up").
- **Versions must match across charts.** A version bump in `canvas-oda/values.yaml` must also be made in the sub-chart `values.yaml` (#573).
- **Generated workflow files must not be hand-edited.** Add the image to `automation/generators/dockerbuild-workflow-generator/dockerbuild-config.yaml` and regenerate, following `docs/developer/work-with-dockerimages.md` (#596). The comment noted this was "most likely from the AI".
- **Formatting-only churn hides real changes** (#596: "hard to see whether there have been code changes or only formatting changes"). Reformatting belongs in a separate PR.
- **Stray AI artefacts must be removed**, for example a `PLAN-582.md` planning file (#596) and a file literally named `-w` from a broken CLI call. These are common in AI-generated PRs, and they are quality issues to flag.
- **Dockerfile naming and folder structure** should follow the existing operator pattern (#596).
- **Code duplication across segments.** Suggest a generic function parameterised by segment (#573).
- **Name clashes.** Sub-resource naming must not collide across core, management and security (#573).
- **CRD descriptions** should document defaults and interpretation, for example that a missing `segment` means `coreFunction` (#573).
- **Docs must follow the writing style guide** (#567, hyphenating "use-case"). Consistency matters more than which form is used.
- **Config correctness in docs and test data**, for example missing `/v1/traces` paths (#518).

## 3. Responsiveness

- **PRs:**
  - median time to the first non-author response is **23 h**, but the 75th percentile is **166 h** (about 7 days);
  - median time to merge is **60 h**, with the 75th percentile at about 20 days.
- **External PRs wait much longer.** 43 of the 60 PRs were authored by maintainers.
- **All 8 open PRs currently have no maintainer review.**
  - Three are from an external contributor (`csotiriou`) and have waited since **Feb–May 2025**: #456, #468 and #490.
  - #574 (NoNickeD) has waited since Dec 2025, with only Copilot's automated review.
  - #601, #605 and #607 are more recent external PRs.
  - Only #613 (anshulkumar-tmf, opened today) is from a co-maintainer.
- **Issues:**
  - closed issues are mostly maintainers' own work items;
  - 18 of the 40 closed issues had no comments at all;
  - when an issue did get a response, the median wait was 1 day.
- **The open backlog is the big problem.** There are 67 open issues:
  - median age **580 days**;
  - 50 older than a year;
  - 58 idle for more than 60 days;
  - 36 with no comments at all;
  - **11 external issues have never had a maintainer response**: #583, #534, #532, #315, #314, #281, #220, #210, #154, #106 and #105.

**Implication for the queue:** at launch, the queue (§4.1) should put the **unreviewed external PRs** and the **unanswered external issues** first. A dedicated backlog-sweep flow (§4.5) will be needed to bring the 580-day backlog under control. The sweep should classify each stale issue as done or superseded, still valid, or needing information, and draft closing or refresh comments in batches.

Defaults for spec Q8 (7 days with no response, 60 days stale) are consistent with the data. Keep them.

## 4. Issue conventions in practice

- About half of issue titles follow the `<component/operator/ctk>: subject` pattern (19 of 40). **Don't nag** contributors about titles.
- Labels actually used on issues: `bug-fix`, `feature`, `refactor`, `documentation`, `help wanted`, `Priority for Launch`.
- Maintainers close issues with a short pointer to the fixing PR, for example "Fixed as part of #562" or "Fixed in #506. Thanks @hrodrigues-hestia!". The skill should draft these closures when a merged PR clearly resolves an issue that is still open.
- Lester's issue replies either:
  - **commit to an action** ("I'll update the Action to pin the Helm version…"); or
  - **judge validity against Canvas scope** ("It should be part of the Canvas reference implementation to allow components in different namespaces…", #448).
- Issues that ask for new capabilities get an answer about whether they fit the Canvas's purpose. This is the alignment criterion (task 1.5) applied to issues.

## 5. Consequences for the spec

- Add `co_maintainers` defaults (see `governance.md`). Self-merge by maintainers is normal and shouldn't be flagged.
- Read and triage **Copilot review comments** rather than duplicating them.
- Add "raise follow-up issues" as a standard output of PR review. The Brief gains a **Draft follow-up issues** section.
- Adjust spec §5.3: Conventional Comments labels apply to inline comments only, and the summary uses Lester's voice.
- Add a **backlog sweep** use case to §4.5.
- Attached test-report PDFs count as evidence of BDD runs.
