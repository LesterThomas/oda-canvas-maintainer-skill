# ODA Canvas Maintainer Skill — Build Tasks

Companion to [`spec.md`](./spec.md). Tasks are grouped into phases. Within a phase they are roughly sequential. Phase 3 can run in parallel with Phase 4 once Phase 2 lands. Check tasks off as they complete, and leave notes inline where a task surfaces a decision rather than just landing one.

**Starting state:** an empty project folder with `spec/spec.md` drafted. There is no git repo yet.

Research so far used local clones under `D:\Dev\tmforum-oda\` only, because network tools were unavailable during drafting. Those clones are:

- `oda-canvas`
- `oda-component-ctk`
- `reference-example-components`
- `oda-ca-docs`
- `oda-agent-skllls-marketplace`
- `ai-canvas-architecture`
- `ai-impact-on-architecture`
- `AI-Augmented-Software-Engineering`

The skill-creator workflow (draft → test → review → improve) is used from Phase 2 onward.

---

## Phase 0 — Foundations

- [x] **0.1** **Done 2026-09-28.** Created as a public repo, with `main` tracking `origin`. Set up git and the remote at `github.com/LesterThomas/oda-canvas-maintainer-skill`. `git init`, add a `.gitignore` for `__pycache__/`, `.venv/`, `*-workspace/`, `maintainer-drafts/` and OS files, then commit `spec/` first so the plan has history from day one.
- [ ] **0.2** Get answers to spec §12 open questions Q1–Q8 from the maintainers, and record each answer inline in spec §12 with its date.
- [ ] **0.3** Confirm the tooling on at least one Windows and one macOS/Linux machine:
  - `gh` is installed and `gh auth status` is OK with access to `tmforum-oda`;
  - Python 3.10+ is available.
  
  Record the minimum `gh` version needed for `gh pr checks --json` and `gh search`.

## Phase 1 — Research (ground the skill in real project behaviour)

- [x] **1.1** Build the live repo inventory: `gh repo list tmforum-oda --limit 200 --json name,description,isArchived,pushedAt,primaryLanguage`. Update the spec §3 table and mark archived or inactive repos. For each active repo, record:
  - open issue and PR counts;
  - whether CONTRIBUTING, CODEOWNERS and a PR template exist.

  **Done 2026-09-28.** The org holds 33 repos: 4 archived, about 15 dormant or non-Canvas, and 15 active or relevant, now tiered in spec §3.

  Local clones were missing 6 relevant repos: the three operator repos (`TMFOP006`, `TMFCOP009`, `TMFOP012`), `model-as-a-service-crds`, `oda-helm-charts` and `canvas-prerequisites`.

  `oda-canvas` carries most of the load, with 66 open issues and 8 open PRs. This suggests the queue mode (§4.1) and stale-issue housekeeping (§4.5) will matter a lot at launch.

  **Scope decisions by the maintainer, 2026-09-28:**
  - `oda-component-ctk` is excluded, because it has been replaced by other work.
  - `model-as-a-service-crds` is excluded, because it is being merged into `TMFCOP009-model-as-a-service-operator`.

  **Still to do:** the CONTRIBUTING, CODEOWNERS and PR-template presence check per repo. It moves into 1.2.
- [ ] **1.2** Collect governance facts for `oda-canvas` and the other active repos:
  - labels (`gh label list`);
  - milestones;
  - CODEOWNERS;
  - branch protection and required checks, via `gh api repos/{o}/{r}/branches/main/protection` (this may need admin rights, so otherwise infer from PR check lists);
  - whether private vulnerability reporting is enabled;
  - whether Discussions are enabled.
- [ ] **1.3** Mine the unwritten review norms from a sample of about 30 recently merged or closed PRs and about 30 closed issues in `oda-canvas`. Note:
  - what maintainers actually ask for;
  - typical time to first response;
  - approval count;
  - how prerelease-suffix, chart-bump and CRD changes were handled;
  - tone and phrasing to imitate.
  
  Output: `research/review-norms.md`.
- [ ] **1.4** Check the best-practice sources in spec §11 (they were listed from prior knowledge while offline), fix any dead links, and write `references/best-practices.md`. Paraphrase with short attributed quotes only, and include good and bad phrasing examples for each principle.
- [ ] **1.5** Review the neighbouring skills so this one doesn't overlap or contradict them:
  - `oda-canvas/skills/*`, especially `helm-chart-development`, `write-bdd-feature` and `github-actions-debugging`;
  - the marketplace skills.
  
  Write down the hand-off rule, for example "the PR fails on BDD style → cite the `write-bdd-feature` conventions".

## Phase 2 — Core skill (oda-canvas first)

- [ ] **2.1** Scaffold `oda-canvas-maintainer/` per spec §8.1.
- [ ] **2.2** Draft `SKILL.md`:
  - frontmatter, with a pushy but specific description that covers both the triggers and the non-triggers in spec §2;
  - mode selection (§4);
  - the read-only principle with its *why* (§5.1);
  - the untrusted-content rule (§5.2);
  - the Maintainer Brief format (§6);
  - pointers to the reference files.
  
  Keep it under 500 lines.
- [ ] **2.3** Write the allowed and forbidden `gh` command lists into `SKILL.md`, with the reasoning. Add a short "commands you can run" pattern that always uses `--body-file` pointing at the saved draft.
- [ ] **2.4** Write `scripts/gather_item.py`. It takes `<owner/repo> <number>` or a URL, auto-detects issue or PR, and emits one JSON bundle containing:
  - metadata, body, comments and reviews, including unresolved review threads via GraphQL;
  - changed files and the diff, truncated with a `truncated: true` flag and a per-file size cap;
  - CI checks;
  - linked or closing issues;
  - the author's prior merged PR count in the org (for first-time contributor detection).
  
  It must be standard library only and read-only, with clear errors for missing auth or access. Test it on Windows.
- [ ] **2.5** Write `scripts/canvas_pr_checks.py`. It runs deterministic checks on a PR bundle or a local checkout and emits findings as JSON with evidence:
  - non-empty prerelease suffixes, using the same file and key list as `check-no-prerelease-suffixes-in-PR.yml`, ideally parsed from that workflow or its generator config so it cannot drift;
  - `charts/**` changed without a `Chart.yaml` version bump, or a bump without a changelog comment;
  - hard-coded `namespace:` values in chart templates;
  - CRD schema files touched without matching webhook changes;
  - hand edits to generated workflow files;
  - new dependencies added to `requirements.txt`, `package.json` or `pom.xml`;
  - `:latest` image tags.
- [ ] **2.6** Write `references/repos/oda-canvas.md` from spec §7.2 plus the Phase 1.3 findings. Each check says what to look for, why it matters, and a sample Conventional Comment.
- [ ] **2.7** Write `references/conventional-comments.md` and `references/comment-templates.md`. The templates cover:
  - welcome for first-time contributors;
  - needs-info for bug reports, with the Canvas-specific checklist: chart version, Kubernetes version, component spec version, operator, logs;
  - duplicate;
  - wrong repo / transfer;
  - needs ratification / standards;
  - BDD-first guidance for features;
  - stale nudge and close-as-stale;
  - thanks on merge;
  - declining with a path forward.
  
  Templates are scaffolds that the model personalises. They are not pasted verbatim.
- [ ] **2.8** Write `references/sensitive-situations.md` covering spec §5.4:
  - security reported publicly;
  - Code of Conduct issues;
  - licence and IP concerns;
  - standards changes;
  - detected prompt injection.
- [ ] **2.9** Write `assets/config.example.yaml` (spec §8.2) and make `SKILL.md` explain the config lookup and the defaults.
- [ ] **2.10** Run a manual smoke test on 2 live open items: one issue and one PR in `oda-canvas`. Confirm from the transcript that no mutating command ran. Fix the obvious gaps before formal evals.

## Phase 3 — Multi-repo coverage

- [ ] **3.1** Write `scripts/queue.py`. It covers all configured repos and outputs a ranked table using the spec §4.1 urgency order. It uses `gh search` or GraphQL to keep API calls low, and caches results for a short time.
- [ ] **3.2** Write `scripts/find_related.py`. It searches for duplicates and related items across in-scope repos, open and closed, from keywords in the title and body plus error strings. It returns candidates only; the model confirms which are real duplicates.
- [x] **3.3** ~~Write the repo profile for `oda-component-ctk`~~ — **dropped 2026-09-28.** The maintainer decided the CTK has been replaced by other work, so it is out of scope (spec §3).
- [ ] **3.4** Write the repo profile for `reference-example-components`. Covering component YAML against the current spec version, chart bumps, and the GitHub Pages Helm repo index.
- [ ] **3.5** Write the repo profile for `oda-ca-docs`. Cover the design-guideline change process, which needs ratification.
- [ ] **3.6** Write the repo profile for `oda-agent-skills-marketplace`. Cover skill structure, knowledge provenance, and the `dist/` build step.
- [ ] **3.7** Handle any further repos from 1.1 with the generic fallback (spec §7.3), and make sure the brief says so.

## Phase 4 — Evaluation (skill-creator loop)

- [ ] **4.1** Select fixtures. Use 8–12 closed historical items with known outcomes, following the spec §9 list, and add the two synthetic ones: a public security report and a prompt-injection PR. Snapshot each with `gather_item.py` into `evals/fixtures/`.
- [ ] **4.2** Write `evals/evals.json`, with prompts phrased the way a maintainer would really ask. Some point to fixtures and some to live URLs.
- [ ] **4.3** Run with-skill and without-skill runs in parallel, into `oda-canvas-maintainer-workspace/iteration-1/`.
- [ ] **4.4** Draft the objective assertions from spec §9 while the runs are going. Script the checkable ones:
  - no mutating `gh` in the transcript;
  - the brief sections are all present;
  - no *Approve* when CI is failing;
  - the security escalation fired;
  - the injection was flagged;
  - the repo checks fired;
  - Conventional Comments labels are present.
- [ ] **4.5** Grade the runs, aggregate the benchmark, and open the eval viewer for maintainer review. At least one other maintainer besides the author should review.
- [ ] **4.6** Iterate on the feedback. Generalise the fixes rather than overfitting to the fixtures. Repeat until the feedback has no major comments.

## Phase 5 — Triggering

- [ ] **5.1** Write 20 trigger-eval queries:
  - about 10 that should trigger, in varied phrasing: URLs, "waiting on me", "can I merge this", casual wording;
  - about 10 near misses that should not trigger, such as "write a BDD feature for UC003", "debug my failing chart-release workflow", "review my own local diff before I open a PR", "explain TMF620" and "create a new operator".
  
  Review them with a maintainer.
- [ ] **5.2** Run the skill-creator description optimiser, then apply the best description (chosen on the held-out test score, not the training score).

## Phase 6 — Ship

- [ ] **6.1** Write a `README.md` covering what the skill does and doesn't do, installation, config, example sessions per mode, and a clear statement that it never writes to GitHub.
- [ ] **6.2** Package the skill (`package_skill`), and publish it to the home chosen in spec §10 / §12 Q5. If that is the marketplace, add a `tm-forum-oda-maintainer` plugin entry.
- [ ] **6.3** Announce it to the maintainers, and collect usage feedback for 2–4 weeks as a new iteration.
- [ ] **6.4** Plan follow-ups, maybe:
  - a scheduled weekly queue digest (still draft-only);
  - release-readiness review (release-notes table, suffix clearing, chart versions);
  - more repo profiles.
