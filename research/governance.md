# Governance facts (task 1.2)

Collected live on 2026-09-28 with read-only `gh` calls, logged in as `LesterThomas`, who has `maintain` permission on `oda-canvas` but not admin.

## oda-canvas

### Maintainers

The `oda-canvas` repository has 36 collaborators with push access:
- 10 with `maintain`: thomo, OmidTahouri, LesterThomas, ferenc-hechler, ajayaggarwal03, g-greatdevaks, adarshkumar4, Suyash7774, RJ-acc;
- 6 with `admin`, all TM Forum staff and IT accounts;
- the rest with `write`.

Who actually approves and merges is a much smaller group. Approving reviews and merges across the last 100 merged PRs:

| Login | Approvals | Merges | Notes |
| --- | ---: | ---: | --- |
| brian-burton | 29 | 35 | `write` role, but the most active reviewer |
| LesterThomas | 23 | 33 | the maintainer using this skill |
| ferenc-hechler | 13 | 23 | the most detailed inline reviewer |
| adarshkumar4 | 10 | 2 | |
| anshulkumar-tmf | 4 | 4 | `admin` |
| RJ-acc, thomo | 1 each | | occasional |

**Proposed `co_maintainers`:** `brian-burton`, `ferenc-hechler`, `adarshkumar4`, `anshulkumar-tmf`. This matches the "about 5 maintainers" figure. *To be confirmed by Lester.*

### Approval in practice

- **One approval is a convention, not an enforced rule.** No branch protection is visible on `main` (the API returns 404 at `maintain` level) and there are no rulesets.
- Of the last 100 merged PRs:
  - 26 were merged with **no approving review**;
  - 48 were **merged by their own author**, typically maintainers merging their own work.
- The skill should not moralise about this. It is a small team and self-merge is normal for maintainers. For **external** PRs, however, one maintainer approval is the bar.

### Labels

There are 13 labels:

- `bug-fix`
- `documentation`
- `duplicate`
- `feature`
- `help wanted`
- `invalid`
- `question`
- `refactor`
- `wontfix`
- `testing`
- `good first issue`
- `Innovation Hub onboarding`
- `Priority for Launch`

**Mismatch with the issue templates.** The templates apply `bug` (Bug report), `docs`, `chore` and `style`, but **none of these labels exist**. Only `feature`, `bug-fix` and `refactor` match. So:
- issues filed from those templates arrive unlabelled or wrongly labelled;
- the skill should map to real labels (`bug`→`bug-fix`, `docs`→`documentation`);
- the skill could also suggest to Lester, once, that the templates or labels be fixed.

### Milestones and projects

- There are 3 milestones (Sprint 2–4, from 2023), all effectively dead. **Milestones are not used.** The skill should not suggest them.
- Projects are enabled, and Discussions are **disabled**.

### Security

- **Private vulnerability reporting is disabled** (`enabled: false`). This answers spec Q6: the only private channel is `components@tmforum.org` (from `CONTRIBUTING.md`).
- The skill could suggest enabling private vulnerability reporting, but that needs an admin.
- There is no `SECURITY.md`.

### Community files

- Present: README, CONTRIBUTING, code of conduct, Apache-2.0 licence.
- The issue templates exist, but GitHub's community profile reports `issue_template: none` because they are `.md` templates with a `config.yaml`, not issue forms.
- There is **no PR template**.
- There is **no CODEOWNERS** file.

### CI checks on every PR

These checks ran on 11 of the last 15 PRs:

- `run_tests_job` — the BDD suite on a cluster. It is long-running, and it can be skipped with `[skip tests]` in the PR title (see `check_skip_tests_job`, and open PR #607);
- `lint-python-code`;
- `check-pr-does-not-contain-prereleasesuffixes-job`;
- `check_skip_tests_job`;
- `build_badges_job`.

Chart release and prerelease Docker builds run conditionally.

**Copilot code review is active.** `copilot-pull-request-reviewer` posted 48 of the last 100 inline comments. Maintainers refer to it directly, for example Lester's "Copilot has a few minor comments…" on #602. The skill should **read Copilot's comments, not duplicate them**, and say which ones it agrees are worth acting on.

## Tier 1 and Tier 2 satellite repos

The satellite repos are `reference-example-components`, `oda-helm-charts`, `canvas-prerequisites`, `TMFOP006-Event-Management`, `TMFCOP009-model-as-a-service-operator` and `TMFOP012-data-products-lifecycle-management-operator`. They share the same picture:

- README only (the operator repos also have a LICENSE);
- no CONTRIBUTING, CODEOWNERS or PR template;
- no branch protection;
- private vulnerability reporting disabled where it could be read;
- **GitHub's default label set**: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. So these repos use `bug` and `enhancement`, not `bug-fix` and `feature`. `reference-example-components` also has `feature` and `Required for Launch`;
- **no CI workflows**, except `reference-example-components`, which has `release.yml`.

**Implications for the skill:**
- `oda-canvas` conventions should be treated as the reference for these repos, applied through each repo's guidance file.
- Label names differ per repo, so `labels-and-metadata.md` needs a per-repo map.
- Without CI, the skill's "Not verified" section matters more. Nothing has been checked automatically on these PRs.
