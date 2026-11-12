# Versions, installation and updates

## Checked state on 2026-11-12

| Component | Latest found | Evidence and limits |
| --- | --- | --- |
| Unity CLI | `1.0.0-beta.17` | Local version and selected command help match beta.17. The live update check and target release notes confirm the release. |
| `com.unity.pipeline` | `1.0.0` | Live registry and versioned 1.0 documentation agree. First stable package release on November 11; review covers documentation and command guidance, with live Editor/Player validation pending. Runtime remains experimental for desktop Players. |
| Unity Editor | Unity 6+ for Pipeline | Prerequisite, not a tested Editor matrix. Keep the version in `ProjectSettings/ProjectVersion.txt`; check the selected package's own requirements. |

This snapshot is not a permanent latest-version claim or a promise that all combinations work. The skill/plugin version in `VERSION` is a separate release track.

## Read-only checks

1. Resolve the executable with `Get-Command unity` (PowerShell) or `command -v unity` (POSIX). If missing after installation, reopen the terminal/check PATH before installing again. Check for competing install methods.
2. Run `unity --version` and the needed command's `--help`. Check the live feed with `unity self-update --check --format json`. Inspect `data.currentVersion`, `data.latestVersion`, envelope success and exit status; fields can change in other releases.
3. Run `unity pipeline list-versions --format json`. Read the registry's latest and available versions. In the project, inspect `Packages/manifest.json` for the requested source/version and `Packages/packages-lock.json` for the resolved entry. A range, Git URL or local path is not a resolved registry release. If necessary inspect that package's own `package.json`; do not infer it from the port descriptor.
4. Compare versions with SemVer. For example, `1.0.0` follows `1.0.0-pre.1` and `0.10.0-exp.1`, and `beta.17` follows `beta.16`. Preserve deliberate team pins and check the features needed by the task. A stable package label does not make every workflow stable: Runtime Pipeline remains experimental in 1.0.
5. Discover the running package's command schema and confirm the exact target with `unity status --project-path <absolute-project> --format json`. A current package can still be unavailable because it has not compiled/loaded.

Report installed, requested/resolved and latest available versions separately, with the check date. Report freshness as unknown when a feed fails. For CLI changes use `unity changelog --target <version>` if the public release-notes page lags. For Pipeline changes check the registry first, then open the matching versioned manual and changelog. On 2026-11-12 the `@latest` documentation redirect pointed to the 1.0 manual.

## Install Unity CLI

When the requested setup includes CLI installation, choose one existing/appropriate official channel and carry it through verification. Do not require the user to repeat authorization already given.

| Environment | Install | Update through the same manager |
| --- | --- | --- |
| Windows with winget | `winget install Unity.CLI` | `winget upgrade Unity.CLI` |
| Homebrew | `brew install --cask unity-cli` | `brew upgrade unity-cli` |
| Unity's configured Debian/Ubuntu repository | `sudo apt install unity-cli` | Refresh package indexes, then `sudo apt upgrade unity-cli` |
| Unity's configured Fedora/RHEL repository | `sudo dnf install unity-cli` | `sudo dnf upgrade unity-cli` |

For Linux repository registration or systems without those managers, follow the current [official installation page](https://docs.unity.com/en-us/unity-cli/use-unity-cli), including OS requirements. Do not invent repository/bootstrap commands from memory. This dependency setup is separate from marketplace installation of this skill; it does not require this repository's Python installer.

Beta.15 release notes say the official shell/PowerShell installers can also set up detected coding agents. Keep that extra change in scope: use the documented `UNITY_CLI_SKIP_SETUP=1` for the installer invocation when only the CLI is requested, then restore the previous environment. Do not overwrite this community skill/plugin with Unity's separate agent package incidentally.

## Update Unity CLI

Read `unity self-update --help` and `unity diagnose update --help` first. For supported standalone/MSIX installs:

```sh
unity self-update --check --format json
unity changelog --target <resolved-target-version>
unity self-update --target <agreed-target-version> --dry-run
unity self-update --target <agreed-target-version>
unity --version
```

The last mutating step requires update scope. Use unpinned `unity self-update` only when latest is the user's policy. Homebrew and Linux repository installations should be updated through their manager; winget/MSIX also supports self-update. Do not install a second competing copy to bypass ownership or update errors. Re-read command help after updating; do not assume this snapshot covers all newer behavior. Do not rely on rollback being available for every install type.

## Install or update Pipeline in the intended project

Require a compatible Editor and a recoverable source-control state. Read `pipeline install --help` and `pipeline upgrade --help`. The local beta.17 uses `--version`. Some older binaries used `--package-version`. Preserve existing Git and local dependencies unless the requested change includes replacing their source.

Before a 0.x → 1.0 upgrade, review the [migration changes](pipeline-package.md#pipeline-10-migration): removed aliases/parameter spellings, direct eval values, and changed Pipeline test results/exit codes. Update dependent scripts as part of the authorized migration. An older CLI that sends removed keys can fail with `INVALID_COMMAND_ARGS`; check its version and help rather than silently downgrading the project.

```sh
unity pipeline list-versions --format json
unity pipeline install --project-path <absolute-project> --version <agreed-package-version>
```

For an existing registry package, verify the latest release suits the project before running the authorized update.

```sh
unity pipeline upgrade --project-path <absolute-project>
```

To deliberately select a specific available version, use the explicit install pin after reviewing help; it overwrites an existing package version. `--force` is not needed as a routine update shortcut. Do not assume Pipeline offers `--dry-run`; use only flags in installed help.

Allow UPM resolution, refresh and compilation to finish. Re-read the manifest/lock, inspect their diff, then verify `pipeline list`, target `status --until-ready` with a bounded timeout, and live command discovery. Import/compile failures are not success. If no Editor can be started within scope, report that files were updated but live validation is pending. See [Pipeline recovery and runtime guidance](pipeline-package.md).

[Official CLI install and update guidance](https://docs.unity.com/en-us/unity-cli/use-unity-cli) · [CLI release notes](https://docs.unity.com/en-us/unity-cli/release-notes) · [Pipeline 1.0 changelog](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/changelog/CHANGELOG.html)
