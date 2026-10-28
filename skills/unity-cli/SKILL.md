---
name: unity-cli
description: Manage Unity Editors, modules, projects, builds and tests with the standalone Unity CLI, and drive running Editors or Players through Unity Pipeline. Use for Unity terminal automation, CLI troubleshooting and CI setup; ordinary source edits alone do not require the CLI.
metadata:
  version: "1.0.1"
---

# Unity CLI

Use the installed binary's help and the connected Pipeline package's schema as authoritative. This skill was checked on 2026-10-28 against CLI 1.0.0-beta.14 and Pipeline documentation 0.9.1-exp.1. These are verification baselines, not mandatory upgrade targets.

## Resolve and inspect

Locate `ProjectSettings/ProjectVersion.txt`, read the version and revision, and use an absolute project path. Preserve that Editor version unless the user requests an upgrade. For source-only work, edit source directly; invoke Unity when validation or live authoring is needed.

```sh
unity --version
unity --help
unity commands --grep <topic>
unity <command> --help
```

Inspect only the relevant Editor, project, module, auth or license state. If `unity` is missing, check PATH; installation requires setup scope. Do not install or upgrade it just to match this skill.

## Choose the workflow

| Task | Reference |
| --- | --- |
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
