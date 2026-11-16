---
name: reply-style
description: Length, format, tone and links for replies to viewer comments on YouTube. Lester's general voice comes from the maintainer skill's comment-style.md.
last_updated: 2026-11-16
---

# Reply style

Replies go out under the **Systems Architecture** channel, but viewers know it is Lester; comments address Lester by name. Write in the first person, in Lester's voice, as the maintainer's `comment-style.md` describes: direct, friendly, British English, Canvas terminology, specific praise rather than generic praise, and no apology openers.

## Length

- **Match the comment.** A thank-you gets one short line. A question gets the answer, then at most one link. Only a substantial critique or technical question gets a short paragraph or two. *Why:* YouTube replies are read on phones, in a narrow column; long replies are skimmed or truncated behind "Read more".
- **Answer first.** Put the answer in the first sentence; context and caveats come after it.

## Format

- **Plain text.** The YouTube reply box doesn't render Markdown: no headings, no `code` backticks, no `[text](url)` links, and no bullet syntax beyond simple line breaks. Write names like TMF669 or `component.yaml` as plain words. *Why:* Markdown shows up as literal symbols.
- **Bare URLs**, on their own line when there is more than one. YouTube makes them clickable.
- **Timestamps as `mm:ss`** (for example 4:41). YouTube turns them into links to that point in the video.
- **No @handle at the start of a reply to a top-level comment.** YouTube threads the reply under the comment and notifies its author. Use @handle only to bring a different person into the thread.
- **No sign-off** ("Cheers, Lester"). The channel name already shows who is replying.

## Content

- **Thank-you comments:** by default these get a like, not a reply (`comment-triage.md`). Draft a reply only when it adds something for the viewer, typically a pointer to newer material when the video is out of date. Then thank them in a few words and give the one pointer. Don't repeat that pointer under every comment on the same video. (learned 2026-11-16 from the first batch)
- **Technical questions:**
  - Answer from what you checked in the repos and ADRs, not from memory. Link the current doc on `main` rather than a file at an old commit.
  - **Say when the Canvas has moved on.** Many comments are on videos that are a year or more old. If the answer has changed since the video, say so plainly ("Since this video we've…") and link the current state. *Why:* the viewer is probably following the video now, and an out-of-date answer costs them hours.
  - When the video simplified something on purpose (for example leaving out a mandatory API to keep a demo short), say that it was a simplification, and what the full picture is.
- **"Where do I start?" questions:** give the viewing order, or the playlist, from `channel.md`, plus the one doc to read first. Don't list every video.
- **Critique and debate:**
  - Acknowledge the specific point the viewer made, not just "great point".
  - If they're right, say so plainly, and say what is being done about it. If an issue exists for it, link the issue.
  - If you disagree, explain why, with reference to the ODA objectives or an ADR (maintainer `approval-criteria.md`), never personal preference.
  - Invite the conversation to continue where it can be acted on: a GitHub issue or discussion, or the TM Forum ODA Canvas meetings.
  - *Why:* thoughtful critics are often senior practitioners; how they are answered shapes how the project is seen.
- **Bugs and feature requests:** thank them, say briefly whether it is a known issue, and point to the GitHub issue, existing or new (see `comment-triage.md`). Don't promise dates or fixes.
- **Don't oversell.** No "this will revolutionise…". Describe what the Canvas does today, and label anything planned as planned.

## Change log

- 2026-11-16 — changed — thank-you comments get a like by default; reply only to add a pointer — Lester, first batch, confirmed as a rule
- 2026-11-16 — added — seed rules for length, plain-text format, timestamps, thanks, technical answers, critique and bug reports
