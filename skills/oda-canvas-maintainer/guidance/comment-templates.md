---
name: comment-templates
description: Scaffolds for recurring maintainer comments. Personalise every one — never paste verbatim.
last_updated: 2026-09-28
---

# Comment templates

These are **scaffolds**. Always personalise them:
- name the person;
- reference the specific item;
- cut anything that doesn't apply.

The voice rules are in `comment-style.md`. `<…>` marks something to fill in.

## Approve with follow-ups

> Thanks @<author>, <specific praise: what it adds and why it matters to the ODA Canvas>. I'm happy to approve.
>
> I've raised some issues for things that don't need to be part of this PR:
> - #<n> <follow-up 1>
> - #<n> <follow-up 2>

## Request changes

> Thanks @<author>, <what's good about it>. There are <a couple of / a few> things to fix before we merge. I've left inline comments on each:
> - <blocking point 1, one line>
> - <blocking point 2, one line>
>
> <Optional: non-blocking points will go into follow-up issues.>

## Needs an ADR

> Thanks @<author>, this is an interesting direction. Because it changes <what: the Component spec / Canvas architecture>, it needs an Architecture Decision Record so the change is agreed and recorded. Could you propose one in [oda-ca-docs/Decision-Log](https://github.com/tmforum-oda/oda-ca-docs/tree/master/Decision-Log) (see ADR-0001 for the format)? We can keep this PR open alongside it.

## Welcome (first-time contributor)

> Welcome, and thanks for your first contribution to the ODA Canvas, @<author>! <One specific, positive observation.> <Next step: review verdict, or what happens next.>

## Needs info (bug)

> Thanks for reporting this, @<author>. To reproduce it, could you add:
> - <only the missing items from `issue-triage.md`, each with a short reason>

## Duplicate

> Thanks @<author>. This looks like the same problem as #<n>, so I'll close this one to keep the discussion in one place. Please add any extra details there.

## Fixed by a merged PR

> Fixed in #<n>, thanks @<reporter>!

## Stale: still needed?

> Sorry this has sat for so long, @<author>. Is this still an issue with the current Canvas release (<version>)? If we don't hear back in the next few weeks we'll close it, but it can always be reopened.

## Close as stale / superseded

> Closing, as <this was superseded by #<n> / the Canvas has changed significantly since (<how>)>. Please reopen, or raise a new issue, if it's still relevant.

## Wrong repo

> Thanks @<author>. This belongs in [<repo>](<url>), which covers <scope>. Could you raise it there? <Or: I'll move it.>

## Thanks on merge

> Merged, thanks @<author>! <Optional: when it will be released or where it shows up.>

## Security report posted publicly

See `sensitive-situations.md`. Use only that wording.

## Change log

- 2026-09-28 — added — seed templates in Lester's style
