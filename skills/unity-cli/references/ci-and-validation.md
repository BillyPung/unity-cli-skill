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

Exit 8 means tests completed with failures; 6 means the run failed without a completed verdict. Read the report and structured codes, distinguishing TESTS_FAILED, TEST_RUN_ERROR and TEST_TIMED_OUT. Diagnose compile/license/crash failures before considering a bounded retry; do not retry assertions as infrastructure failures.

`--shard N/M` requires an appropriate full-suite inventory via `--shard-inventory`. Do not run simultaneous Editors on the same project directory; use isolated CI checkouts. `--retries` reports flakes; keep failures visible. `--rerun-failed` consumes the prior report. `--affected` uses impact information and can fall back to all tests; use `--affected-compare` when assessing selection coverage. Coverage requires the project's Code Coverage package. `watch test` is a development loop, not an unattended CI step.

## Build and batch

Discover `--list-targets` and `--list-profiles`. Unity 6 build profiles support package/partner platforms absent from the target list. `--create-profile` writes an asset; listing is read-only. Without a custom execute method, supported built-in builds need an output destination. With `--execute-method`, the project's method must honor the forwarded output contract. Verify artifacts and provenance, not just exit status.

`run` supplies batch-mode lifecycle; do not mechanically repeat direct Editor `-batchmode/-quit` flags. With `run --command`, arguments after `--` bind to the registered command instead of reaching the Editor. Check current grouped-name syntax locally.

Detached `command --detach` returns a job ID. Track that same job with `unity job status` or bounded `unity job wait`; cancellation is a request, not proof work reverted. These CLI jobs differ from Pipeline condition waits (`unity command job wait`).

## CI configuration

`ci init --dry-run` previews GitHub/GitLab workflow generation. Review writes before using `--overwrite`. Project defaults can live in `ProjectSettings/UnityCliConfig.json`; `config resolve <key> <project>` reports the winning layer. Explicit task flags should make critical values visible. Accelerator settings optimize imports but do not change correctness requirements. Keep signing/license/auth secrets in the CI secret store.

Source: installed CLI beta.14 command help; [CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference). For deeper binary-matched details use `unity skill show --path references/build-run-test.md`.
