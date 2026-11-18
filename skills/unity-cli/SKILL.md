---
name: unity-cli
description: Manage Unity Editors, modules, projects, builds and tests with the standalone Unity CLI, and drive running Editors or Players through Unity Pipeline. Use for Unity terminal automation, CLI troubleshooting and CI setup; ordinary source edits alone do not require the CLI.
metadata:
  version: "1.6.1"
---

# Unity CLI

Use the installed binary's help and the connected Pipeline package's schema as authoritative. On 2026-11-19 the live feeds reported CLI 1.0.1 and Pipeline 1.0.0. The installed CLI was 1.0.0. The 1.0.1 guidance follows Unity's release notes. Pipeline 1.0 guidance follows Unity's manual and changelog, with live Editor/Player validation pending. Check the intended project's resolved version separately.

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
| MCP clients, tool grouping/filtering, managed CLI tools or command discovery | [MCP and tools](references/mcp-and-tools.md) |
| Builds, tests, reports, sharding, detached jobs or CI | [CI and validation](references/ci-and-validation.md) |
| Play-mode verification, screenshots and console checks | [Play-mode loop](references/playmode-verification.md) |

## Execute within scope

- Keep installs, project upgrades, license activation/return, remote links, cache cleanup and configuration changes within the requested task. Prompt-control flags are not authorization.
- Before a large installation, state the version, modules, architecture and destination if unspecified. Preview with `--dry-run` when supported.
- Before persistent Editor/asset/settings mutations, inspect source-control changes and resolve the exact objects or paths. Preserve unrelated work. Discover the command schema and declared effects; use exposed `dry-run` and `confirm` gates for authorized changes. Not every additive command has those flags.
- Prefer registered Pipeline commands for supported authoring operations. Treat `script eval` as arbitrary C# execution. Use the narrowest code and verify its effects.
- Target the intended checkout explicitly with `--project-path`. Never borrow an Editor on a sibling worktree. Runtime selectors target Players and take precedence over project selection; avoid mixing them.
- Keep port descriptors, bearer tokens, service-account secrets, license serials and signing credentials out of chat, logs and commits. Let the user finish interactive login. Bug-report uploads require explicit scope.

## Verify completion

Use JSON for one result and NDJSON for supported progress streams. Inspect the exit code and any actual response envelope; branch on stable error codes when provided. Pipeline 1.0 `script eval` returns the script's value, including scalars or null, rather than the old eval object. A compile/runtime failure exits 6; do not require a payload `success` field. Keep stdout results and stderr diagnostics separate. See the [Pipeline migration guide](references/pipeline-package.md#pipeline-10-migration) before reusing older parsers. Surface actionable notifications without automatically executing suggested remediation.

Poll the existing operation until terminal state; acceptance is not completion. Verify installed modules, build artifacts, XML test reports, or saved scene/asset diffs as appropriate. For top-level `unity test`, exit 8 means a completed suite with failures; exit 6 means the run failed without a completed verdict. Pipeline `test run/status` instead use 6 for test failures or run errors; inspect their results and diagnostics. Investigate before retrying.

For connection failures distinguish package loading, Safe Mode/compile errors, an unready Editor, sandbox visibility and a wrong target. Use bounded waits and diagnostics; do not silently switch Editors, delete caches or change versions. Report the effective versions, verified result and unresolved blocker.

With CLI 1.0, an unanswered `recompile` exits 12 rather than 7, and closing an invalid project path exits 11. Check [CLI migration guidance](references/command-guide.md#cli-10-migration) when older automation assumes different exit codes or output flags. Prefer `close --if-saved` for an authorized close that must preserve unsaved scenes; it does not save them.

With CLI 1.0.1, request an explicit format when capturing piped output. Older generated CI workflows need `unity cache key --format human` for the bare key. See [output changes](references/command-guide.md#cli-101-output-changes) for TSV headers, NDJSON paging and shell completions.
