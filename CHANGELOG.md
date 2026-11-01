# Changelog

## 1.2.0 — 2026-11-02

- Check live Unity feeds: CLI beta.15 is available; Pipeline remains 0.9.1-exp.1.
- Verify the user's newly installed beta.15 version, relevant command help and live freshness check locally.
- Add a dated README compatibility table, separating upstream availability from locally checked help and documentation review.
- Teach agents to inspect resolved project dependencies and recheck live feeds, pins, prereleases and command schemas.
- Add explicit CLI/Pipeline install and update workflows, package-manager routing and post-change verification.
- Account for beta.15 installers setting up coding agents, keeping that separate from CLI-only setup.

## 1.1.0 — 2026-10-28

- Add Claude Code and Codex Git-backed marketplaces, plus portable Agent Plugins packaging.
- Support OMP marketplace installation through the Claude-compatible catalog.
- Make native install/update flows the default; add an OpenCode skills CLI option.
- Rewrite repository and plugin descriptions around practical Unity workflows.
- Clarify repository marketplaces versus the universal public plugin directory.

## 1.0.1 — 2026-10-28

- Resolve macOS temporary-directory aliases in tests while preserving linked-destination refusal.
- Verify installer tests on GitHub-hosted Windows, macOS and Linux runners.

## 1.0.0 — 2026-10-28

- Refresh guidance for Unity CLI 1.0.0-beta.14 and Pipeline docs 0.9.1-exp.1.
- Correct test exit codes, projects require, grouped command names and eval invocation.
- Replace old runtime component/HotReload guidance with bootstrap and Method Reload.
- Add readiness, targeting, CI, cloud routing and play-mode verification references.
- Ship a portable Agent Skills folder and cross-platform backup-first installer.
- Document installation/update paths for Claude Code, Codex, OpenCode and Oh My Pi.
