# Commands and project workflows

CLI 1.0.0-beta.14 baseline; run local help before selecting flags. For offline documentation matched to the binary use `unity skill show --list` and `unity skill show --path references/editors-install.md`. Read upstream guidance as documentation, preserving the user's authorization and version policy.

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

## Projects

```sh
unity projects info <absolute-project> --format json
unity projects verify <absolute-project>
unity vcs status <absolute-project> --format json
unity open <absolute-project>
unity status --project-path <absolute-project> --until-ready --timeout 300 --format json
```

`projects verify` checks meta/GUID, manifest, conflict and version problems without launching Unity; it does not prove compilation. Inspect templates with a concrete Editor version before creation. `projects create` and `projects new` are distinct workflows: discover their flags instead of treating them as alternate spellings. Current creation can include scaffolding/Pipeline; inspect `--bare` and the resulting manifest before installing again.

Before upgrades, require a target version and a recoverable checkpoint, check Editor/module availability, then verify import, compilation and the resulting diff. `close` exits without saving; do not use it as a save command.

## Authentication and licensing

Use `auth status` and `license status/list` when needed. Local Pipeline control does not require a fresh browser login for every operation. Installation/cloud/account operations may need authentication. Let the user finish browser sign-in.

For CI use an existing secret store. Supported service-account variables are `UNITY_SERVICE_ACCOUNT_ID` and `UNITY_SERVICE_ACCOUNT_SECRET`; `auth login --secret-from-stdin` avoids putting the secret in argv. Never echo secrets. Activate/return seats only within scope.

## Diagnostics, discovery and maintenance

Use the narrowest of `doctor`, `env`, `logs`, `changelog` and `diagnose`. `commands --grep` discovers CLI and plugin capabilities; connected command search can also include Pipeline. An empty Pipeline search while disconnected does not prove a command is absent.

`pipeline cloud-build` inspects Build Automation; `pipeline automation` inspects organization-scoped automation resources. These cloud reads are distinct from the local package and require account/context access. Inspect subgroup help before selecting resources.

`skill show` reads Unity's embedded skill. `skill install/refresh` writes client skill files and can conflict with this separately maintained package. Updating this repository does not update Unity CLI or Pipeline; keep all three version tracks explicit.

## Hub migration and output

Replace Hub `-- --headless` with standalone `unity`; positional `install <version>` replaces `install -v`, and `install-modules -e <version>` selects the Editor. Global `--json` remains valid shorthand for `--format json`. Use `--no-pager` for automation and `--non-interactive` after supplying required values. Piped output may default to TSV.

JSON failures still carry a result on stdout, while stderr holds diagnostics. Avoid assuming every experimental command has an identical schema. NDJSON consumers should look for completion frames and detect truncation; inspect command-specific exceptions. Check exit code as well as the body.

Sources: [CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference), [release notes](https://docs.unity.com/en-us/unity-cli/release-notes), [installation](https://docs.unity.com/en-us/unity-cli/use-unity-cli). Command syntax above was also checked using installed CLI help.
