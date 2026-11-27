# Versions, installation and updates

## Checked state on 2026-11-27

| Component | Latest found | Evidence and limits |
| --- | --- | --- |
| Unity CLI | `1.1.0` | Local CLI reports 1.0.0. The live update feed confirms 1.1.0, and `unity changelog --target 1.1.0` documents its changes. |
| `com.unity.pipeline` | `1.0.1` | Live registry and 1.0 changelog agree. The patch updates Auto Tick for background Editor callbacks. Live Editor/Player validation is pending. |
| Unity Editor | Unity 6+ for Pipeline | Read `ProjectSettings/ProjectVersion.txt` and check package requirements. CLI 1.1 blocks package setup on Unity 6000.5.0 through 6000.5.2. |

This snapshot is not a permanent latest-version claim or a promise that all combinations work. The skill/plugin version in `VERSION` is a separate release track.

## Read-only checks

1. Resolve the executable with `Get-Command unity` (PowerShell) or `command -v unity` (POSIX). If missing after installation, reopen the terminal/check PATH before installing again. Check for competing install methods.
2. Run `unity --version` and the needed command's `--help`. Check the live feed with `unity self-update --check --format json`. Inspect `data.currentVersion`, `data.latestVersion`, envelope success and exit status; fields can change in other releases.
3. Run `unity pipeline list-versions --format json`. Read the registry's latest and available versions. In the project, inspect `Packages/manifest.json` for the requested source/version and `Packages/packages-lock.json` for the resolved entry. A range, Git URL or local path is not a resolved registry release. If necessary inspect that package's own `package.json`; do not infer it from the port descriptor.
4. Compare versions with SemVer. For example, stable CLI `1.0.0` follows `1.0.0-beta.17`, and stable Pipeline `1.0.0` follows `1.0.0-pre.1` and `0.10.0-exp.1`. Preserve deliberate team pins and check the features needed by the task. A stable package label does not make every workflow stable: Runtime Pipeline remains experimental in 1.0.
5. Discover the running package's command schema and confirm the exact target with `unity status --project-path <absolute-project> --format json`. A current package can still be unavailable because it has not compiled/loaded.

Report installed, requested/resolved and latest available versions with the check date and CLI update channel. Report freshness as unknown when a feed fails. Use `unity changelog --target <version>` for version-specific CLI changes, especially when the public release-notes index trails the feed. For Pipeline changes check the registry, then open the matching versioned manual and changelog. The `@latest` redirect points to the 1.0 manual, which covers patch 1.0.1. Check existing prerelease pins against the project's version policy before changing them.

## Install Unity CLI

When the requested setup includes CLI installation, choose one existing/appropriate official channel and carry it through verification. Do not require the user to repeat authorization already given.

The install guide lists Windows 10 21H1+ and macOS 14+. The CLI 1.1.0 changelog lowers the Linux minimum to glibc 2.31 and restores CLI support for Ubuntu 20.04 and Debian 11. Older releases such as 1.0.0 require glibc 2.34. Check Editor and module requirements separately. CLI 1.1 `.deb` and `.rpm` packages include Bash, Zsh and Fish completion scripts.

| Environment | Install | Update through the same manager |
| --- | --- | --- |
| Windows with winget | `winget install Unity.CLI` | `winget upgrade Unity.CLI` |
| Homebrew | `brew install --cask unity-cli` | `brew upgrade unity-cli` |
| Unity's configured Debian/Ubuntu repository | `sudo apt install unity-cli` | Refresh package indexes, then `sudo apt upgrade unity-cli` |
| Unity's configured Fedora/RHEL repository | `sudo dnf install unity-cli` | `sudo dnf upgrade unity-cli` |

