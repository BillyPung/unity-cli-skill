# Unity CLI

**Bring your coding agent into Unity.**

Go from “what does this project need?” to a working Editor, a verified build, or a useful test report—without teaching your agent Unity's command-line workflow every time.

Unity CLI is a skill plugin for **Claude Code, Codex, and Oh My Pi**, with a portable skill for **OpenCode and other Agent Skills clients**. It helps your agent use the standalone Unity CLI and Unity Pipeline with the right project, version, and verification steps.

[Install](#install) · [Update](#update) · [Try it](#try-it) · [Changelog](CHANGELOG.md)

## What you can do

- **Get a project ready.** Find its Editor version, inspect modules, and prepare the setup it needs.
- **Work with the open Editor.** Inspect scenes and assets, use registered Pipeline commands, and verify saved changes.
- **Build with context.** Select the target or build profile, check requirements, and verify the output.
- **Make tests useful.** Run the relevant suite, read its report, and distinguish failing tests from a failed test run.
- **Keep the team in sync.** Install once through your agent's marketplace and receive versioned skill updates.

This plugin supplies instructions and reference material. Install [Unity CLI](https://docs.unity.com/en-us/unity-cli/use-unity-cli) separately. Live Editor control also needs Unity 6+ and the project's Pipeline package. Community maintained; not affiliated with Unity Technologies.

## Install

### Claude Code

Run inside Claude Code:

```text
/plugin marketplace add BillyPung/unity-cli-skill
/plugin install unity-cli@unity-cli-skills
```

Start a new session, then invoke `/unity-cli:unity-cli` or ask Claude to use the Unity CLI skill.

### Codex / ChatGPT desktop

In the plugin browser, choose **Add plugin marketplace** and enter:

```text
https://github.com/BillyPung/unity-cli-skill
```

Select **Unity CLI Skills**, open **Unity CLI**, and install it. Start a new chat and select the installed plugin. Use the repository URL, not the raw marketplace JSON URL. Labels and repository-marketplace support can vary by client version and workspace policy.

For Codex CLI, run from your terminal:

```sh
codex plugin marketplace add BillyPung/unity-cli-skill
codex plugin add unity-cli@unity-cli-skills
```

This repository is an installable **Git-backed marketplace**. It has not been submitted to or approved for the universal public ChatGPT/Codex Plugins Directory. Adding this repository makes it available through its own marketplace source; it does not create a central directory listing.

### Oh My Pi (omp)

Run inside OMP:

```text
/marketplace add BillyPung/unity-cli-skill
/marketplace install unity-cli@unity-cli-skills
/reload-plugins
```

OMP reads the Claude-compatible catalog included here and discovers the portable plugin's skills.

### OpenCode and other Agent Skills clients

Using the [community skills CLI](https://github.com/vercel-labs/skills), with Node.js 22.20+:

```sh
npx skills add BillyPung/unity-cli-skill --skill unity-cli -a opencode -g
```

Omit `-a opencode` to select another supported client interactively. Omit `-g` for a project install. This installs the portable skill rather than a Claude/Codex plugin. The [Agent Skills standard](https://agentskills.io/specification) defines the skill format; each client controls discovery and installation.

## Update

Use the same manager you installed with:

| Client | Update |
| --- | --- |
| Claude Code | `/plugin marketplace update unity-cli-skills`, then `/plugin update unity-cli@unity-cli-skills` |
| Codex desktop | Refresh the **Unity CLI Skills** marketplace in the plugin browser and apply the plugin update when offered. |
| Codex CLI | `codex plugin marketplace upgrade unity-cli-skills`, then `codex plugin add unity-cli@unity-cli-skills` |
| OMP | `/marketplace update unity-cli-skills`, then `/marketplace upgrade unity-cli@unity-cli-skills`, then `/reload-plugins` |
| Skills CLI | `npx skills update unity-cli` |

Start a new chat/session if your client still shows the old version. These steps update this skill plugin; Editor, CLI and Pipeline upgrades remain separate decisions.

**Send coworkers this:**

> Install Unity CLI from the marketplace at https://github.com/BillyPung/unity-cli-skill. The README has native install and update commands for Claude Code, Codex and OMP, plus an OpenCode skill option.

## Try it

> Inspect this Unity project and tell me which Editor and modules it needs. Make no changes yet.

> Run the Edit Mode tests and explain the failures using the test report.

> Connect to this project's open Editor, inspect the scene, and check the console for errors.

The skill discovers the commands exposed by your installed versions. Its guidance was reviewed on **2026-10-28** against **Unity CLI 1.0.0-beta.14** help and **Pipeline 0.9.1-exp.1** documentation. Older versions need command discovery; a newer plugin version does not require upgrading your project.

## Already installed a loose skill?

If you used the earlier file-copy installer, preserve any customizations, then remove or disable that loose `unity-cli` copy after installing the marketplace plugin. Otherwise your client may show two skills or keep selecting stale instructions. See [manual skill locations](docs/manual-skills.md) to locate it. Marketplace plugins should be updated through their manager, not by editing cache files or running the old Python installer.

## Package layout

One skill source, multiple native entry points:

```text
plugin.json                         Portable Agent Plugins package
.claude-plugin/plugin.json          Claude Code plugin
.claude-plugin/marketplace.json     Claude Code / OMP marketplace
.codex-plugin/plugin.json           Codex compatibility manifest
.agents/plugins/marketplace.json    Codex marketplace
skills/unity-cli/                   Shared skill and references
```

For maintenance, keep versions synchronized across manifests, catalogs, `VERSION`, and skill metadata. Existing installer files remain for older checkouts; marketplace installation needs neither Python nor a manual clone.

## References

[Unity CLI](https://docs.unity.com/en-us/unity-cli/unity-cli-reference) · [Pipeline](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/index.html) · [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) · [OMP marketplaces](https://github.com/can1357/oh-my-pi/blob/main/docs/marketplace.md)

MIT licensed. Unity binaries and third-party documentation are not bundled.
