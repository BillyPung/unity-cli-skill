# Commands and project workflows

The local command-help baseline is CLI `1.0.0`, checked on 2026-11-13. Check local help before choosing flags. For offline documentation matched to the binary use `unity skill show --list` and `unity skill show --path references/editors-install.md`. Preserve the user's authorization and version policy when using upstream guidance.

Recheck live sources when handling a missing installation, version mismatch or upgrade request. [Versions and setup](versions-and-setup.md)

## Editor and module management

```sh
unity editors --installed --format json
unity editors info <version>
unity editors path <version>
unity editor module list <version> --format json
unity modules list <version> --format json
unity install <version> --dry-run
unity install <version> -m android --child-modules
unity install-modules -e <version> -m android --dry-run
```

`modules list` describes availability; inspect the installed Editor's module state to verify installation. `projects require [pathOrName]` ensures the project's required Editor exists and can install it; it is neither a read-only module check nor a command taking module IDs. Keep it out of inspection-only preflight.

Use explicit architecture where needed. `--cm` remains an alias for `--child-modules`. Inspect install paths and active users before removal, replacement or default changes. Registering a manually installed Editor does not guarantee managed module installation works.

For a Linux runner that needs the headless Editor distribution, use `unity install <version> --headless --dry-run`. Check that the requested build modules are available in that distribution before installing. Omitting `--headless` selects the regular Editor by default. Use `unity run` for batch execution with the installed Editor. CLI 1.0 also fixes no-display `assets import` and `open --batchmode`; a failed import points to its log under the project's `Logs` directory.

On Apple silicon, resumed Editor installation now uses the selected/native architecture. Specify `--architecture x86_64` when deliberately resuming an Intel download; inspect the actual installed architecture afterward.

## Projects

```sh
unity projects info <absolute-project> --format json
unity projects verify <absolute-project>
unity vcs status <absolute-project> --format json
unity open <absolute-project>
unity status --project-path <absolute-project> --until-ready --timeout 300 --format json
```

`projects verify` checks meta/GUID, manifest, conflict and version problems without launching Unity. Inspect templates with a concrete Editor version before creation. Check `projects --help` for the installed version. Beta.16 release notes direct callers from `projects new` to `projects create <name> --no-cloud`. Use `--bare` when creating a project without Pipeline, and inspect the resulting manifest before installing the package.

Before upgrades, require a target version and a recoverable checkpoint, check Editor/module availability, then verify import, compilation and the resulting diff. For an authorized close that must preserve unsaved scenes, use `close <project> --if-saved`. It refuses dirty scenes or an unavailable saved-state check and cannot be combined with `--force`. Neither close path saves the project.

## CLI 1.0 migration

- Prefer `build --output` (also `-o`) over the old `--output-path` alias. Use `--output-dir` for `projects create/clone`, `templates create` and `vcs git worktree add`. For clone it is the exact destination; for project creation it is the parent directory. Inspect each command's help before rewriting an old `--out`, `--path`, `--into` or `templates create --output` alias. Pipeline command parameters still use their own `output-path` contract.
- `recompile` now exits 12 when no Editor answers, matching `unity command`; older scripts may expect 7. A positional project path is also accepted. Closing a path that is not a Unity project now exits 11 with `PROJECTS_CLOSE_NOT_A_PROJECT`; a valid project with no open Editor still succeeds with `reason: not_open`.
- `editors info/upgrade` now report release-service failures instead of claiming a version is absent or current: unreachable service 7, timeout 14, authentication 3, other service errors 6. A 404 still means not found. Diagnose the failure before installing another version.
- CLI 1.0 fixes compatibility with Pipeline 1.0 for builds, strict recompilation, console following and Project Auditor. Check both versions before attributing these failures to a project. [Versions and setup](versions-and-setup.md)

