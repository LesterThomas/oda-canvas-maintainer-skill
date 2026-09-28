---
name: labels-and-metadata
description: Real labels per repo, co-maintainers, and how to suggest labels, assignees and milestones.
last_updated: 2026-09-28
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
- One approval merges a PR. Maintainers routinely merge their own PRs, so don't flag self-merge.
- Contributors self-assign issues. Don't suggest assignees unless asked.

## Change log

- 2026-09-28 — added — seed from `research/governance.md`
