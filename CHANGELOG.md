# Changelog

## 1.6.1 — 2026-11-19

- Document Unity CLI 1.0.1 from the release notes and live update feed. The installed CLI was 1.0.0 and the Pipeline registry still reports 1.0.0.
- Update guidance for raw cache keys and workflow previews, TSV headers, NDJSON paging and update results, and shell completion envelopes.
- Document command catalog paths, MCP group filters and the status tool's exclusion behavior.

## 1.6.0 — 2026-11-13

- Verify stable Unity CLI 1.0.0 locally and in the live feed; Pipeline remains 1.0.0.
- Refresh supported versions, installation prerequisites, stable/beta channel guidance, Hub pinning and post-update verification.
- Document CLI output flag conventions, guarded Editor closing, changed exit codes and Pipeline 1.0 compatibility fixes.
- Add live command help, MCP tool grouping/filtering, client configuration migration and managed CLI tool guidance.
- Cover credential-store changes, headless imports, build result validation and final NDJSON/interruption handling. Live Editor/Player/MCP validation remains pending.

## 1.5.0 — 2026-11-12

- Confirm Pipeline 1.0.0 in the live registry and review its first stable release; Unity CLI remains beta.17 locally and in the update feed.
- Update README compatibility and AI version checks, preserving explicit installation/update workflows and project pins.
- Document direct eval values, removed aliases, kebab-case arguments, eval timeout units and the CommandContext authoring API.
- Distinguish live Pipeline test modes, result fields and exit codes from top-level CLI tests; correct capture output paths and Play-mode background handling.
- Add Profiler capture analysis and Scene Preview guidance, plus updated Build Profile and Method Reload constraints. Runtime Pipeline remains experimental for desktop Players; live Editor/Player validation is pending.

## 1.4.0 — 2026-11-07

- Verify CLI beta.17 locally and confirm Pipeline 0.10.0-exp.1 in the live registry.
- Document headless Linux Editor installation, Pipeline TSV changes and the quoted project path discovery fix.
- Update guidance for Pipeline Automation writes and separate test report destinations.

## 1.3.0 — 2026-11-04

- Confirm Pipeline 0.10.0-exp.1 in Unity's registry and review its versioned documentation.
- Update agent guidance for capture paths and overlays, `component get_fields`, protocol exit codes and per-user Editor settings.
- Record experimental desktop Player support and point agents to Profiler and memory capture commands.
- Record CLI beta.16 as available and retain beta.15 as the local command-help baseline.

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
