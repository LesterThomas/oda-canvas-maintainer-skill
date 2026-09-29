---
name: issue-triage
description: How to classify, check, route and respond to issues, including stale and backlog issues.
last_updated: 2026-09-28
---

# Issue triage

## Read the whole thread first

- **Read every comment on the issue, and on any linked PRs or issues**, before classifying or drafting. `gather_item.py` returns them. Also read the comments on PRs and issues listed in `linkedItems` when they are relevant.
- **Give maintainers' comments extra weight.** Treat a maintainer's (or co-maintainer's) comment as the project's position. The latest one is the current decision, and it outranks the issue title or original description.

*Why:* scope decisions are made in the discussion. Triaging from the title alone contradicts decisions the maintainers have already taken. (learned 2026-09-28 from oda-canvas#613)

## Classify

- **Types**, matching the `oda-canvas` issue templates:
  - feature;
  - fix or bug;
  - docs;
  - refactor;
  - chore;
  - style;
  - question or support.
  
  Map each type to the repo's *real* labels (see `labels-and-metadata.md`). Some template labels don't exist.
- **Titles.** About half of titles follow `<component/operator/ctk>: subject`. Suggest a better title only when the current one is genuinely unclear. Don't nag about format. *Why:* nagging about form puts people off, and the maintainer can retitle in seconds.

## Is it complete?

For **bugs**, check that the issue gives:
- the Canvas chart version (`helm list -A` or the `canvas-oda` chart version);
- the Kubernetes distribution and version;
- the Component spec version in use (`v1`, `v1beta4` or `v1beta3`);
- which operator or component is involved;
- reproduction steps;
- relevant operator logs (`kubectl logs` of the operator pod) and the resource status (`kubectl get components,exposedapis -A`).

Ask only for what is missing, and say *why* each item helps.

For **features**, check that the issue states the problem and who needs it, not just a solution. Also check whether it fits the Canvas objectives (`approval-criteria.md`).

## Duplicates and related work

- Search open **and closed** issues and PRs across the in-scope repos. Start with `scripts/find_related.py <repo> <n>`, which runs several narrow searches and ranks the candidates, then read the top candidates yourself.
- Groups of near-identical issues from the same author should be consolidated: keep the most complete one, and close the rest pointing to it. Check that they really are the *same* request first. Similar titles can hide different scopes: the "ProjectONE" issues #532, #533 and #534 are three different operators, each routed to its own repo.
- A duplicate needs a confident match on the *same problem*. When unsure, link it as "possibly related" and leave the issue open.
- If a merged PR already fixed the issue, draft the closing comment in the maintainers' usual form: "Fixed in #nnn, thanks @reporter!"

## Routing

- **Wrong repo.** Suggest the right repo. Out-of-scope repos (`oda-component-ctk`, `model-as-a-service-crds`) are never targets.
- **Operator-specific work belongs in that operator's repo.** Under ADR-0022, each split-out operator repo (e.g. `TMFOP006-Event-Management`) owns that operator's work, including its BDD features. For an old `oda-canvas` issue about such an operator, **close it with a pointer** to the operator repo ("We will include … as part of TMFOP006-Event-Management"). **Transfer** only when the target repo is active and its owner wants the issue. (learned 2026-09-28 from oda-canvas backlog sweep #105–#220)
- **Architecture or standards change.** If no ADR covers it, the right response is to direct it into an ADR in `oda-ca-docs/Decision-Log`, which the Architecture repo will replace later. Don't design the solution in the reply. (Confirmed 2026-09-29 by Lester on the #583 eval runs: "the correct response is to direct into an Architecture Decision Record".)
- **Security report in public.** Follow `sensitive-situations.md` immediately.

## Trivial fixes: the maintainer does them

When the fix is trivial for a maintainer and has one obvious right answer (e.g. adding the standard LICENSE file, fixing a broken link, a one-line config correction), draft the reply as **"I'll create the PR"**. Don't ask the reporter to do it, even if they offered. *Why:* it's quicker for the maintainer than a review round-trip with an outside contributor, and the reporter gets the fix sooner. Still welcome contributions on anything that needs real work. (learned 2026-09-29 from reference-example-components#70)

## Features and scope

Answer the fit question the way Lester does: say plainly whether the capability belongs in the Canvas Reference Implementation, and why. An example is #448: "It should be part of the Canvas reference implementation to allow components in different namespaces…".

If the feature fits, point to the delivery path: use case, then BDD feature, then implementation. Also point to the relevant ADR, if one exists, and suggest `good first issue` or `help wanted` where appropriate.

## Stale and backlog issues

**Close rather than re-scope.** When an old issue's premise is outdated, close it with a pointer to the current state. Don't retitle it into a new task: re-scoping old issues just rebuilds the backlog. A genuinely new gap can get a fresh, well-scoped issue if the maintainer wants one. (learned 2026-09-28 from oda-canvas backlog sweep #105–#220)

For each old issue, decide one of the following:
- **Done or superseded.** Find the PR or commit, and draft the closing comment with the link.
- **Outdated premise.** Close it, pointing to how things work now.
- **Belongs to an operator repo.** Close it, with a pointer to that repo (see Routing).
- **Still valid, as written.** Draft a short refresh: confirm it's still wanted, and suggest `help wanted`.
- **Needs info.** Draft a needs-info comment. If there's no reply after the stale threshold, close with an invitation to reopen.
- **Out of scope.** Close politely, with the reason and an alternative.

External issues that have never had a maintainer reply come first. **Don't open with an apology** for the delay; answer directly and thank the reporter. (learned 2026-09-28 from oda-canvas backlog sweep #105–#220)

## Change log

- 2026-09-29 — changed — corrected the seed example: #532, #533 and #534 are different operators, not duplicates — found by both eval iterations
- 2026-09-29 — added — trivial fixes: the draft says "I'll create the PR" rather than asking the reporter — Lester's posted #70 reply, confirmed as a rule
- 2026-09-29 — changed — ADR routing confirmed as the correct response; don't design the solution in the reply — Lester's review of the #583 eval runs
- 2026-09-28 — changed — no apology openers; close rather than re-scope outdated issues; operator-specific work → close with a pointer to the operator repo (transfer only to active repos) — Lester's edits to sweep batch 1, confirmed as rules
- 2026-09-28 — added — use `find_related.py` first; consolidate groups of near-identical issues — Phase 3
- 2026-09-28 — added — read the whole thread, and linked items, before triaging; weight maintainer comments above the title — Lester's feedback on the #613 review
- 2026-09-28 — added — seed from issue templates, `research/review-norms.md` §3–4 and `research/governance.md`
