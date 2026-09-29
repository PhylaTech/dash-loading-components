<!--
PR title must be Conventional Commits — this repo squash-merges to main,
so the PR title becomes the commit subject release-please sees.

Pattern:  <type>(<optional scope>): <description>
Examples: feat: add gridora family
          fix(gallery): meta tags for previews
          chore(deps): bump flicker-dot to 0.2.0
-->

## What

<!-- Brief description of the change. -->

## Checklist

- [ ] PR title starts with `feat:` / `fix:` / `perf:` / `revert:` (if this should ship in the next PyPI release) or `chore:` / `docs:` / `ci:` / `test:` / `style:` / `refactor:` (if not)
- [ ] I expect release-please to open a release PR after this merges (feat/fix/perf/revert) — or I do **not** expect one (chore/docs/ci/…)
- [ ] If marketing copy (README, gallery) was touched, component counts and family descriptions match the code