For Linux repository registration or systems without those managers, follow the current [official installation page](https://docs.unity.com/en-us/unity-cli/use-unity-cli), including OS requirements. Do not invent repository/bootstrap commands from memory. This dependency setup is separate from marketplace installation of this skill; it does not require this repository's Python installer.

Winget now distributes stable CLI releases only. Inspect `self-update --help` and the existing stable/beta channel policy before changing channels. Linux repository suites also distinguish `stable` from `unstable`; do not silently replace a team's configured suite to resolve an unavailable version. For direct release downloads, verify the checksum and, when required by the workflow, the Unity signature over `SHA256SUMS` (`SHA256SUMS.asc`) using Unity's published key.

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

The last mutating step requires update scope. In CLI 1.0, `self-update --target <version>` pins that version against Unity Hub replacement. An unpinned `self-update` returns to newest-release tracking and permits Hub updates again; use it only when that is the user's policy. Homebrew and Linux repository installations should be updated through their manager; winget/MSIX also supports self-update. Do not install a second competing copy to bypass ownership or update errors.

Inspect the update result's `installed`, `installedVersion` when supplied (not for MSIX), and `appliesAfterExit`. Re-resolve `unity --version` after the update process exits, rather than treating a scheduled replacement or a no-op as an installed target. Re-read command help after updating. MSIX can update in the background and has no rollback; other install types also need their own rollback check. An offline check never proves a pin is current.

Prefer explicit JSON for version checks and dry runs across versions. With 1.0.1, TSV checks and dry runs use key/value rows, and NDJSON emits one result frame with the JSON fields. Review older scripts that parse the previous output layout.

## Install or update Pipeline in the intended project

Require a compatible Editor and a recoverable source-control state. Read `pipeline install --help` and `pipeline upgrade --help`. The local CLI 1.0 uses `--version`. Some older binaries used `--package-version`. Preserve existing Git and local dependencies unless the requested change includes replacing their source.

CLI 1.1 refuses Pipeline install or upgrade on Unity 6000.5.0 through 6000.5.2 with exit 6 and `PIPELINE_EDITOR_UNSUPPORTED` before changing the manifest. Pipeline cannot start on those releases. Check the project pin and plan an Editor update to 6000.5.3f1 or later on that release line when authorized. CLI 1.1 accepts `--force` for both commands, but the flag only bypasses the check.

CLI 1.1 Pipeline install and upgrade can also install or update Unity's official `unity-pipeline` agent skill for the invoking agent and clients that already have a Unity skill. Edited copies are preserved. For a package-only request, add `--no-skill` after confirming it in help. On CLI 1.0, omit that flag. Update this repository's skill through its own marketplace.

Before a 0.x → 1.0 upgrade, review the [migration changes](pipeline-package.md#pipeline-10-migration): removed aliases/parameter spellings, direct eval values, and changed Pipeline test results/exit codes. Update dependent scripts as part of the authorized migration. An older CLI that sends removed keys can fail with `INVALID_COMMAND_ARGS`; check its version and help rather than silently downgrading the project.

CLI 1.0 includes compatibility fixes for Pipeline 1.0 builds, `recompile --strict`, `logs --console --follow` and Project Auditor. Check the client version first when beta.17 automation fails after a Pipeline upgrade; do not weaken strict validation or change the package pin as a workaround.

```sh
unity pipeline list-versions --format json
unity pipeline install --project-path <absolute-project> --version <agreed-package-version> --no-skill
```

For an existing registry package, verify the latest release suits the project before running the package-only update on CLI 1.1.

```sh
unity pipeline upgrade --project-path <absolute-project> --no-skill
```

CLI 1.0.1 can fall back to a running Editor when the shell's working directory was deleted. Keep the absolute `--project-path` on install and upgrade so discovery does not choose another project.

To deliberately select a specific available version, use the explicit install pin after reviewing help; it overwrites an existing package version. `--force` is not needed as a routine update shortcut. Do not assume Pipeline offers `--dry-run`; use only flags in installed help.

Allow UPM resolution, refresh and compilation to finish. Re-read the manifest/lock, inspect their diff, then verify `pipeline list`, target `status --until-ready` with a bounded timeout, and live command discovery. Import/compile failures are not success. If no Editor can be started within scope, report that files were updated but live validation is pending. See [Pipeline recovery and runtime guidance](pipeline-package.md).

[Official CLI install and update guidance](https://docs.unity.com/en-us/unity-cli/use-unity-cli) · [CLI 1.1.0 changelog](https://public-cdn.cloud.unity3d.com/hub/prod/cli/1.1.0/CHANGELOG.md) · [Pipeline 1.0 changelog](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/changelog/CHANGELOG.html)
