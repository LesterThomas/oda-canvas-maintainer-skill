# ODA Canvas Maintainer Skill — Build Tasks

Companion to [`spec.md`](./spec.md). Tasks are grouped into phases. Within a phase they are roughly sequential. Phase 3 can run in parallel with Phase 4 once Phase 2 lands. Check tasks off as they complete, and leave notes inline where a task surfaces a decision rather than just landing one.

**Starting state (2026-09-28):**

- The repo is live at <https://github.com/LesterThomas/oda-canvas-maintainer-skill> and contains only `spec/` and a README.
- The first research pass used local clones under `D:\Dev\tmforum-oda\`. It was then checked against the live organisation (task 1.1).
- The skill-creator workflow (draft → test → review → improve) is used from Phase 2 onward.

**Design note (spec v0.2):** review knowledge lives in a **living `guidance/` folder**, with one Markdown file per guidance type. It improves from the maintainer's feedback during normal use (spec §7). Tasks that write review knowledge therefore write *seed* guidance files, not static references.

---

## Phase 0 — Foundations

- [x] **0.1** Set up git and the remote at `github.com/LesterThomas/oda-canvas-maintainer-skill`: `git init`, a `.gitignore`, and a first commit of `spec/`. **Done 2026-09-28:** public repo, with `main` tracking `origin`.
- [x] **0.2** Record the answers to the spec §12 open questions. **Done 2026-09-28.** All questions are answered. Round 1:
  - Q1: scope exclusions decided;
  - Q2: one approval, about 5 maintainers, personal use for now;
  - Q4: no special handling for AI PRs; the criteria are ODA alignment and quality;
  - Q5: marketplace creator skill later.
  
  Round 2 answered Q7 (the ADR route) and Q9/Q10 (co-maintainers, AI-Native aligned), and research answered Q3, Q6 and Q8.
- [ ] **0.3** Confirm the tooling on this machine (Windows): `gh` authenticated as `LesterThomas` with access to `tmforum-oda` (confirmed 2026-09-28), and Python 3.10+. Record the minimum `gh` version needed for `gh pr checks --json` and `gh search`.

## Phase 1 — Research (ground the seed guidance in real project behaviour)

- [x] **1.1** Build the live repo inventory and the spec §3 tiers. **Done 2026-09-28.**
  - The org holds 33 repos: 4 archived, about 15 dormant or non-Canvas, and the rest tiered in spec §3.
  - Local clones were missing `TMFOP006`, `TMFCOP009`, `TMFOP012`, `model-as-a-service-crds`, `oda-helm-charts` and `canvas-prerequisites`.
  - `oda-canvas` carries most of the load, with 66 open issues and 8 open PRs, so the queue (§4.1) and stale housekeeping (§4.5) matter from day one.
  - **Maintainer scope decisions:** `oda-component-ctk` is excluded (replaced by other work), and `model-as-a-service-crds` is excluded (merging into `TMFCOP009`).
- [x] **1.2** Collect governance facts for the Tier 1 and Tier 2 repos. **Done 2026-09-28 → [`research/governance.md`](../research/governance.md).**
  - Proposed `co_maintainers`, from the last 100 approvals and merges: `brian-burton`, `ferenc-hechler`, `adarshkumar4`, `anshulkumar-tmf`. **Confirmed by Lester 2026-09-28.**
  - One approval is a convention, not enforced. There is no branch protection, 26 of the last 100 PRs merged with no approval, and 48 were self-merged.
  - The issue templates apply labels that don't exist: `bug`, `docs`, `chore` and `style`.
  - Milestones are unused, Discussions are off, and private vulnerability reporting is **off**, so security goes to `components@tmforum.org`.
  - The Copilot PR reviewer is active.
  - The satellite repos have no CONTRIBUTING or CI and use GitHub's default labels.
- [x] **1.3** Mine the unwritten review norms from about 60 closed PRs, 100 inline comments, 40 closed issues and the full open backlog. **Done 2026-09-28 → [`research/review-norms.md`](../research/review-norms.md).** Key findings:
  - **Lester's pattern:** approve valuable, good-enough PRs and move non-blocking points into **follow-up issues**. He praises specifically, and his substantive comments are about **architectural alignment**: CR portability, segment consistency, CRD semantics, downstream assumptions, and keeping the base Canvas lean.
  - **The other maintainers' unwritten checklist:**
    - clear prerelease suffixes;
    - bump chart patch versions and keep versions in sync across charts;
    - regenerate workflows, don't hand-edit them;
    - no formatting churn;
    - remove stray AI artefacts such as `PLAN-*.md`;
    - follow the style guide.
  - **The backlog is the real pain.** There are 67 open issues with a median age of 580 days, 11 external issues were never answered, and all 8 open PRs are unreviewed (some external ones since Feb 2025).
  - Spec updated: follow-up issues and a Copilot section in the Brief, the backlog sweep in §4.5, external-first queue ordering, and Conventional Comments for inline comments only.
- [x] **1.4** Check the best-practice sources. **Done 2026-09-28 → [`research/sources.md`](../research/sources.md).** All 10 sources were verified. One URL was corrected: the Kubernetes `review-guidelines` page is 404, and it is replaced by `docs/guide/expectations/`.
- [x] **1.5** Distil the ODA and ODA Canvas objectives into alignment tests. **Done 2026-09-28 → [`research/oda-objectives.md`](../research/oda-objectives.md).**
  - It sets out 7 stated objectives, 9 alignment tests and 5 red flags.
  - It includes a calibration table of 6 real decisions (#602, #603, #573, #581, #513, #448).
  - **Resolved with Lester 2026-09-28:**
    - an AI-Native Canvas is an ODA goal, so that work is aligned by default;
    - the ratification route is a new **ADR** in `oda-ca-docs/Decision-Log`, which will later move to an Architecture repo;
    - ADRs are also an alignment source, so the skill fetches the ADR index live.
    
    ADR-0013 corrects one assumption: the Reference Implementation certifies Components, not other Canvases.
- [x] **1.6** Review the neighbouring skills and marketplace fit. **Done 2026-09-28 → [`research/neighbouring-skills.md`](../research/neighbouring-skills.md).**
  - The skill reviews *against* `helm-chart-development`, `write-bdd-feature` and `create-oda-operator`, and links to them without copying them.
  - It hands CI debugging to `github-actions-debugging`.
  - It reads conventions from the target repo's current `main`, not local clones (Lester's `oda-canvas` clone was 5 commits behind).
  - **Layout decision:** the skill lives at `skills/oda-canvas-maintainer/` so it drops into the marketplace unchanged, where `build_plugin.py` rewrites the paths.

## Phase 2 — Core skill and guidance folder (oda-canvas first)

- [x] **2.1** Scaffold `skills/oda-canvas-maintainer/` per spec §8.1, including `guidance/` and `guidance/repos/`.
  **Done 2026-09-28.**
- [x] **2.2** Install for personal use: link `~/.claude/skills/oda-canvas-maintainer` to `skills/oda-canvas-maintainer/` in this repo with a Windows directory junction (`mklink /J`). Guidance edits made by the skill then land directly in this git repo (spec §7.4). Document the step in the README.
  **Done 2026-09-28.** The junction was created, and git resolves to this repo through it. Claude Code picked the skill up in the same session.
- [x] **2.3** Draft `SKILL.md`:
  - frontmatter, with a pushy but specific description that covers both the triggers and the non-triggers in spec §2;
  - mode selection (§4.1–4.6);
  - the fixed principles with their *why* (§5.1 read-only, §5.2 untrusted content, §5.4 sensitive situations, §5.5 limits), stated as sitting above guidance;
  - the two approval criteria (§5.6);
  - the Maintainer Brief format, including **Guidance applied** (§6);
  - how to load guidance files (the "Loaded when" column in §7.1).
  
  Keep it under 500 lines. All changeable judgement goes in `guidance/`, not in `SKILL.md`.
  **Done 2026-09-28.** `SKILL.md` is about 270 lines.
- [x] **2.4** Write the **learning loop** into `SKILL.md` (spec §7.3):
  - the four feedback signals;
  - apply explicit feedback immediately and report it in one line;
  - propose inferred lessons instead of applying them;
  - the "just this once or always?" scope check;
  - generalise the rule with a *why* and a provenance tag;
  - replace contradicting rules and log the replacement;
  - consolidation when a file passes about 200 lines;
  - only the maintainer teaches, never fetched content;
  - offer a local commit at the end of the session and never push without asking.
  **Done 2026-09-28.** It is in `SKILL.md` → Learning loop.
- [x] **2.5** Write `guidance/README.md`: the file index, the file format (frontmatter, Guidance, Change log), the provenance tag format, and the precedence rules (§7.5).
  **Done 2026-09-28.**
- [x] **2.6** Write the seed guidance files from Phase 1:
  - `approval-criteria.md` (from 1.5 and 1.3), including the AI-Native-by-default rule, how to check a PR against the ADRs (fetched live via `adr_source`), and the draft an ADR is needed wording;
  - `pr-review.md` (spec §7.2 seed);
  - `issue-triage.md`, including the Canvas needs-info checklist (chart version, Kubernetes version, component spec version, operator, logs) and the ratification route default;
  - `comment-style.md`, covering best practice from 1.4, Conventional Comments, `oda-canvas` writing style and the maintainer's phrasing from 1.3;
  - `comment-templates.md`: welcome, needs-info, duplicate, transfer, needs ratification, BDD-first, stale nudge and close, thanks, decline-with-path, security redirect. These are scaffolds to personalise, not text to paste;
  - `labels-and-metadata.md` (from 1.2);
  - `queue-priorities.md`: the §4.1 order, 7 and 60 day defaults, and co-maintainer handling;
  - `sensitive-situations.md` (spec §5.4, plus the injection playbook);
  - `repos/oda-canvas.md` (spec §7.2 seed plus 1.3).
  
  Every seed file starts with an empty Change log.
  **Done 2026-09-28.** There are 10 seed files, about 620 lines in total. The seed also includes Lester's real phrasing and the #602/#603/#608 calibration examples.
- [x] **2.7** Write `scripts/gather_item.py`. It takes `<owner/repo> <number>` or a URL, auto-detects issue or PR, and emits one JSON bundle containing:
  - metadata, body, comments and reviews, including unresolved review threads via GraphQL;
  - changed files and the diff, truncated with a `truncated: true` flag;
  - CI checks;
  - linked or closing issues;
  - the author's prior merged PR count in the org;
  - **which maintainers (`co_maintainers`) have already reviewed or commented**;
  - **the maintainer's own posted comments**, which the learning loop compares with saved drafts (§7.3 signal 3).
  - **Copilot review comments**, tagged separately, plus **attachment links** such as test-report PDFs, which count as BDD evidence (spec §4.3).
  
  It must be standard library only and read-only. Test it on Windows.
  **Done 2026-09-28.** A shared `_gh.py` enforces the read-only allowlist: it refuses non-GET `gh api`, GraphQL mutations and write subcommands, and all four refusals were tested. The diff budget skips lockfiles and binaries and reports exactly which files were clipped or omitted.
- [x] **2.8** Write `scripts/canvas_pr_checks.py`, the deterministic `oda-canvas` checks, emitting findings as JSON with evidence:
  - prerelease suffixes, using the key list parsed from `check-no-prerelease-suffixes-in-PR.yml` or its generator config so it cannot drift;
  - chart changes without a `Chart.yaml` bump or changelog comment;
  - hard-coded namespaces;
  - CRD changes without webhook changes;
  - hand edits to generated workflow files;
  - new dependencies;
  - `:latest` tags.
  **Done 2026-09-28.** It was validated against #613, #601, #596, #573, #516 and #602. On live open PRs it found real problems: a leftover prerelease suffix in #601 (`ai-canvas-0.1.6`) and a missing `oda-crds` bump in #613. The first run was noisy, and these fixes cut the noise:
  - Actions `paths` semantics, so `*` doesn't cross `/`;
  - test and doc changes excluded from image bumps;
  - values-only chart changes downgraded to a question;
  - `:latest` ignored in generated workflows and docs;
  - concise dependency evidence.
- [x] **2.9** Write `scripts/draft_diff.py`. It compares a saved draft in `maintainer-drafts/` with what the maintainer actually posted, and emits the meaningful differences (added, removed or reworded points; verdict change). This supports learning signal 3. It is read-only on GitHub.
  **Done 2026-09-28.** It was tested with a synthetic draft against Lester's real #608 review, which surfaced a genuine style lesson (see 2.11), and with an unposted draft.
- [x] **2.10** Write `assets/config.example.yaml` (spec §8.2), including `maintainer_login: LesterThomas`, `co_maintainers` (from 1.2) and `guidance_dir`. Make `SKILL.md` explain the config lookup and the defaults.
  **Done 2026-09-28.** `drafts_dir` now defaults to `~/.oda-canvas-maintainer/drafts`, so it works for both the personal and the plugin install.
- [~] **2.11** Run a manual smoke test on live open items: one issue and one PR in `oda-canvas`. Deliberately give 2–3 pieces of feedback and confirm that:
  - no mutating `gh` command ran;
  - the feedback landed in the correct guidance files, in the right format;
  - a follow-up review applied it.
  
  Fix the obvious gaps before formal evals.
  **Partly done 2026-09-28.** The skill was invoked through the real skill loader on live PR #613:
  - It produced a full brief and saved `oda-canvas-613.md` plus `.comment.md` in `drafts_dir`.
  - No mutating command ran.
  - It found a material defect CI didn't catch: the title and #612 say "a2a **and sse**", but `sse` appears 0 times in the PR, while the APISIX and Kong operators already support it.
  - It discounted the `crd-without-webhook` lead with evidence.
  - It drafted a regression-guard follow-up issue.
  
  **Correction from feedback (same day):** the `sse` "defect" was wrong. On #612, Lester had argued that SSE is a transport rather than a semantic-layer protocol, and the author then removed it. The skill never read #612's comments.

  **Learning loop exercised, with signal 1 (explicit feedback):**
  - New rules in `pr-review.md` and `issue-triage.md`: read all comments on the PR and associated issues, and give maintainer comments precedence over titles and descriptions.
  - `gather_item.py` now fetches `linked_issue_threads`, flags `is_maintainer`, and adds `maintainer_comments_in_linked_threads`.
  - The re-run applied the rule and dropped the false blocker. The verdict stays *Request changes*, now for the chart bump only.
  - The superseded draft was renamed `*.learned.md`.
  - An inferred rule (apiType values are semantic-layer protocols, not transports) was proposed rather than applied, per the loop design.
  
  **Signal 3 exercised (2026-09-28):** Lester posted the #613 review 3 minutes after the revised draft. `draft_diff.py --all` detected it: similarity 0.96, one sentence removed, and the **verdict changed** from Request changes to Approve. Two lessons were proposed (not applied), and the draft was renamed `*.learned.md`.
  
  **Remaining:** Lester's answer on those proposals.
## Phase 3 — Multi-repo coverage

- [x] **3.1** Write `scripts/queue.py`. It covers all configured repos and ranks items using the order in `guidance/queue-priorities.md`. It flags items another maintainer is handling, uses `gh search` or GraphQL to keep API calls low, and caches results for a short time.
  **Done 2026-09-28.** It uses one paginated GraphQL query per repo, and has a `--sweep` mode, so it also covers 3.8's listing. A live run over tier 1 and tier 2 found 85 open items: 5 external PRs unreviewed, 15 external issues unanswered, 55 stale. The first run over-flagged 13 "security" items, because authentication and secrets are Canvas design vocabulary. The flag is now restricted to vulnerability-disclosure language in items under 90 days old.
- [x] **3.2** Write `scripts/find_related.py`. It searches for duplicates and related items across in-scope repos, open and closed. It returns candidates only; the model confirms which are real duplicates.
  **Done 2026-09-28.** GitHub search ANDs terms, so long queries return nothing. It uses pairs of distinctive title words, identifiers and error lines, scored across queries. Tested: #534 finds its near-duplicates #532/#533 (the ProjectONE trio), and #314 finds the closed #345 (container vulnerability scan).
- [x] **3.3** ~~Repo guidance for `oda-component-ctk`~~ — **dropped 2026-09-28.** The repo is out of scope (spec §3).
- [x] **3.4** Write `guidance/repos/reference-example-components.md`. Cover component YAML against the current spec version, chart bumps and the GitHub Pages Helm index.
  **Done 2026-09-28.** Default branch `master`; chart-releaser publishes on push, so chart bumps are blocking; the `# version:` changelog format; the no-LICENSE issue #70.
