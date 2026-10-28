# Unity Pipeline

Baseline: com.unity.pipeline 0.9.1-exp.1 documentation. Live commands require Unity 6+ and a compiled package. Preserve an existing package version unless an update is requested or necessary and authorized.

## Installation and discovery

Inspect `pipeline install --help` first. CLI beta.14 uses `--version` for a package pin; older binaries used `--package-version`.

```sh
unity pipeline install --project-path <absolute-project>
unity pipeline list
unity status --project-path <absolute-project> --until-ready --timeout 300 --format json
unity command --project-path <absolute-project>
unity command --project-path <absolute-project> --detail full --format json
```

Install before first open when setup is requested. If installing into an open Editor, wait for resolution/compilation and refresh. Safe Mode can prevent Pipeline loading at all; `recompile` cannot diagnose through a server that never started. Inspect Editor logs and fix startup compile errors. A sandbox can also hide an existing Editor: absence from status alone is not proof it is stopped.

## Grouped commands and selection

Pipeline 0.9 uses `unity command <group> <name>`. Discover groups and schema rather than retaining a hard-coded catalog. Examples:

```sh
unity command --project-path <absolute-project> editor status
unity command --project-path <absolute-project> package list
unity command --project-path <absolute-project> script eval -- --code "return UnityEngine.Application.unityVersion;"
unity command --project-path <absolute-project> --obsolete-command-names --format json
```

The last command maps obsolete names when the connected package supports it. Flat names from 0.4, such as `editor_status` and `runtime_status`, are not current package syntax. Top-level `unity eval` is absent in CLI beta.14. Older Pipeline packages can expose `eval` under `unity command`; discover their schema explicitly.

CLI beta.14 supports `--port`, `--pid`, and `--instance` for explicit Editor selection. For worktrees always target the owning project. New listings use `--group-by`; the old `--group_by` spelling is deprecated. Listing filters, detail and paging reduce large responses.

Put Pipeline arguments after `--` to prevent collisions with CLI flags. CLI timeout is seconds; `script eval`'s code timeout is milliseconds. Inspect the live schema for other timeout contracts.

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

Target Players with `--runtime <process-name>` or `--runtime-path <descriptor-folder-or-bundle>` before the command group, e.g. `unity command --runtime MyGame.exe runtime status`. Do not assume universal platform support: build target, backend, network reachability, stripping and individual command support must all be checked.

Method Reload uses `[MethodReload]` and `script.methodreload` commands. Editor compilation/push and IL-interpreter routes support workflows beyond the old Mono-only pattern; direct Roslyn compilation has platform constraints. For IL2CPP check preserved members and generated link.xml requirements. Verify reload status, then validate persistent source with a normal compilation/build; a reload is not that validation.

[Runtime setup](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/runtime-setup.html), [Method Reload](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/method-reload.html), [package changelog](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/changelog/CHANGELOG.html)

## Connectivity and multiplayer

Prefer CLI discovery over parsing descriptors or hard-coded ports. Direct clients dial IPv4 `127.0.0.1`, with bearer authentication; keep descriptors private. The usual ranges are 7800–7849 (Editor) and 7900–7949 (Player). Do not expose or forward the execution server to other hosts.

Multiplayer Play Mode scenario commands require Unity 6000.3+ and the matching package. Discover scenarios, start through the scenario manager, poll each player's reachability and target its returned project path/instance. Do not use ordinary play entry for an orchestrated scenario.

[Connectivity](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/connectivity.html), [MPPM](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/commands/multiplayer-play-mode.html), [command index](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/index.html)
