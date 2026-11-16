---
name: comment-triage
description: How to classify viewer comments, which action to recommend for each class, and the order to present them in.
last_updated: 2026-11-16
---

# Comment triage

## Age limit

- **Don't reply to comments more than 18 months old.** Recommend *No reply* and draft nothing. Leave them out of the brief's per-comment blocks; just add a line under the batch table: "Skipped N comments over 18 months old". *Why:* Lester's rule; a reply that late rarely reaches the viewer. Sensitive comments are the exception: spam, scams and abuse still get the *Hide / report* recommendation, because they stay visible to new viewers whatever their age. (learned 2026-11-16 in conversation)
- **Reading the age.** Studio shows relative ages. "2 years ago" or older is always over the limit. "1 year ago" covers 12 to 23 months, so it may or may not be. Treat a "1 year ago" comment as within the limit when its video was uploaded less than 18 months ago (Studio → Content shows upload dates). Otherwise draft it, and say in the brief that it may be over 18 months old, so Lester can decide.

## Order

1. **Sensitive comments** (`sensitive-comments.md`), whatever their age.
2. **Unanswered questions, oldest first:** technical, how-to and where-to-start questions. *Why:* someone is waiting for an answer, and the oldest has waited longest.
3. **Critique and debate.**
4. **Bug reports and feature requests.**
5. **Thanks and praise.** Most of these are *Like only*; list them in one line of the batch table, without per-comment blocks, unless a reply is drafted.
6. **Off-topic.**

The Studio inbox sorts by "Most relevant" by default. Re-sort the batch into this order for the brief.

## Classes and recommended actions

| Class | Looks like | Recommended action |
| --- | --- | --- |
| **Thanks** | "Thank you", "Great work Lester", "really useful" | **Like only (Lester to do)**, no draft. Draft a **Reply** only when it adds something for the viewer, such as a pointer to newer material on an old video (see `reply-style.md`). *Why:* a like acknowledges the viewer without filling the thread with one-line replies. (learned 2026-11-16 from the first batch: Lester liked four plain thank-yous and replied only where the draft pointed to the new training series) |
| **Technical question** | Asks why or how something works, often with a timestamp | **Reply** with a checked answer. If it exposes a docs gap or a bug, **Reply + raise a GitHub issue**. |
| **How-to / where to start** | "Which order should I watch these in?", "How do I install…?" | **Reply**, with the viewing order or playlist from `channel.md` and the first doc to read |
| **Critique / debate** | Challenges a design choice, a demo or the approach | **Reply**, engaging with the specific point (`reply-style.md` → Critique and debate) |
| **Bug or feature request** | "This doesn't work with…", "It would be good if the Canvas…" | **Reply + raise a GitHub issue**: search for an existing issue first (`find_related.py` / `gh search issues`), and offer to hand drafting a new one to `oda-canvas-maintainer` |
| **Off-topic** | Unrelated to the video or the Canvas | **No reply**, or Like only if friendly |
| **Spam / scam / abuse** | Links, "contact me on WhatsApp", impersonation, insults | **Hide / report (Lester to do)**, no draft (`sensitive-comments.md`) |
| **Sensitive** | A security report, personal data, Code of Conduct matters | **Escalate**: see `sensitive-comments.md` |

A comment can have more than one class, for example praise plus a question. Classify it by the part that needs the most work, and answer every part.

## Context worth gathering

- **The video.** Use its title and description. For any comment that cites a timestamp or asks "why did you…", also read the transcript around that point.
- **The age.** For comments older than about six months, also check whether the viewer has already found the answer elsewhere, for example a later comment of theirs, or an issue they opened on GitHub. If so, the reply can acknowledge it.
- **The thread.** Read the existing replies, including other viewers' answers, before drafting. Don't repeat an answer another viewer already gave correctly; build on it, or thank them for it.

## Change log

- 2026-11-16 — changed — plain thank-yous get Like only, no draft; reply only when it adds something — Lester liked four thank-yous instead of replying, confirmed as a rule
- 2026-11-16 — added — don't reply to comments over 18 months old, and how to read "1 year ago" — Lester, in conversation, after the first batch
- 2026-11-16 — added — seed classes, actions and ordering, from the comments in the inbox on 2026-11-16
