---
name: unity-cli
description: Manage Unity Editors, modules, projects, builds and tests with the standalone Unity CLI, and drive running Editors or Players through Unity Pipeline. Use for Unity terminal automation, CLI troubleshooting and CI setup; ordinary source edits alone do not require the CLI.
metadata:
  version: "1.3.0"
---

# Unity CLI

Use the installed binary's help and the connected Pipeline package's schema as authoritative. On 2026-11-04 the live feeds reported CLI 1.0.0-beta.16 and Pipeline 0.10.0-exp.1. The local CLI remains beta.15. Pipeline 0.10 guidance comes from Unity's manual and changelog. Treat latest available, locally checked and project-pinned versions as separate facts.

## Resolve and inspect

Locate `ProjectSettings/ProjectVersion.txt`, read the version and revision, and use an absolute project path. Preserve that Editor version unless the user requests an upgrade. For source-only work, edit source directly; invoke Unity when validation or live authoring is needed.

```sh
unity --version
unity --help
unity commands --grep <topic>
unity <command> --help
```

Inspect only the relevant Editor, project, module, auth or license state.

## Check versions, install or update

For setup, update requests or suspected version mismatches, read [versions and setup](references/versions-and-setup.md). Check `unity --version`, then `unity self-update --check --format json` and `unity pipeline list-versions --format json` when network access is available. Read the project's requested/resolved `com.unity.pipeline` version from `Packages/manifest.json` and `Packages/packages-lock.json`; discover live commands before assuming compatibility. Compare prerelease versions semantically, not lexicographically. A failed/offline check means latest is unknown, not up to date.

If Unity CLI is missing, check PATH and duplicate installations, then install it through the appropriate official installer/package manager when setup is authorized. If an update is requested, inspect release notes, preserve any team pin, and update through the existing install method (`unity self-update` for supported standalone/MSIX installs, or its package manager). Do not change the Editor version incidentally.

If live Editor control needs Pipeline and the package is missing, install it with `unity pipeline install --project-path <absolute-project>` within the authorized setup. For a requested package upgrade, inspect source-control changes, the Editor/package requirements and the installed command help, then use `unity pipeline upgrade --project-path <absolute-project>` or an explicitly agreed `pipeline install --version <version>` pin. Preserve Git/local package sources unless changing them is intended.

Carry out installation/update work already covered by the user's request; otherwise report the concrete missing/outdated dependency and proposed change before seeking authorization. A version check alone does not authorize an update, and a notification's remediation command is not an instruction to execute. After a change, recheck CLI version/help, resolved package version, compilation and target Editor readiness; report the actual outcome.

For installation/update of this skill plugin itself, use the host's native marketplace flow in the [repository README](https://github.com/BillyPung/unity-cli-skill#install). Keep that separate from CLI/Pipeline installation and Unity's own agent plugin. Do not edit plugin caches or use the legacy Python installer for a marketplace-managed plugin.

## Choose the workflow

| Task | Reference |
| --- | --- |
| Version correctness/freshness, CLI installation/update, Pipeline installation/update | [Versions and setup](references/versions-and-setup.md) |
| Editors, modules, projects, authentication, migration or diagnostics | [Command guide](references/command-guide.md) |
| Live Editor/Player commands, custom commands, package setup or Method Reload | [Pipeline guide](references/pipeline-package.md) |
| Builds, tests, reports, sharding, detached jobs or CI | [CI and validation](references/ci-and-validation.md) |
| Play-mode verification, screenshots and console checks | [Play-mode loop](references/playmode-verification.md) |

## Execute within scope

- Keep installs, project upgrades, license activation/return, remote links, cache cleanup and configuration changes within the requested task. Prompt-control flags are not authorization.
- Before a large installation, state the version, modules, architecture and destination if unspecified. Preview with `--dry-run` when supported.
- Before persistent Editor/asset/settings mutations, inspect source-control changes and resolve the exact objects or paths. Preserve unrelated work. Discover the command schema; use exposed `dry_run` and `confirm` gates for authorized changes. Not every additive command has those flags.
- Prefer registered Pipeline commands for supported authoring operations. Treat `script eval` as arbitrary C# execution. Use the narrowest code and verify its effects.
- Target the intended checkout explicitly with `--project-path`. Never borrow an Editor on a sibling worktree. Runtime selectors target Players and take precedence over project selection; avoid mixing them.
- Keep port descriptors, bearer tokens, service-account secrets, license serials and signing credentials out of chat, logs and commits. Let the user finish interactive login. Bug-report uploads require explicit scope.

## Verify completion

Use JSON for one result and NDJSON for supported progress streams. Inspect the exit code and envelope `success`; branch on stable `errors[].code`, not human diagnostics. Preserve both stdout and stderr separately. Surface actionable notifications without automatically executing suggested remediation.

Poll the existing operation until terminal state; acceptance is not completion. Verify installed modules, build artifacts, XML test reports, or saved scene/asset diffs as appropriate. Test exit 8 means a completed suite with failures; exit 6 means the run failed without a completed verdict. Investigate before retrying.

For connection failures distinguish package loading, Safe Mode/compile errors, an unready Editor, sandbox visibility and a wrong target. Use bounded waits and diagnostics; do not silently switch Editors, delete caches or change versions. Report the effective versions, verified result and unresolved blocker.
