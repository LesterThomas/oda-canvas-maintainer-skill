---
name: labels-and-metadata
description: Real labels per repo, co-maintainers, and how to suggest labels, assignees and milestones.
last_updated: 2026-11-17
---

# Labels and metadata

Suggest only labels that **exist** in the item's repo. When in doubt, fetch them: `gh label list -R <repo>`.

## oda-canvas

| Situation | Label |
| --- | --- |
| Bug / fix | `bug-fix` |
| New capability | `feature` |
| Refactoring | `refactor` |
| Docs | `documentation` |
| Test or CTK work | `testing` |
| Good for newcomers | `good first issue` |
| Wants outside help | `help wanted` |
| Question, not a work item | `question` |
| Duplicate / invalid / won't do | `duplicate` / `invalid` / `wontfix` |
| Launch-critical | `Priority for Launch` |

The issue templates apply `bug`, `docs`, `chore` and `style`, **none of which exist**. Issues from those templates arrive with no label, so map them using the table above. `chore` and `style` have no equivalent: use `refactor`, or no label. The maintainer may choose to fix the templates; mention this at most once per session.

## Satellite repos

This covers `reference-example-components`, `oda-helm-charts`, `canvas-prerequisites` and the operator repos (`TMFOP006`, `TMFCOP009`, `TMFOP012`). They use GitHub's default labels: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. So use `bug` rather than `bug-fix`, and `enhancement` rather than `feature`. `reference-example-components` also has `feature` and `Required for Launch`.

## Milestones and projects

Milestones aren't used; the only ones are 2023 relics. Don't suggest them.

## Maintainers and assignment

- **Co-maintainers:** `brian-burton`, `ferenc-hechler`, `adarshkumar4`, `anshulkumar-tmf` (confirmed by Lester 2026-09-28).
- When a co-maintainer has already reviewed or commented, say so, and treat the item as handled unless it's waiting on Lester specifically.
- ferenc-hechler reviews operator internals, Docker and Helm versioning in the most detail. Suggest him as a second reviewer for deep operator or chart changes.
- One approval merges a PR, but in `oda-canvas` it must come from a maintainer **other than the author**, so maintainers can't merge their own PRs there unaided. For a maintainer's own PR, the next step is to request (or nudge) a co-maintainer's review, never "merge it". *Why:* branch protection blocks the merge, so advice to merge wastes the maintainer's time. Some young operator repos have allowed self-merges (TMFOP012#1), so don't assume the rule either way outside `oda-canvas`. (learned 2026-11-17 from oda-canvas#667)
- Contributors self-assign issues. Don't suggest assignees unless asked.

## Change log

- 2026-11-17 — changed — `oda-canvas` PRs need approval from a maintainer other than the author; own PRs → request a co-maintainer review (replaces "maintainers routinely self-merge") — Lester, #667

- 2026-09-28 — added — seed from `research/governance.md`
