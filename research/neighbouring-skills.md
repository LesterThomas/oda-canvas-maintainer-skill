# Neighbouring skills and marketplace fit (task 1.6)

## Skills in oda-canvas/skills/

| Skill | Relationship to the maintainer skill |
| --- | --- |
| `helm-chart-development` | **Source of truth** for chart conventions: umbrella chart, prerelease suffixes, `Chart.yaml` changelog comments, `_helpers.tpl`, RBAC. The maintainer skill *cites* it in review comments ("see the helm-chart-development conventions") rather than copying them, so there is one source to keep current |
| `write-bdd-feature` | Source of truth for BDD conventions: file naming `UCxxx-Fyyy-*.feature`, the standard header comment, `@UCxxx` tags, implementation-agnostic steps |
| `create-oda-operator` | Source of truth for the operator folder layout. Lester updated it during #596 so new operators follow the `Dockerfile` naming and folder pattern |
| `canvas-usecase-documentation` | Documentation and use-case templates, and the writing style |
| `github-actions-debugging` | Explains the CI pipeline. The maintainer skill hands off to it when a PR's CI failure needs debugging and not just a verdict |
| `canvas-ops-tutorial` | No overlap |
| `skill-creator` | No overlap (tooling) |

**Hand-off rule for `SKILL.md`:**
- The maintainer skill *reviews against* these conventions and links to them.
- It doesn't generate code, charts, BDD features or docs itself.
- If Lester asks it to *fix* something in a PR, that is out of scope. The fix is drafted as a comment to the author, or as an instruction to the Copilot agent (see `review-norms.md` §1.8).

**Freshness:** when reviewing, read these conventions from the *target repo's current `main`*, not from a stale local clone. Lester's `oda-canvas` clone was 5 commits behind `origin/main` on 2026-09-28. This favours fetching with `gh api` over reading local files.

## Marketplace fit (for spec §10, the creator skill later)

`oda-agent-skills-marketplace` (local clone is up to date):
- Canonical skills live at `skills/<name>/`.
- `tools/build_plugin.py` packages them into `dist/consumer/` and `dist/creator/`. Every skill must be listed in exactly one of `CONSUMER_SKILLS`, `CREATOR_SKILLS`, `SHARED_SKILLS` or `INTERNAL_ONLY_SKILLS`.
- The build rewrites the skill's own `skills/<name>/…` paths, and `knowledge/…` paths, to `${CLAUDE_PLUGIN_ROOT}/…` in the packaged copies.
- The creator plugin is `tm-forum-oda-creator` v1.1.0 (author: Lester Thomas). Its current creator skills are all about *drafting and extending ODA standards*: use cases, component and API extensions, matrix corrections, use-case linting.

**Decisions this implies for this repo, recorded now to avoid a restructure later:**

1. **Put the skill at `skills/oda-canvas-maintainer/`** in this repo, not at the top level, so it drops straight into the marketplace's `skills/`. The spec §8.1 layout is updated to match.
2. **Refer to bundled files as `skills/oda-canvas-maintainer/…`** in `SKILL.md`, the same convention as the marketplace. `build_plugin.py` then rewrites them correctly. For personal use, the skill resolves them against its own base directory, which Claude Code reports when the skill loads.
3. **`guidance/` must be writable, but plugin installs are not.** This confirms the overlay design in spec §7.4. When packaged:
   - the bundled `guidance/` becomes the seed;
   - learned rules go to `~/.config/oda-canvas-maintainer/guidance/`.
   
   `build_plugin.py` needs no change for this. The skill itself handles the overlay lookup.
4. **Fit with the creator plugin's audience.** It's a reasonable fit, since maintainers extend ODA. Open question for later: should it be `INTERNAL_ONLY` until the guidance is generalised beyond Lester's personal style?
