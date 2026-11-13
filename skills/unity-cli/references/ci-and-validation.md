# CI, builds and tests

Inspect installed `build`, `test`, `run`, `job` and `ci init` help. Use absolute projects, pinned Editors, explicit output paths and bounded execution times. Do not add `--allow-install` without installation scope.

## Validation choices

- `projects verify`: static integrity checks; no Editor launch.
- `recompile --project-path <project>`: compile through a running Pipeline Editor; `--strict` also fails on warnings. An Editor booted into Safe Mode may be unreachable.
- `test <project> --mode EditMode|PlayMode`: executable tests plus report.
- `build`: artifacts; partial output does not prove success.

## Reports and selection

```sh
unity test <absolute-project> --mode EditMode --report-format nunit,junit --output <absolute-results.xml> --timeout 600 --format json
```

For top-level `unity test`, exit 8 means tests completed with failures; 6 means the run failed without a completed verdict. Read the report and structured codes, distinguishing TESTS_FAILED, TEST_RUN_ERROR and TEST_TIMED_OUT. Diagnose compile/license/crash failures before considering a bounded retry; do not retry assertions as infrastructure failures. Live Pipeline tests have a different contract below.

When setting both `--output` and `--junit-output`, give them distinct destination files. Beta.17 rejects a JUnit path that resolves to the same file as the NUnit report. [CLI release notes](https://docs.unity.com/en-us/unity-cli/release-notes)

`--shard N/M` requires an appropriate full-suite inventory via `--shard-inventory`. Do not run simultaneous Editors on the same project directory; use isolated CI checkouts. `--retries` reports flakes; keep failures visible. `--rerun-failed` consumes the prior report. `--affected` uses impact information and can fall back to all tests; use `--affected-compare` when assessing selection coverage. Coverage requires the project's Code Coverage package. `watch test` is a development loop, not an unattended CI step.

## Live Pipeline tests

For Pipeline 1.0, `unity command ... test run` defaults to `mode=editor`. Modes `playmode` and `all` require `async-tests=true` to survive Play-mode domain reloads. Tests that recompile/reload should also run asynchronously. An async start returning 0 means only that the run started; poll the same run with `test status` through completion.

```sh
unity command --project-path <absolute-project> test run -- --mode all --async-tests true
unity command --project-path <absolute-project> test status -- --detail failures
```

`test status` supports `detail=full|failures|summary`; use summary for cheap polling, then failures for messages and stack traces. Result fields are camelCase (`summary.total`, `results[].fullName`); older packages can differ, so check `tests.camelCase`. Synchronous `test run` writes per-test records and logs its summary to stderr; do not expect the status payload shape from that command.

Pipeline test exit 0 means passed tests, 2 means invalid arguments or no matching tests, 6 means test failures or a run error, and 14 means timeout (the docs note 6 over HTTP). Cancelled `test status` exits 130. A failed status poll still writes the run's results/counts: preserve them before handling the non-zero exit. Mode `all` combines EditMode and PlayMode results and continues into PlayMode even when EditMode tests fail. Starting a new run, cancelling, or timing out a synchronous run stops the run in progress; do not start another merely to obtain status.

[Pipeline build and test reference](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/build-and-compilation.html)

## Build and batch

Discover `--list-targets` and `--list-profiles`. Unity 6 build profiles support package/partner platforms absent from the target list. `--create-profile` writes an asset; listing is read-only. Without a custom execute method, supported built-in builds need an output destination. With `--execute-method`, the project's method must honor the forwarded output contract. Verify artifacts and provenance, not just exit status.

In CLI 1.0 prefer top-level `build --output <path>`/`-o` over the older `--output-path` alias. This rename does not change Pipeline capture/build command parameters. CLI 1.0 fixes builds routed through an already open Pipeline 1.0 Editor and fails with exit 6 when Unity exits 0 but produces neither a logged build result nor output. Check the requested artifact even when the process exits cleanly.

Pipeline 1.0 refuses a Build Profile that is missing, cannot activate, or targets a different platform. Its build uses the profile's scene list, and a valid `dry-run` reports the target and scenes. Review that preview instead of assuming the current Editor settings are the requested build.

`run` supplies batch-mode lifecycle; do not mechanically repeat direct Editor `-batchmode/-quit` flags. With `run --command`, arguments after `--` bind to the registered command instead of reaching the Editor. Check current grouped-name syntax locally.

Detached `command --detach` returns a job ID. Track that same job with `unity job status` or bounded `unity job wait`; cancellation is a request, not proof work reverted. These CLI jobs differ from Pipeline condition waits (`unity command job wait`).

For `test`, `run` and `build --create-profile` with `--allow-install --format ndjson`, distinguish the install's result from the overall command's final result. CLI 1.0 writes a final `success:false` frame when execution fails after successful installation; consume the whole stream and process exit code. On Windows, Ctrl+C during Editor-backed build/run/test now exits 130 for interruption, rather than a missing-result failure. Do not report that as a completed test verdict or retry it automatically.

## CI configuration

`ci init --dry-run` previews GitHub/GitLab workflow generation. Review writes before using `--overwrite`. Project defaults can live in `ProjectSettings/UnityCliConfig.json`; `config resolve <key> <project>` reports the winning layer. Explicit task flags should make critical values visible. Accelerator settings optimize imports but do not change correctness requirements. Keep signing/license/auth secrets in the CI secret store.

The `test`, `build` and `run` flags were checked locally with CLI 1.0.0 on 2026-11-13. For binary-matched details use `unity skill show --path references/build-run-test.md`. [CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference)
