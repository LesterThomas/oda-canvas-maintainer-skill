---
name: comment-style
description: Voice, tone and structure for every draft the maintainer will post; includes inline comment labelling and best-practice principles.
last_updated: 2026-09-28
---

# Comment style

Drafts are posted under **Lester's name**, so they must sound like him. When in doubt, shorter and warmer is better.

## Voice

- **First person, direct and friendly.** Examples: "I'm happy to approve", "I've added some issues for…", "Thanks @name, good catch." Use "we" for the project ("we should look to apply this as a fix later").
- **@-mention the author** in the opening line of summary comments.
- **Brief.** A trusted, small or obviously good PR gets one or two sentences, or simply "Looks good to me". Don't pad.
- **British English** in prose ("behaviour", "organise"). Keep the terminology from `oda-canvas/docs/writing-style.md`: "ODA Canvas", "ODA Component", "Software Operators"; `code formatting` for CRDs, files and commands.
- **Don't restate decisions to the people who made them.** If the author already agreed something with the maintainers (for example on the linked issue), don't tell them it's been agreed. Just review against it. *Why:* it adds length and nothing new for the reader. (learned 2026-09-28 from oda-canvas#613)
- **No labels in the summary comment.** Conventional Comments labels are for inline comments only.

## Praise

Praise specifically: say *what* is good and *why it matters to the Canvas*. For example: "the first demonstration of a Carbon Management operator working in the Canvas", or "Kudos to @RJ-acc for such an impressive contribution". Generic praise such as "Great work!" adds nothing.

When approving a correctness fix, briefly explain *why* it is right (#608). This shows the maintainer understood the change, and it teaches the codebase to others.

## Structure of a PR summary comment

1. Thanks and specific praise, with an @-mention.
2. The verdict, in plain words: "I'm happy to approve", "A couple of things need fixing before we merge", or "Before reviewing further, I think this needs an ADR…".
3. Blocking points, if any. Keep them short; the detail goes in inline comments.
4. Non-blocking points being moved to follow-up issues ("I've raised #… for …"). Write this as though the issues exist, because the maintainer creates them before posting.
5. The next step, and who takes it.

## Inline comments (Conventional Comments)

- Format: `<label> [(blocking|non-blocking)]: <subject>`, then a short explanation of **why**.
- Labels: `issue`, `suggestion`, `question`, `nitpick`, `praise`, `todo`, `chore`, `thought`, `note`.
- Mark every `issue` or `suggestion` as blocking or non-blocking. Nits are never blocking.
- Point out the problem and let the author choose the fix, unless the fix is a one-liner that's quicker to show than describe.
- Critique the code, never the person. Write "this change" and "the operator", not "you broke".

## Declining or pushing back

- Depersonalise the "no": refer to the Canvas objectives, an ADR or documented scope, not personal preference.
- Always give a path forward: what would make it acceptable, or where the idea belongs (an ADR, another repo, an optional chart).
- Thank the contributor for the effort even when declining.

## Instructions to coding agents

When a PR comes from a coding agent (for example the Copilot SWE agent), draft instructions as `@copilot - <imperative steps>`, linking the relevant docs. An example is "follow the instructions in docs/developer/work-with-dockerimages.md to…" (#571). Use numbered steps and exact file paths, because agents follow instructions literally.

## Change log

- 2026-09-28 — added — don't restate agreed decisions to the author — Lester removed that sentence from the #613 draft, and confirmed it as a rule
- 2026-09-28 — added — seed from Lester's reviews (`research/review-norms.md` §1), `research/sources.md` and the `oda-canvas` writing style
