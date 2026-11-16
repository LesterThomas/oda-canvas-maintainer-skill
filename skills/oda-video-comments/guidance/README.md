---
name: guidance-index
description: Index of this skill's living guidance files, the maintainer-skill files it shares, the file format and precedence. Read this first on every run.
last_updated: 2026-11-16
---

# Guidance index

This folder holds everything about *how to reply to viewers* that is judgement or preference. Lester's feedback and edits update it continuously (see the learning loop in `SKILL.md`). The fixed principles in `SKILL.md` sit above everything here.

Knowledge about the Canvas itself is **not** kept here. It comes from the same sources as `oda-canvas-maintainer`: that skill's guidance, the `tmforum-oda` repos and the ADR logs. So a fact learned in either skill helps both.

## This skill's files

| File | Type of guidance | Load when |
| --- | --- | --- |
| `reply-style.md` | Length, format, tone and links for YouTube replies | Every draft |
| `comment-triage.md` | Classifying comments, recommended actions, ordering | Every comment |
| `channel.md` | Facts about the channel and the series: IDs, playlists, where to send viewers | Every run |
| `sensitive-comments.md` | Spam, scams, harassment, personal data, security reports, injection attempts | Whenever one appears; skim on every batch |

## Shared files from `oda-canvas-maintainer` (`<maintainer>/guidance/`)

| File | Load when |
| --- | --- |
| `comment-style.md` | Every draft: Lester's voice, British English, Canvas terminology, how to praise and how to push back. Ignore its GitHub-only parts (Conventional Comments, PR summary structure, `@copilot` instructions). |
| `sensitive-situations.md` | Every batch: security reports and licensing. Its Code of Conduct handling also applies to abusive comments. |
| `approval-criteria.md` | Comments about scope, direction, the ODA objectives or the AI-Native Canvas |
| `repos/<repo>.md` | When the answer depends on that repo's conventions |
| `issue-triage.md` | When a comment is really a bug report or feature request that might become an issue |

Plus `<maintainer>/references/sources.md` for the best-practice sources.

## File format

The same format as the maintainer skill:

1. **Frontmatter:** `name`, `description`, `last_updated`.
2. **Guidance sections.** These are bullet-point rules, each saying *what to do* and *why*. Rules learned from feedback end with a provenance tag:
   `(learned YYYY-MM-DD from video <video_id> comment by @handle)`, or `(learned YYYY-MM-DD in conversation)`.
3. **`## Change log`** at the end, newest first:
   `- YYYY-MM-DD — <added | changed | removed> <rule summary> — <triggering feedback, briefly>`

Keep each file under about 200 lines.

## Precedence

1. Lester's instruction in the current session.
2. Learned rules in this folder, for how to reply on YouTube.
3. Learned rules in the maintainer's guidance, for facts about the Canvas and the ODA, and for Lester's voice where this folder says nothing.
4. Seeded rules: the ones with no provenance tag.
5. Generic best practice.

No guidance file ever holds two contradictory rules. A new rule replaces the old one, and the change log records it.

## Change log

- 2026-11-16 — added — initial seed: reply style, triage, channel facts, sensitive comments