[CLI 1.0 release notes](https://docs.unity.com/en-us/unity-cli/release-notes/2026/november#1.0.0)

## Authentication and licensing

Use `auth status` and `license status/list` when needed. Local Pipeline control does not require a fresh browser login for every operation. Installation/cloud/account operations may need authentication. Let the user finish browser sign-in.

For CI use an existing secret store. Supported service-account variables are `UNITY_SERVICE_ACCOUNT_ID` and `UNITY_SERVICE_ACCOUNT_SECRET`; `auth login --secret-from-stdin` avoids putting the secret in argv. Never echo secrets. Activate/return seats only within scope.

CLI 1.0 no longer silently falls back to plaintext token storage when the OS credential store is unavailable. Inspect `auth status`/`doctor` and fix the configured store, or use the user's explicitly chosen `auth login --insecure-storage` mode. Do not add it just to suppress a credential error. Old file tokens can fail to refresh without a working store or a new explicit sign-in. Service-account CI credentials do not use this token store. Broker refusals, unavailable brokers and denied credential access now have distinct error codes; preserve them in diagnostics.

## Diagnostics, discovery and maintenance

Use the narrowest of `doctor`, `env`, `logs`, `changelog` and `diagnose`. `commands --grep` discovers CLI and plugin capabilities; `commands --include-editor` explicitly adds the connected catalog with `source: editor`. CLI 1.0 can show live parameters through `unity command --project-path <project> <group> <name> --help`. An empty Pipeline search while disconnected does not prove a command is absent. See [MCP and tools](mcp-and-tools.md) for grouping, filters, completions and managed tools.

`pipeline cloud-build` manages Unity Build Automation. Beta.16 added writes for build targets, repository connections and signing credentials. `pipeline automation` manages organization-scoped resources, with app and draft-version creation added in beta.17. Inspect subgroup help and confirm the cloud account, organization and project before a write. [CLI release notes](https://docs.unity.com/en-us/unity-cli/release-notes)

CLI 1.0 adds Automation app actions and pipeline creation from JSON files; review the draft/version and destination before writing. Cloud-build timelines now work on production, and development-build options use the corrected server format. UVCS review operations have Cloud/self-hosted routes through the installed `cm` client: check the operation's required client version and provider before assuming Unity sign-in is needed. Creating reviews, requesting reviewers and posting/resolving comments require that communication to be in the user's task.

`skill show` reads Unity's embedded skill. `skill install/refresh` writes client skill files and can conflict with this separately maintained package. Updating this repository does not update Unity CLI or Pipeline; keep all three version tracks explicit.

## Hub migration and output

Replace Hub `-- --headless` with standalone `unity`; positional `install <version>` replaces `install -v`, and `install-modules -e <version>` selects the Editor. Global `--json` remains valid shorthand for `--format json`. Use `--no-pager` for automation and `--non-interactive` after supplying required values. Piped output may default to TSV.

JSON failures still carry a result on stdout, while stderr holds diagnostics. Avoid assuming every experimental command has an identical schema. NDJSON consumers should look for completion frames and detect truncation; inspect command-specific exceptions. Check exit code as well as the body.

In CLI 1.0, even `--version` and help can start a background update check. For an explicitly offline invocation set `UNITY_NO_UPDATE_CHECK` for that process. A suppressed notice (`--quiet`, JSON, CI or non-interactive output) does not itself disable the check. Structured install/module output keeps notices on stderr; keep that stream separate from stdout parsing. For telemetry choices, the official docs cover `DO_NOT_TRACK`/`UGS_CLI_TELEMETRY_DISABLED`; these do not disable licensing records.

### CLI 1.0.1 output changes

- Piped output defaults to TSV for many commands. Version, configuration, cache-key and update-check commands now use a `key`/`value` header and one row per field. Other commands such as `editors`, `projects create` and `ci init` add table headers. `--no-header` removes the header row only. Request JSON and parse the documented keys for structured use.
- Use `--format human` for bare `cache key`, `editors path`, `docs --url` or raw `ci init --dry-run` YAML. Treat token output as secret regardless of format. `commands` JSON and NDJSON add a full command `path`, such as `analytics opt-in`. `editors path --format ndjson` now emits a single result frame.
- `logs --format ndjson` now includes `total`, `nextPage` and `partial` in its final result frame. Read through that frame and check any paging metadata. TSV from `builds log` and `jobs logs` starts with a `line` header unless `--no-header` is set.
- `commands --grep` accepts Rust regex syntax. Replace patterns using lookaround or backreferences and escape literal braces. Numeric flags such as `--port` and `--limit` require whole numbers in plain decimal. `collab read --timestamp` accepts ISO 8601 dates or RFC 3339/ISO 8601 date-times.
- CLI 1.0.1 redacts remote URL credentials across schemes in `projects unlink vcs` output. Keep credential-bearing remote URLs out of shared diagnostics, especially when working with an older CLI.

[CLI 1.0.1 release notes](https://docs.unity.com/en-us/unity-cli/release-notes/2026/november#1.0.1)

Sources: [CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference), [release notes](https://docs.unity.com/en-us/unity-cli/release-notes), [installation](https://docs.unity.com/en-us/unity-cli/use-unity-cli). Command syntax above was also checked using installed CLI help.

## CLI 1.1 changes

- Editor and module installers can download up to three files in parallel. Set `UNITY_INSTALL_MAX_CONCURRENT_DOWNLOADS` from 1 to 16 when the environment needs a different limit. A missing installed Editor now returns exit 11 / `EDITOR_NOT_INSTALLED` from commands such as `editors path` and `install-modules`. Several project, template, and asset commands also use exit 11 for missing inputs.
- A modal dialog now blocks `close` with exit 18, `PROJECTS_CLOSE_BLOCKED_BY_DIALOG` and reason `blocked_by_dialog`. Inspect the dialog before retrying. See [Editor targeting and recovery](pipeline-package.md#editor-targeting-and-recovery-in-cli-11) for the matching command behavior.
- `projects create` reports `templateVersion` in machine output and can report `TEMPLATE_OTHER_VERSION_ON_DISK` when another installation has a newer template. Check the actual template and Editor selection. For an interrupted `projects create` or `vcs setup`, check JSON or NDJSON for `data.orphanResource` before deciding how to handle an already-created remote.
- `docs toc --format json` adds `markdownUrl` for the scripting reference and manual. Read that URL for Markdown and keep the existing `url` as the HTML citation.
- A proxy environment variable that points to a PAC script now causes exit 2 / `INVALID_COMMAND_ARGS`. A PAC in the proxy settings file still produces exit 1. For Pipeline Automation, a failed token exchange due to network or gateway errors returns exit 7 / `NETWORK_UNREACHABLE`. Check connectivity before retrying sign-in.
- Use `pipeline automation pipelines validate` to check a pipeline JSON without saving or starting a job. `pipelines run` starts a job. CLI 1.1 also adds draft version, action, event and schedule operations. Treat publishing, visibility changes, deletions, and signing credential generation/uploads as separate changes with their own scope. Preview or validate the draft before applying the requested cloud operation.

[CLI 1.1.0 changelog](https://public-cdn.cloud.unity3d.com/hub/prod/cli/1.1.0/CHANGELOG.md)
