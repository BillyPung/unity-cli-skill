# Unity Pipeline

Documentation baseline is `com.unity.pipeline` 1.0.0, the first stable package release. Live commands require Unity 6+ and a compiled package; individual features can require newer Editors. Preserve existing project pins when choosing versions. Runtime Pipeline remains experimental for desktop Players.

The live registry confirmed 1.0.0 as latest on 2026-11-19. This baseline is a documentation review, with live Editor/Player validation pending. Recheck the registry and resolved dependency before updating. [Versions and setup](versions-and-setup.md)

## Installation and discovery

Inspect `pipeline install --help` first. The local CLI 1.0 accepts `--version` for a package pin. Some older binaries used `--package-version`.

```sh
unity pipeline install --project-path <absolute-project>
unity pipeline list
unity status --project-path <absolute-project> --until-ready --timeout 300 --format json
unity command --project-path <absolute-project>
unity command --project-path <absolute-project> --detail full --format json
```

Install before first open when setup is requested. If installing into an open Editor, wait for resolution/compilation and refresh. Safe Mode can prevent Pipeline loading at all; `recompile` cannot diagnose through a server that never started. Inspect Editor logs and fix startup compile errors. A sandbox can also hide an existing Editor: absence from status alone is not proof it is stopped.

For scripted installs and upgrades, prefer `--format json` and inspect the resolved package version. Beta.17 emits TSV fields as key/value rows with a header. Check any parser that expects the earlier positional row. Beta.17 also fixes Editor discovery for launches with a quoted `-projectPath` argument. Check the CLI version if an older binary misses an Editor launched that way. [CLI release notes](https://docs.unity.com/en-us/unity-cli/release-notes)

## Grouped commands and selection

Pipeline 1.0 uses `unity command <group> <name>`. Discover the groups, effects, package version and schema for the installed package.

```sh
unity command --project-path <absolute-project> editor status
unity command --project-path <absolute-project> package list
unity command --project-path <absolute-project> script eval -- --code "return UnityEngine.Application.unityVersion;"
```

Flat names from 0.4, such as `editor_status` and `runtime_status`, no longer redirect in 1.0, and the catalog no longer lists them. Older packages may support `--obsolete-command-names` to map replacements; do not depend on that listing for 1.0 migration. Use `script eval`, or `script eval -- --file <path.cs>` for a file: `script eval_file` has been removed. Top-level `unity eval` is absent in CLI beta.14.

CLI 1.0 supports `--port`, `--pid`, and `--instance` for explicit Editor selection. For worktrees always target the owning project. Listings use `--group-by`; Pipeline 1.0 refuses the old `group_by` key. Listing filters, detail and paging reduce large responses. CLI 1.0 also reads command help directly from the Editor, for example `unity command --project-path <absolute-project> component get_fields --help`.

Put Pipeline arguments after `--` to prevent collisions with CLI flags. In the 1.0 schema both the CLI timeout and `script eval`'s `timeout` are seconds; code helpers such as `Wait.Until(..., timeoutMs: ...)` use milliseconds. An eval request timing out can leave the script running detached; inspect existing work before retrying. Prefer an explicit detached job for long waits. Inspect the live schema for other timeout contracts.

## Pipeline 1.0 migration

- `script eval` returns the script's JSON value (a scalar, object, list or null), replacing the old eval object with `output`, `diagnostics`, `success` and `result`. This applies to `--result-only`, `--format json`, piped output, detached `unity job wait`, and `unity run --command "script eval" --json`. Keep any outer CLI envelope separate from the eval value. Compilation/runtime failures exit 6 and write diagnostics to stderr; invalid arguments use 2. A compile-only `--dry-run` writes no value. Do not test for an eval payload's `success` field.
- Built-in parameters use kebab-case for both flags and structured keys: `output-path`, `dry-run`, `since-session`, `group-by`. Pre-kebab aliases `outputPath`, `since_session` and `group_by` are now removed. Unknown structured keys fail rather than being ignored. Use `enabled` for on/off settings and `package add`'s `name` parameter. Recheck old client-generated requests on `INVALID_COMMAND_ARGS`.
- Ungrouped command aliases, `capture screenshot` and `script eval_file` are removed. Use the grouped catalog and current capture/eval commands. `component set_field` now treats numeric enums as their underlying values, accepts named `[Flags]` combinations, and reads/writes serializable structs and lists as JSON objects. Object paths can select prefab children, for example `Assets/UI/Screen.prefab:Canvas/Header`.
- `test run/status` use camelCase result fields (`summary.total`, `results[].fullName`); check `tests.camelCase` when supporting older packages. Live test defaults, async requirements, poll details and exit codes differ from top-level `unity test`; see [CI and validation](ci-and-validation.md#live-pipeline-tests).
- `editor.playmode start` and `start_scenario` turn Run In Background on until play mode exits; `--run-in-background false` preserves the project's setting. Play entry now fails while scripts have compile errors. Verify frames still advance. [Play-mode loop](playmode-verification.md)
- Commands declare effects in the catalog. Profiler capture analysis and the `CommandContext` authoring API are covered below. Some formerly public server, dispatcher, settings and response types are now internal; compile custom integrations against the installed package instead of using those implementation types.

The following changes from 0.10 also apply:

- For `component get_fields`, use `detail=value` where older versions used `format=value`. When authoring commands, leave `format`, `json`, `fields`, `verbose` and `omit-nulls` to the executor.
- Check the Editor's `transport.pipelineProtocol` capability and the client's support before using package-formatted streaming. Pipeline protocol server errors start at exit code 100 in 0.10. Apply that rule to protocol responses and consult the installed CLI's exit-code contract for the outer command.
- Editor server settings migrate from `ProjectSettings/` to per-user `UserSettings/`. Check each Editor's configuration when reproducing settings across a team. `editor status` now reports domain reload count and Auto Refresh. On Unity 6.3+ the toolbar can start and stop the server.
- The [play-mode guide](playmode-verification.md) covers capture paths, overlays and frame freshness.

[Pipeline 1.0 release notes](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/changelog/CHANGELOG.html) · [Script commands](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/scripts.html) · [Connectivity and capabilities](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/connectivity.html)

## Mutation and batch handling

Resolve stable object/asset identities and inspect source-control state first. Read the catalog's read-only, destructive and idempotent effects as metadata about the command, not user authorization. Destructive/overwriting commands may expose `dry-run` and `confirm`; preview takes precedence. Additive commands may expose neither. Inspect the exit code and any available result/envelope; failures can still carry useful results, as with `test status`. Batch timeout now uses 14 instead of generic failure 6.

`job batch` executes several operations with references and Undo grouping. Validate its documented limitations: filesystem, package, bake and settings writes are not all rollbackable. Keep writes under the configured authoring root; do not widen it to work around a failed path check. Poll async build/test/package/bake status to completion.

See [mutation conventions](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/safety-and-mutations.html) and [batch commands](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/batch.html).

## Custom commands

Use static handlers with `[CliGroupCommand(group, description)]` and `[CliArg]` metadata; keep Unity API work on the main thread. The default is `MainThreadRequired=true`. Declare the strongest applicable `CommandEffect`, including `Destructive` when a command takes `confirm` even for occasional overwrites. Use kebab-case parameter metadata in new commands. Inspect installed API signatures before copying older examples.

Attributes live in `Unity.Pipeline.Attributes`; richer APIs require the appropriate Pipeline assembly. In 1.0 use a `CommandContext` and return `ExitCode` or `Task<ExitCode>`: write one result with `cmd.Result.Write`, or stream records with `WriteRecord`, and log through `cmd.Log` to stderr. Do not mix result writes with raw `cmd.Std.Out`. `--log-level` and `--log-format json` control diagnostics; preserve valid stdout results. Handle cooperative cancellation and cleanup across frames. Legacy value-returning signatures remain supported but cannot take a `CommandContext`. `CliCommand.RuntimeOnly` was removed: use runtime tags. Tags do not hide commands or authorize access. Recompile and verify the new catalog and success/error behavior.

[Creating commands](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/creating-commands.html)

## Profiler captures and Scene Preview

Discover `diagnostics profiler_record` and memory snapshot commands for the target Editor or desktop Player, then poll their status. For saved `.data` captures, `diagnostics profiler_session` opens a session; pass its `sessionId` through the `session` argument to `profiler_summary`, `profiler_frame`, `profiler_markers`, `profiler_sample` and `profiler_counters`. These can rank CPU/GC/GPU frames, inspect hot paths and allocation callstacks, and explain marker costs. Inspect their schema before selecting frame ranges or sorting.

Loading a capture replaces the Editor's Profiler history. Use `dry-run` to preview, preserve an unsaved recording, then apply `confirm` only within the authorized analysis. A load is refused while recording or taking a memory snapshot. Switching sessions can reload history too. Sessions end on domain reload; `profiler_close` releases them without clearing the current Profiler history. [Profiling and memory](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/profiling-and-memory.html)

Scene Preview can build an asset content archive and load it in a preview Player. Configure the preview Build Profile and allowed assemblies in Project Settings > Pipeline > Editor. Its `ENABLE_PIPELINE_SCENE_PREVIEW` define is independent of the Runtime toggles; do not add it to normal game builds incidentally. Project Service delivery needs Unity 6000.7+, while the importer/loader support the package's other Editor versions. [Scene Preview](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/scene-preview.html)

## Runtime setup and Method Reload

Current setup uses Project Settings > Pipeline > Runtime and automatic `RuntimePipelineBootstrap`; no manager component is required in a startup scene. Development/profiled and release inclusion are separate toggles. Do not enable release inclusion incidentally: it adds the command server and code-execution surface. Do not carry forward the old assertion that release builds always exclude Pipeline.

Pipeline 1.0 still documents experimental Runtime Pipeline support for desktop Players on Windows, macOS and Linux. Target a Player with `--runtime <process-name>` or `--runtime-path <descriptor-folder-or-bundle>` before the command group. For example, run `unity command --runtime MyGame.exe runtime status`. Check the Player's scripting backend, reachability, stripping and command availability. [Runtime setup](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/runtime-setup.html)

Method Reload uses `[MethodReload]` and `script.methodreload` commands. Editor compilation/push and IL-interpreter routes support workflows beyond the old Mono-only pattern; direct Roslyn compilation has platform constraints. In 1.0, Editor `script.methodreload reload` and `script run --mode hotpatch` refuse source outside `Assets/` and loaded packages; do not bypass the boundary. Removed attribute members include `MethodReloadAttribute.Id` and `MethodReloadOverrideMethodAttribute.Description`. For IL2CPP check preserved members and generated link.xml requirements. Verify reload status, then validate persistent source with a normal compilation/build; a reload is not that validation.

[Method Reload](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/method-reload.html)

## Connectivity and multiplayer

Prefer CLI discovery over parsing descriptors or hard-coded ports. Direct clients dial IPv4 `127.0.0.1`, with bearer authentication; keep descriptors private. The usual ranges are 7800–7849 (Editor) and 7900–7949 (Player). In 1.0 the Editor refuses to write its descriptor if it cannot restrict it to the current user; inspect the logged permission problem rather than making it public. Do not expose or forward the execution server to other hosts.

Multiplayer Play Mode scenario commands require Unity 6000.3+ and the matching package. Discover scenarios, start through the scenario manager, poll each player's reachability and target its returned project path/instance. Do not use ordinary play entry for an orchestrated scenario.

[Connectivity](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/connectivity.html) · [MPPM](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/multiplayer-play-mode.html) · [Package manual](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/index.html)