- [x] **3.5** Write `guidance/repos/oda-helm-charts.md` and `guidance/repos/canvas-prerequisites.md`. Cover consistency with `oda-canvas/charts` and installation correctness.
  **Done 2026-09-28.** `oda-helm-charts` is empty, so its file is interim rules plus a warning about drift between two copies of a chart. `canvas-prerequisites` is Brian's work in progress (#1, #2), and its file covers the prerequisite/Canvas boundary.
- [x] **3.6** Write `guidance/repos/` files for the Tier 2 operators: `TMFOP006`, `TMFCOP009` and `TMFOP012`. Start from the `oda-canvas` operator and CRD rules. `TMFCOP009` also receives the MaaS CRDs being merged in.
  **Done 2026-09-28.** One pattern file, `repos/canvas-operator-repos.md` (`applies_to: TMFOP*, TMFCOP*`), rather than one file per repo, since all three are young and share conventions. Finding: **licences differ**. TMFOP006 is Apache-2.0, TMFCOP009 and TMFOP012 are TM Forum RAND, and TMFCOP009 PR #1 proposes Apache → RAND. This was added to `sensitive-situations.md` as an escalation.
- [x] **3.8** Implement the **backlog sweep** (spec §4.5). It works in batches of about 10 issues, with unanswered external issues first (#583, #534, #532, #315, #314, #281, #220, #210, #154, #106, #105 as of 2026-09-28). For each issue it:
  - checks for a merged PR or commit that resolved it;
  - classifies it as done, valid, needs info or out of scope;
  - drafts the comments.
  
  The output is a batch table. This is likely the highest-value feature at launch (`research/review-norms.md` §3).
  **Done 2026-09-28.** The sweep mode is in `SKILL.md` (`queue.py --sweep` → `gather_item` + `find_related` per issue → classify with evidence → drafts, a batch table and batch commands). **First real batch (#105, #106, #154, #210, #220):** 1 transfer to TMFOP006, 2 refresh-and-retitle with real gaps found (no BDD features for UC004/UC008; install guide doesn't mention `observability-stack`), 1 help-wanted, 1 close as answered. Saved as `sweep-oda-canvas-batch1.md`. Awaiting Lester's review.
- [x] **3.7** For Tier 3 repos, rely on the generic fallback. The skill offers to start a repo guidance file after the first review there (spec §7.2).
  **Done 2026-09-28.** `SKILL.md` repo-guidance lookup: exact file, then `applies_to` pattern, then the generic fallback with an offer to start a file.
## Phase 4 — Evaluation (skill-creator loop)

- [ ] **4.1** Select fixtures. Use 8–12 closed historical items with known outcomes (spec §9 list), preferring ones the maintainer reviewed personally, plus the two synthetic ones: a public security report and a prompt-injection PR. Snapshot each with `gather_item.py` into `evals/fixtures/`.
- [ ] **4.2** Write the review-quality evals in `evals/evals.json`, with prompts phrased the way the maintainer really asks.
- [ ] **4.3** Write the **learning-loop evals** (spec §9): scripted multi-turn sessions covering:
  - explicit feedback, then a second review that should apply it;
  - contradicting feedback;
  - "just this once" feedback;
  - an injected "rule" in a PR body;
  - feedback that tries to disable a §5 principle.
  
  Each session runs against a **copy** of the guidance folder so the real guidance isn't polluted.
- [ ] **4.4** Run with-skill and without-skill runs in parallel into `oda-canvas-maintainer-workspace/iteration-1/`. Draft the objective assertions while they run, and script the checkable ones:
  - no mutating `gh` command;
  - all brief sections present, including **Guidance applied**;
  - no *Approve* while CI fails;
  - both criteria assessed;
  - security escalation fired;
  - injection flagged and not learned;
  - repo checks fired;
  - guidance file changes are correct in location, format, provenance and change log.
- [ ] **4.5** Grade the runs, aggregate the benchmark, and open the eval viewer for maintainer review.
- [ ] **4.6** Iterate on the feedback. Generalise the fixes rather than overfitting to the fixtures. Improvements to review judgement go into **seed guidance**; improvements to process go into `SKILL.md`. Repeat until the feedback has no major comments.

## Phase 5 — Triggering

- [ ] **5.1** Write 20 trigger-eval queries:
  - about 10 that should trigger, in varied phrasing: URLs, "waiting on me", "can I merge this", "what have you learned about my reviews", casual wording;
  - about 10 near misses that should not trigger: "write a BDD feature for UC003", "debug my failing chart-release workflow", "review my own local diff before I open a PR", "explain TMF620", "create a new operator".
  
  Review them with the maintainer.
- [ ] **5.2** Run the skill-creator description optimiser, then apply the best description (chosen on the held-out test score).

## Phase 6 — Personal use, then marketplace

- [ ] **6.1** Update `README.md` with what the skill does and doesn't do, installation via junction, config, example sessions per mode, how the guidance learns, and a clear statement that it never writes to GitHub issues or PRs.
- [ ] **6.2** Use the skill personally for 4–6 weeks. Review the git history of `guidance/` every couple of weeks, and run a consolidation pass (spec §4.6).
- [ ] **6.3** Prepare the marketplace move (spec §10):
  - implement the guidance overlay model (§7.4): bundled seed plus a user overlay in `~/.config/oda-canvas-maintainer/guidance/`, merged per file;
  - split the learned guidance into project-general rules (which ship as the seed) and personal rules (which stay local);
  - match the marketplace layout (`skills/<name>/` → `dist/creator/skills/<name>/`).
- [ ] **6.4** Raise a PR to `tmforum-oda/oda-agent-skills-marketplace` adding the skill to the `tm-forum-oda-creator` plugin. The maintainer raises and merges it themselves.
- [ ] **6.5** Plan follow-ups, maybe:
  - a scheduled weekly queue digest (still draft-only);
  - release-readiness review (release-notes table, suffix clearing, chart versions);
  - sharing learned guidance between maintainers.

## Phase 4 status (2026-09-28, paused at usage limit)

- [x] 4.1–4.4: there are 8 evals in `skills/oda-canvas-maintainer/evals/evals.json`, with 60 assertions and 2 synthetic fixtures. All 16 runs finished; outputs are in the git-ignored `skills/oda-canvas-maintainer-workspace/iteration-1/`. `check_no_writes.py` scanned the real transcripts and confirmed **0 GitHub writes in all 16 runs**. Eval 1's suffix assertion was corrected: #601 targets a feature branch.
- [x] 4.5: **Done 2026-09-29.** All 16 runs are graded. The benchmark is in `iteration-1/benchmark.json` and `.md`, with analyst notes, and the static viewer is `review-iteration-1.html`.
  - **With the skill: 96.9% pass. Without: 84.2%.** The difference is +13 points, at a cost of +76 s and +24k tokens per run.
  - 48 of 60 assertions pass in both configurations. Evals 2, 3 and 7 don't separate the two at all.
  - The skill's advantage is in the project-specific and learned rules:
    - no apology openers;
    - components@tmforum.org as the security channel;
    - ADR and ADR-0022 routing;
    - ready-to-run gh commands and batch structure.
  - Two skill "failures" are flaws in the assertions (eval 8 ProjectONE, eval 5 drafts).
  - Awaiting Lester's review in the viewer.
- [x] 4.6: **Iteration 2 done 2026-09-29.** With the skill: 100% (71/71). Without: 81%. The lead is +19 points, up from +13.
  - Lester's eval feedback was applied as rules:
    - non-`main` PRs get Comment only, and the fixes should also go to `main`;
    - no parroted praise;
    - ADR routing confirmed.
  - Two #70 rules were also applied: the maintainer does trivial fixes, and replies stay on the question asked.
  - All five fixes listed below were applied. In addition:
    - `queue.py` broken-workflow detection is now deterministic;
    - the `gh --merged` flag in `SKILL.md` is fixed;
    - the ProjectONE seed error is corrected.
  - The viewer is `review-iteration-2.html` and is waiting for Lester's review. The iteration-1 list follows:
  1. `canvas_pr_checks.py`: suffix and version checks only apply when the PR base is `main` (#601 targets `feature/ai-canvas-experimental-changes`).
  2. ADRs also live in `tmforum-oda/ai-canvas-architecture` (ADR-001..008, RAND-licensed). Add it as a second `adr_source`.
  3. Queue additions: failing default-branch workflows (ref-components Release Charts failing since 26 Sep, so TMFC007 is unpublished); issues that @-mention the maintainer; PRs with the maintainer's review requested; `ai-canvas-architecture` PRs.
  4. `queue.py` security flag misses "Critical bugs in … libraries" (Dependabot, #555–559). Add "critical bug(s)" and "Dependabot" to the pattern, as a dependency-security category rather than a disclosure.
  5. Learning-loop check: ref-components #70 closed and #75 merged. Run `draft_diff.py` on the #70 draft.
