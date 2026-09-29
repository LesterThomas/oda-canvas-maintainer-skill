---
name: queue-priorities
description: How to rank the "what needs my attention" queue and backlog sweeps, and the thresholds used.
last_updated: 2026-09-28
---

# Queue priorities

## Thresholds

- **No response:** an external item with no maintainer reply after **7 days**.
- **Stale:** no activity for **60 days**.

The data supports these defaults: the median time to first response on PRs is 23 h, but the 75th percentile is about 7 days.

**External** means not one of `maintainer_login` or `co_maintainers`. That includes TM Forum staff and other accounts with repo permissions but no maintainer role, such as `RJ-acc` and `hvaughanattmforum`. Their items still deserve a reply, but mention in the brief when an "external" author is actually TM Forum staff, because the tone may differ.

**Security flag.** `queue.py` escalates only vulnerability-disclosure and dependency-alert language ("vulnerability", CVE ids, "exploit", leaked or exposed secrets, "critical bugs", Dependabot) in items under 90 days old. Authentication and authorisation are everyday Canvas design topics, not security reports.

## Ranking (highest first)

0. **Broken on the default branch:** workflows whose latest run on `main`/`master` failed. These go above the table, because they block releases for everyone. For example, reference-example-components' Release Charts failed from 26 Sep 2026, so TMFC007 was never published.
1. **Possible vulnerability reports** from the last 90 days. Older mentions are noted in the row, not escalated, because a years-old public report needs a sweep decision, not an urgent private-channel reply.
2. **Asks you directly:** your review is requested and you haven't reviewed, or you were @-mentioned after your last comment. *Why:* someone is explicitly waiting on you, and these are easy to miss in a large backlog (#545 waited 363 days).
3. **External PRs with no maintainer review**, oldest first. One approval merges a PR, so a single review from Lester unblocks a contributor. *Why:* contributors reviewed within about 48 h are far more likely to return, and some external PRs have waited since February 2025.
4. **External issues with no maintainer reply**, oldest first.
5. **PRs where the author has responded** since the last maintainer review. The author is waiting on us.
6. **Co-maintainer PRs with no review**. These rank lower, because maintainers routinely self-merge.
7. **Stale items** that need a keep, refresh or close decision. These go to a backlog sweep rather than the daily queue.

**Handled by someone else.** An item a co-maintainer is actively handling (a review or comment within the stale threshold) drops below unclaimed items. Mark it "handled by @<login>".

**Drafts.** Draft PRs rank at the bottom unless the author has explicitly asked for feedback.

## Queue output

Show one table, in this order: item link, age, type, author (external or maintainer), state, why it's here, suggested next step. Show at most about 15 rows, and offer "show more". No deep review happens in queue mode. The maintainer picks items to open.

## Backlog sweep

- Work in batches of about 10 issues, with unanswered external issues first.
- For each issue, give a classification and a draft (see `issue-triage.md`).
- End with a batch table so the maintainer can act on all ten quickly.

## Change log

- 2026-09-29 — added — broken-on-default-branch section, "asks you directly" rank (review requested or unanswered @-mention), dependency-alert wording — gaps found in the Phase 4 eval baseline
- 2026-09-28 — added — definition of external; security flag narrowed to disclosure language — Phase 3 testing of `queue.py`
- 2026-09-28 — added — seed from spec §4.1 and `research/review-norms.md` §3
