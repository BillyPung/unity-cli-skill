# Unity CLI Skill

A portable [Agent Skills](https://agentskills.io/specification) package for Unity CLI and Unity Pipeline automation. Works with Claude Code, Codex, OpenCode, and **Oh My Pi (omp)**. Community-maintained; not an official Unity product.

The skill covers Editor/module management, projects, builds, tests, CI and live Editor/Player control. Its guidance was checked on **2026-10-28**, using local **Unity CLI 1.0.0-beta.14** help and official **Pipeline 0.9.1-exp.1** documentation. Older versions need live command discovery. This release includes the corrections listed in [CHANGELOG.md](CHANGELOG.md).

## Quick install

Prerequisites: Git and Python 3.9+ (`python`, `python3`, or `py -3` as available). Unity CLI must be installed separately using [Unity's instructions](https://docs.unity.com/en-us/unity-cli/use-unity-cli).

```sh
git clone https://github.com/BillyPung/unity-cli-skill.git
cd unity-cli-skill
python scripts/install.py --client codex
```

Replace `codex` with `claude`, `opencode`, `omp`, or `generic`. Commands work in PowerShell, Bash and zsh; substitute your Python launcher if necessary. To install for several clients, run the installer once for each. It copies only the portable skill folder, not this entire repository.

The installer replaces the selected skill directory and **preserves the previous directory in a timestamped backup outside the client's skills discovery root**. This includes local customizations. Backups are never automatically deleted. It prints both paths. Use `--dry-run` to preview before changing files. Linked destination paths are refused; use the manual method if you intentionally manage symlinks.

## Update in seconds

From the original checkout, run these commands in order. Stop if `git pull` fails:

```sh
git pull --ff-only
python scripts/install.py --client codex
```

Use the same client and scope as your installation. Repeat the installer for other client copies. Do not merge an update into a locally modified checkout blindly: keep local adaptations on a branch. Installation does not update Unity CLI, Editors or Pipeline packages.

**Message to send coworkers:**

> Please update from https://github.com/BillyPung/unity-cli-skill: run `git pull --ff-only` in your checkout, then `python scripts/install.py --client YOUR_CLIENT`. Supported clients: `claude`, `codex`, `opencode`, `omp`. Start a fresh agent session if the update is not detected.

For a pinned team version, use `git checkout v1.0.0` before installation. To return to current development: `git switch main`, then pull and reinstall. Private repositories require GitHub access and a working Git credential helper or SSH; never put a token into the clone URL.

## Supported locations

| Client option | User installation | With `--project /path/to/project` |
| --- | --- | --- |
| `generic` | `~/.agents/skills/unity-cli` | `.agents/skills/unity-cli` |
| `codex` | `~/.agents/skills/unity-cli` | `.agents/skills/unity-cli` |
| `claude` | `~/.claude/skills/unity-cli` | `.claude/skills/unity-cli` |
| `opencode` | `~/.config/opencode/skills/unity-cli` | `.opencode/skills/unity-cli` |
| `omp` | `~/.omp/agent/skills/unity-cli` | `.omp/skills/unity-cli` |
| `codex-legacy` | `$CODEX_HOME/skills/unity-cli`, default `~/.codex/skills/unity-cli` | `.codex/skills/unity-cli` |

`~` means your user home; Windows examples resolve under your user profile. Current Codex documentation uses `.agents/skills`; `codex-legacy` is provided for installations still using the older path, not as the recommended path for new clients. Avoid keeping stale same-named copies in both locations.

The global installer honors `CLAUDE_CONFIG_DIR`, `XDG_CONFIG_HOME`, and `CODEX_HOME` for their corresponding options. For OMP profiles, custom configuration roots, or another Agent Skills host, specify its exact supported destination:

```sh
python scripts/install.py --destination /custom/skills/unity-cli
python scripts/install.py --client claude --project /path/to/your/unity-project
```

OMP profile example: `--destination ~/.omp/profiles/PROFILE/agent/skills/unity-cli`. In PowerShell use `--destination "$HOME/.omp/profiles/PROFILE/agent/skills/unity-cli"`. OMP's foreign user providers can be opt-in, so its native `omp` destination is the reliable default.

The Agent Skills specification defines the folder format, **not a universal installation directory**. `generic` uses the common `.agents/skills` convention; verify discovery rules for any other host. All clients receive the same `SKILL.md` and references with no host-specific permission grants.

## Manual installation (no Python)

Copy the whole `skills/unity-cli` directory into one location from the table, keeping `SKILL.md` directly inside `unity-cli`. Preserve any old copy elsewhere before replacing it. Include `references/`; copying only `SKILL.md` breaks its links. For updates, pull the repository, then replace the complete installed folder. A reviewed symlink to the source folder is another option on hosts that support it; then a successful pull updates that link's content directly.

## Verify and use

Start a fresh session if your client does not detect changed skills. Ask: **"Use the unity-cli skill to inspect my Unity CLI version and available commands without modifying my project."**

- Claude Code: `/unity-cli`.
- Codex: `$unity-cli`, or select it from `/skills` where available.
- OpenCode: ask the agent to load the `unity-cli` skill through its skill tool.
- OMP: `/skill:unity-cli` when skill commands are enabled.

Each installed copy has `.unity-cli-install.json` with its package version and Git commit (null for a ZIP without Git metadata). Verify with `unity --version` separately. A portable file install does not bypass host workspace trust or tool permissions.

If discovery fails, check the folder depth, whether skills are enabled, and duplicate copies in project/user/plugin locations. An older skill installed by `unity skill install` can shadow this one; choose which source you maintain. Do not use `unity skill refresh` to update this repository's skill.

## Rollback or uninstall

To roll back, move the current `unity-cli` folder aside, then move the printed backup directory back to the original destination. For a repository release rollback, check out the earlier tag and reinstall. To uninstall, remove only the installed `unity-cli` folder; preserve backups you still need. No Unity installation, project, account, or license is changed by this installer.

## Maintaining this package

Edit the single source at `skills/unity-cli/`, update `VERSION`, frontmatter version and changelog, then run:

```sh
python -m unittest discover -s tests -v
```

Review local CLI help and official package documentation before adding commands. Add a tag for a reviewed release. The GitHub workflow runs installer tests on Windows, macOS and Linux. Documentation checks are a baseline; Pipeline behavior still needs validation in a matching Editor/project.

## Sources

- [Agent Skills format](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills)
- [OpenCode skills](https://docs.opencode.ai/docs/skills/)
- [OMP skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md) and [configuration/profiles](https://github.com/can1357/oh-my-pi/blob/main/docs/config-usage.md)
- [Unity CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference) and [release notes](https://docs.unity.com/en-us/unity-cli/release-notes)
- [Pipeline command index](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/index.html)

Documentation is summarized in original guidance; Unity binaries and third-party manuals are not bundled. MIT license applies to this repository's authored files.
