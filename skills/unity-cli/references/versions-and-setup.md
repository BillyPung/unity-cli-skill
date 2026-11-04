# Versions, installation and updates

## Checked state on 2026-11-04

| Component | Latest found | Evidence and limits |
| --- | --- | --- |
| Unity CLI | `1.0.0-beta.16` | Local CLI is beta.15. Live `self-update --check` and `changelog --target` verified beta.16 availability and notes. |
| `com.unity.pipeline` | `0.10.0-exp.1` | Live registry and versioned 0.10 documentation agree. The review covers documentation and command guidance. |
| Unity Editor | Unity 6+ for Pipeline | Prerequisite, not a tested Editor matrix. Keep the version in `ProjectSettings/ProjectVersion.txt`; check the selected package's own requirements. |

This snapshot is not a permanent latest-version claim or a promise that all combinations work. The skill/plugin version in `VERSION` is a separate release track.

## Read-only checks

1. Resolve the executable with `Get-Command unity` (PowerShell) or `command -v unity` (POSIX). If missing after installation, reopen the terminal/check PATH before installing again. Check for competing install methods.
2. Run `unity --version` and the needed command's `--help`. Check the live feed with `unity self-update --check --format json`. Inspect `data.currentVersion`, `data.latestVersion`, envelope success and exit status; fields can change in other releases.
3. Run `unity pipeline list-versions --format json`. Read the registry's latest and available versions. In the project, inspect `Packages/manifest.json` for the requested source/version and `Packages/packages-lock.json` for the resolved entry. A range, Git URL or local path is not a resolved registry release. If necessary inspect that package's own `package.json`; do not infer it from the port descriptor.
4. Compare versions with SemVer. For example, `0.10.0-exp.1` follows `0.9.1-exp.1`, and `beta.16` follows `beta.15`. Preserve deliberate team pins and check the features needed by the task.
5. Discover the running package's command schema and confirm the exact target with `unity status --project-path <absolute-project> --format json`. A current package can still be unavailable because it has not compiled/loaded.

Report installed, requested/resolved and latest available versions separately, with the check date. Report freshness as unknown when a feed fails. For CLI changes use `unity changelog --target <version>` if the public release-notes page lags. For Pipeline changes open the matching versioned manual and changelog. On 2026-11-04 the Pipeline `@latest` documentation redirect still pointed to 0.9 while the registry and 0.10 changelog showed 0.10.0-exp.1.

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

Require a compatible Editor and a recoverable source-control state. Read `pipeline install --help` and `pipeline upgrade --help`. Beta.14 and beta.15 use `--version`; older binaries used `--package-version`. Do not overwrite an existing Git/local dependency merely to match the registry snapshot.

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

[Official CLI install and update guidance](https://docs.unity.com/en-us/unity-cli/use-unity-cli) · [CLI release notes](https://docs.unity.com/en-us/unity-cli/release-notes) · [Pipeline 0.10 changelog](https://docs.unity3d.com/Packages/com.unity.pipeline@0.10/changelog/CHANGELOG.html)
