# Unity Pipeline

Documentation baseline is `com.unity.pipeline` 0.10.0-exp.1. Live commands require Unity 6+ and a compiled package. Preserve existing project pins when choosing versions.

The live registry confirmed 0.10.0-exp.1 as latest on 2026-11-07. Recheck the registry and resolved dependency before updating. [Versions and setup](versions-and-setup.md)

## Installation and discovery

Inspect `pipeline install --help` first. The local beta.17 accepts `--version` for a package pin. Some older binaries used `--package-version`.

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

Pipeline 0.9 and 0.10 use `unity command <group> <name>`. Discover the groups and schema for the installed package.

```sh
unity command --project-path <absolute-project> editor status
unity command --project-path <absolute-project> package list
unity command --project-path <absolute-project> script eval -- --code "return UnityEngine.Application.unityVersion;"
unity command --project-path <absolute-project> --obsolete-command-names --format json
```

The last command maps obsolete names when the connected package supports it. Flat names from 0.4, such as `editor_status` and `runtime_status`, are not current package syntax. Top-level `unity eval` is absent in CLI beta.14. Older Pipeline packages can expose `eval` under `unity command`; discover their schema explicitly.

CLI beta.14 supports `--port`, `--pid`, and `--instance` for explicit Editor selection. For worktrees always target the owning project. New listings use `--group-by`; the old `--group_by` spelling is deprecated. Listing filters, detail and paging reduce large responses.

Put Pipeline arguments after `--` to prevent collisions with CLI flags. CLI timeout is seconds; `script eval`'s code timeout is milliseconds. Inspect the live schema for other timeout contracts.

## Pipeline 0.10 migration

- For `component get_fields`, 0.10 uses `detail=value` where older versions used `format=value`. When authoring commands for 0.10, leave `format`, `json`, `fields`, `verbose` and `omit-nulls` to the executor.
- Check the Editor's `transport.pipelineProtocol` capability and the client's support before using package-formatted streaming. Pipeline protocol server errors start at exit code 100 in 0.10. Apply that rule to protocol responses and consult the installed CLI's exit-code contract for the outer command.
- Editor server settings migrate from `ProjectSettings/` to per-user `UserSettings/`. Check each Editor's configuration when reproducing settings across a team. `editor status` now reports domain reload count and Auto Refresh. On Unity 6.3+ the toolbar can start and stop the server.
- Discover Profiler capture and memory snapshot commands for the target Editor or desktop Player. The [play-mode guide](playmode-verification.md) covers capture changes that affect existing scripts.

[Pipeline 0.10 release notes](https://docs.unity3d.com/Packages/com.unity.pipeline@0.10/changelog/CHANGELOG.html) · [Connectivity and capabilities](https://docs.unity3d.com/Packages/com.unity.pipeline@0.10/manual/connectivity.html)

## Mutation and batch handling

Resolve stable object/asset identities and inspect source-control state first. Destructive/overwriting commands may expose `dry_run` and `confirm`; preview takes precedence. Additive commands may expose neither. Inspect nested returned results as well as transport/envelope success.

`job batch` executes several operations with references and Undo grouping. Validate its documented limitations: filesystem, package, bake and settings writes are not all rollbackable. Keep writes under the configured authoring root; do not widen it to work around a failed path check. Poll async build/test/package/bake status to completion.

See [mutation conventions](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/safety-and-mutations.html) and [batch commands](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/commands/batch.html).

## Custom commands

Use static handlers with `[CliGroupCommand(group, description)]` and `[CliArg]` metadata; keep Unity API work on the main thread. The default is `MainThreadRequired=true`. In 0.9.1 `[CliCommand]` also supports explicit group/name and dotted-name overloads. Inspect installed API signatures before copying older examples.

Attributes live in `Unity.Pipeline.Attributes`; richer APIs such as `CommandRegistry` and `IStructuredCommandInput` require the appropriate Pipeline assembly. Return serializable values and let the server wrap them. `CliCommand.RuntimeOnly` was removed: use runtime tags. Tags do not hide commands or authorize access. New registrations appear after compilation/domain reload. Verify schema and success/error behavior.

[Creating commands](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/creating-commands.html)

## Runtime setup and Method Reload

Current setup uses Project Settings > Pipeline > Runtime and automatic `RuntimePipelineBootstrap`; no manager component is required in a startup scene. Development/profiled and release inclusion are separate toggles. Do not enable release inclusion incidentally: it adds the command server and code-execution surface. Do not carry forward the old assertion that release builds always exclude Pipeline.

Pipeline 0.10 documents experimental Runtime Pipeline support for desktop Players on Windows, macOS and Linux. Target a Player with `--runtime <process-name>` or `--runtime-path <descriptor-folder-or-bundle>` before the command group. For example, run `unity command --runtime MyGame.exe runtime status`. Check the Player's scripting backend, reachability, stripping and command availability. [Runtime setup](https://docs.unity3d.com/Packages/com.unity.pipeline@0.10/manual/runtime-setup.html)

Method Reload uses `[MethodReload]` and `script.methodreload` commands. Editor compilation/push and IL-interpreter routes support workflows beyond the old Mono-only pattern; direct Roslyn compilation has platform constraints. For IL2CPP check preserved members and generated link.xml requirements. Verify reload status, then validate persistent source with a normal compilation/build; a reload is not that validation.

[Method Reload](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/method-reload.html)

## Connectivity and multiplayer

Prefer CLI discovery over parsing descriptors or hard-coded ports. Direct clients dial IPv4 `127.0.0.1`, with bearer authentication; keep descriptors private. The usual ranges are 7800–7849 (Editor) and 7900–7949 (Player). Do not expose or forward the execution server to other hosts.

Multiplayer Play Mode scenario commands require Unity 6000.3+ and the matching package. Discover scenarios, start through the scenario manager, poll each player's reachability and target its returned project path/instance. Do not use ordinary play entry for an orchestrated scenario.

[Connectivity](https://docs.unity3d.com/Packages/com.unity.pipeline@0.10/manual/connectivity.html) · [MPPM](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/commands/multiplayer-play-mode.html) · [Package manual](https://docs.unity3d.com/Packages/com.unity.pipeline@0.10/manual/index.html)
