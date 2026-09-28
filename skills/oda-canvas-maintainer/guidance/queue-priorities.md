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

## Ranking (highest first)

1. **Security-sensitive** items, whatever their age.
2. **External PRs with no maintainer review**, oldest first. One approval merges a PR, so a single review from Lester unblocks a contributor. *Why:* contributors reviewed within about 48 h are far more likely to return, and some external PRs have waited since February 2025.
3. **External issues with no maintainer reply**, oldest first.
4. **PRs where the author has responded** since the last maintainer review. The author is waiting on us.
5. **Co-maintainer PRs with no review**. These rank lower, because maintainers routinely self-merge.
6. **Stale items** that need a keep, refresh or close decision. These go to a backlog sweep rather than the daily queue.

**Handled by someone else.** An item a co-maintainer is actively handling (a review or comment within the stale threshold) drops below unclaimed items. Mark it "handled by @<login>".

**Drafts.** Draft PRs rank at the bottom unless the author has explicitly asked for feedback.

## Queue output

Show one table, in this order: item link, age, type, author (external or maintainer), state, why it's here, suggested next step. Show at most about 15 rows, and offer "show more". No deep review happens in queue mode. The maintainer picks items to open.

## Backlog sweep

- Work in batches of about 10 issues, with unanswered external issues first.
- For each issue, give a classification and a draft (see `issue-triage.md`).
- End with a batch table so the maintainer can act on all ten quickly.

## Change log

- 2026-09-28 — added — seed from spec §4.1 and `research/review-norms.md` §3
