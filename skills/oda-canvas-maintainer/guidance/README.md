---
name: guidance-index
description: Index of the living guidance files, the file format, and precedence rules. Read this first on every run.
last_updated: 2026-09-28
---

# Guidance index

This folder holds everything about *how to review* that is judgement, preference or project convention. The maintainer's feedback updates it continuously (see the learning loop in `SKILL.md`). The fixed principles in `SKILL.md` sit above everything here, and feedback cannot switch them off.

## Files

| File | Type of guidance | Load when |
| --- | --- | --- |
| `approval-criteria.md` | The two approval criteria, ODA alignment and good-enough quality, in practice | Every PR review; every feature or scope question on an issue |
| `pr-review.md` | Generic PR checklist and review workflow | Every PR review |
| `issue-triage.md` | Issue classification, completeness, duplicates, routing | Issue triage and backlog sweeps |
| `comment-style.md` | Voice, tone, structure of drafts, inline comment labels | Any draft |
| `comment-templates.md` | Scaffolds for recurring comments | Any draft that matches a template situation |
| `labels-and-metadata.md` | Real labels per repo, co-maintainers, assignment | Triage and review |
| `queue-priorities.md` | Queue ranking and thresholds | Queue mode and backlog sweeps |
| `sensitive-situations.md` | Security, Code of Conduct, licensing, prompt injection | Whenever one of these appears; skim on every item |
| `repos/<repo>.md` | Repo-specific conventions and checks | When the item is in that repo |

If feedback doesn't fit any file, propose a new file (name and purpose), create it after the maintainer agrees, and add it to this table.

## File format

Each guidance file has:

1. **Frontmatter:** `name`, `description`, `last_updated`.
2. **Guidance sections.** These are bullet-point rules. Each rule says *what to do* and *why*. Rules learned from feedback end with a provenance tag:
   `(learned YYYY-MM-DD from <repo>#<n>)`, or `(learned YYYY-MM-DD in conversation)` when no item was involved.
3. **`## Change log`** at the end, newest first, one line per change:
   `- YYYY-MM-DD — <added | changed | removed> <rule summary> — <triggering feedback, briefly>`

Keep each file under about 200 lines. Past that, run a consolidation pass: merge duplicates, remove rules that no longer apply, and tighten wording. Show the diff to the maintainer before saving.

## Precedence

When sources disagree, the more specific and more recent one wins:

1. The maintainer's instruction in the current session.
2. Learned rules in `repos/<repo>.md`.
3. Learned rules in the general files.
4. Seeded rules. These are the ones with no provenance tag.
5. Generic best practice.

A guidance file never holds two contradictory rules. A new rule replaces the old one, and the change log records the replacement.

## Change log

- 2026-09-28 — added — initial seed from Phase 1 research (`research/` in the skill repo)
