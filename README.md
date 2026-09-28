# ODA Canvas Maintainer Skill

An Agent Skill that helps maintainers of the [TM Forum ODA Canvas](https://github.com/tmforum-oda/oda-canvas) and related `tmforum-oda` repositories triage issues and review pull requests.

The skill reads issues, PRs, diffs and CI results from GitHub. It then drafts comments, reviews, suggested labels and next actions. It **never writes to GitHub**: the human maintainer reviews every draft and performs every action themselves.

**Status:** specification stage. See [`spec/spec.md`](spec/spec.md) for the design and [`spec/tasks.md`](spec/tasks.md) for the build plan.
