---
name: sources
description: Verified best-practice sources behind the guidance (static; not changed by feedback).
---

# Best-practice sources (verified 2026-09-28)

Each source below was fetched and checked on 2026-09-28. Content is paraphrased; the only direct quotes are short and attributed. This file seeds `references/sources.md` in the skill, and the principles seed `guidance/comment-style.md` and `guidance/approval-criteria.md`.

| # | Source | URL | Status |
| --- | --- | --- | --- |
| 1 | Open Source Guides, *Best Practices for Maintainers* | <https://opensource.guide/best-practices/> | ✅ |
| 2 | Open Source Guides, *Building Welcoming Communities* | <https://opensource.guide/building-community/> | ✅ |
| 3 | Google Engineering Practices, *The Standard of Code Review* | <https://google.github.io/eng-practices/review/reviewer/standard.html> | ✅ |
| 4 | Google Engineering Practices, *How to Write Code Review Comments* | <https://google.github.io/eng-practices/review/reviewer/comments.html> | ✅ |
| 5 | Conventional Comments | <https://conventionalcomments.org/> | ✅ |
| 6 | Kubernetes, *Community Expectations* (reviewers) | <https://www.kubernetes.dev/docs/guide/expectations/> | ✅ URL corrected. The spec's `…/review-guidelines/` returned 404 |
| 7 | CHAOSS, *Time to First Response* metric | <https://chaoss.community/kb/metric-time-to-first-response/> | ✅ |
| 8 | OpenSSF Scorecard checks | <https://github.com/ossf/scorecard/blob/main/docs/checks.md> | ✅ |
| 9 | Contributor Covenant 2.1 | <https://www.contributor-covenant.org/version/2/1/code_of_conduct/> | ✅ |
| 10 | GitHub Docs, *Configuring private vulnerability reporting* | <https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository> | ✅ |

## Principles taken from the sources, and how they fit this project

- **Approve on improvement, not perfection** [3]. Approve when a change clearly improves overall code health, even if it isn't perfect. Mark polish as `Nit:`/optional. *This matches Lester's approve-plus-follow-up-issues habit exactly.*
- **Explain why; critique the code, not the person; praise good work** [4]. Let the author solve the problem where possible instead of dictating the fix. Label severity (Nit / Optional / FYI).
- **Explicit severity labels** [5]. The Conventional Comments format is `<label> [decorations]: <subject>`.
  - Labels: `praise`, `nitpick`, `suggestion`, `issue`, `todo`, `question`, `thought`, `chore`, `note`, `typo`, `polish`, `quibble`.
  - Decorations: `(blocking)`, `(non-blocking)`, `(if-minor)`.
  - *Used for inline comments* (see `review-norms.md` §1).
- **Respond fast, especially to newcomers** [2, 7].
  - Contributors who get a review within about 48 hours are much more likely to return [2].
  - Time to first response is the CHAOSS health signal for responsiveness [7].
  - *This directly motivates the queue ordering, given the 580-day median issue age (`review-norms.md` §3).*
- **Depersonalise "no"** [1]. Decline by referring to documented scope and criteria, not personal preference. Thank the contributor and link the relevant docs. "No is temporary, yes is forever" (Open Source Guides, quoting a maintainer).
  - *The two approval criteria are that documentation. Declines cite them.*
- **Write down the scope and vision** [1]. It lets contributors self-check and keeps refusals impersonal.
  - *This supports a later suggestion: publish the approval criteria in `CONTRIBUTING.md`.*
- **Use templates, labels and `good first issue`; automate the objective checks** [1, 2].
  - *The label and template mismatch in `governance.md` is worth fixing.*
- **Reviewers are the first contact with the project** [6]. Respond with reasonable latency, and say so when unavailable, so work can be re-routed.
  - *This matches the co-maintainer awareness in the queue.*
- **Address bad behaviour promptly** [2]. Code of Conduct enforcement is graded as correction, then warning, then temporary ban, then permanent ban, and handled privately by community leaders [9].
  - *The skill flags these cases and drafts nothing public.*
- **Security reports go through a private channel** [10]. Private vulnerability reporting adds a "Report a vulnerability" button, and admins enable it. *It is disabled on `oda-canvas`, so the channel is `components@tmforum.org`.*
- **Human review before merge; protected branches; least-privilege workflow tokens; pinned dependencies** [8]. These are useful review checks on workflow and CI changes: unpinned Actions, broad `permissions:`, `pull_request_target` misuse.
  - *There is no branch protection on `oda-canvas` today. That is Lester's decision, not the skill's.*
