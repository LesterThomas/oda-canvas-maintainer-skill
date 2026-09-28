# ODA Canvas Maintainer Skill

An Agent Skill that helps maintainers of the [TM Forum ODA Canvas](https://github.com/tmforum-oda/oda-canvas) and related `tmforum-oda` repositories triage issues and review pull requests.

The skill reads issues, PRs, diffs, CI results and review threads from GitHub. It then drafts comments, reviews (with a recommended verdict), inline comments, follow-up issues and backlog clean-ups. It **never writes to GitHub**: the maintainer reviews every draft and performs every action themselves. The bundled scripts enforce this with a read-only `gh` allowlist.

Its review knowledge lives in [`skills/oda-canvas-maintainer/guidance/`](skills/oda-canvas-maintainer/guidance/), with one Markdown file per type of guidance. When the maintainer gives feedback while using the skill, the matching guidance file is updated, so reviews keep improving. Git history is the learning log.

**Status:** Phase 2 (core skill) is built and in personal use. See [`spec/spec.md`](spec/spec.md) for the design, [`spec/tasks.md`](spec/tasks.md) for the build plan, and [`research/`](research/) for the evidence behind the seed guidance.

## What it does

| Ask | It produces |
| --- | --- |
| "What needs my attention on the Canvas repos?" | A ranked queue: unreviewed external PRs first |
| "Review https://github.com/tmforum-oda/oda-canvas/pull/613" | A Maintainer Brief: alignment and quality assessment, verdict, draft summary and inline comments, follow-up issues, and the `gh` command to post it |
| "Help me reply to issue #583" | A triage brief: classification, duplicates, labels and a draft reply |
| "Sweep the backlog" | Batches of about 10 stale issues, each classified with a drafted close, refresh or needs-info comment |
| "What have you learned about how I review?" | A summary of learned rules, plus lessons found by comparing drafts with what was actually posted |

A PR is judged on two criteria only: **alignment with the objectives of the ODA** (including the AI-Native Canvas and the ADRs in `oda-ca-docs/Decision-Log`), and **good-enough quality**.

## Install (personal use, Windows)

Link the skill folder into Claude Code's skills directory, so guidance updates land in this repo:

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\oda-canvas-maintainer" -Target "D:\Dev\tmforum-oda\oda-canvas-maintainer-skill\skills\oda-canvas-maintainer"
```

On macOS or Linux, use `ln -s <repo>/skills/oda-canvas-maintainer ~/.claude/skills/oda-canvas-maintainer`.

**Requirements:**
- the `gh` CLI, authenticated with `gh auth login` and with read access to `tmforum-oda`;
- Python 3.10+, standard library only.

**Optional config:** copy [`assets/config.example.yaml`](skills/oda-canvas-maintainer/assets/config.example.yaml) to `~/.config/oda-canvas-maintainer/config.yaml` and edit it. Drafts are saved to `~/.oda-canvas-maintainer/drafts/`.

## Layout

```
skills/oda-canvas-maintainer/     # same layout as oda-agent-skills-marketplace (future home, creator plugin)
├── SKILL.md                      # workflow, fixed principles, brief format, learning loop
├── guidance/                     # LIVING: updated from maintainer feedback
├── references/sources.md         # verified best-practice sources (static)
├── scripts/                      # read-only helpers (gather_item, canvas_pr_checks, draft_diff)
└── assets/config.example.yaml
research/                         # Phase 1 evidence behind the seed guidance
spec/                             # spec.md + tasks.md
```
