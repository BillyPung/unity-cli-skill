# MCP, command discovery and Unity tools

CLI 1.0 adds live help, catalog discovery and smaller MCP catalogs. Read local help and discover the intended Editor before choosing a route. Ordinary terminal workflows can continue through `unity command`; an MCP configuration is not a prerequisite for this skill.

## Discover commands

```sh
unity commands --include-editor --format json
unity command --project-path <absolute-project> editor
unity command --project-path <absolute-project> editor status --help
```

`commands --include-editor` adds connected commands with `source: editor` and waits briefly for the connection. The first example uses auto-discovery; run it from the intended project directory and verify which Editor supplied the catalog. Use explicit `--project-path` with `unity command` for subsequent help and execution. A disconnected or uncompiled package is not an empty feature set. A group lists its commands; full command help reads parameters from the connected Editor.

CLI 1.0.1 adds the full `path` to each command in JSON and NDJSON catalogs. Read the field when present and account for its absence when supporting older versions.

`unity completion <shell>` prints the completion script for the chosen shell. CLI 1.0 completions can offer connected Editor commands and their parameters, including in `unity shell`. Regenerate an older script when completion setup is requested; review its installation destination rather than changing shell profiles during an unrelated task.

In CLI 1.0.1, run `unity completion <shell>` without a machine format when saving the raw script. JSON and NDJSON now wrap the output, with the shell and script in `data.shell` and `data.script`.

## MCP catalogs and filters

Inspect `unity mcp --help` and `unity mcp configure --help`. For an authorized MCP server session, a typical grouped launch is:

```sh
unity mcp --project-path <absolute-project> --tool-groups
```

This is a long-running server, not an inspection command. Each group tool takes `command` and `args`; consult its description and current schema. C# execution commands such as `script eval` and `exec` remain separate tools, so a group approval does not cover arbitrary code execution.

The server can exclude commands by `--exclude-annotations` (`read-only`, `destructive`, `idempotent`, `open-world`), by `--exclude-tool-groups` (for example `"scene,editor.*"`), or by `--exclude-tools`. These filters hide matching Editor commands and reject calls to them. Excluding an annotation is a deny filter, not an allow list; excluding `read-only` would remove reads. Match the requested access policy and inspect the resulting tools. Do not add filters incidentally or treat metadata as user authorization.

CLI 1.0.1 allows a whole MCP Editor group name, such as `editor_playmode`, in `--tools` or `--exclude-tools`. One entry then includes or excludes all commands in that group. An inclusion filter keeps the `unity-cli-status` tool for connection diagnostics. A matching exclusion also removes that tool and rejects calls to it, so review broad patterns such as `"*status*"`.

`mcp configure <client> --dry-run` previews a client configuration write. New CLI 1.0 entries use grouped tools. Rerunning configure over an older entry switches its tool names and can invalidate the client's existing allow list. Review that change and any project path, then apply only when client configuration is requested. `mcp configure` does not inherit `UNITY_PROJECT_PATH`; pass `--project-path` explicitly when configuring a fixed project. Verify the connected client after its reload.

CLI 1.1 exits 2 for an unsupported client or an unavailable `--local` configuration mode. Keep the project path explicit because auto-discovery can reuse the last project reached from a working folder. [Editor targeting and recovery](pipeline-package.md#editor-targeting-and-recovery-in-cli-11)

## Managed Unity CLI tools

`unity plugin install <id>` installs an executable Unity tool, including tools published after the current CLI. Inspect `plugin --help`, the tool identity and destination first. Managed tools come from Unity's CLI plugin CDN and are checksum-verified. `unity <id>` runs the installed tool. Separately, `unity-<name>` executables on PATH can extend dispatch; built-in commands win, and supported groups such as `cloud` can delegate an unknown subcommand to their group plugin. Check the executable's provenance before running it.

These executable tools differ from this repository's instruction-only marketplace plugin and Unity's own coding-agent plugin. Do not use `unity plugin install` to install this skill or replace it through `unity setup` as an incidental remediation. Use the host's [native marketplace update instructions](https://github.com/BillyPung/unity-cli-skill#update).

Command flags were checked with local 1.0.0 help. The 1.0.1 changes follow Unity's release notes. Live Editor/MCP client validation is pending. [CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference) · [CLI 1.0.1 release notes](https://docs.unity.com/en-us/unity-cli/release-notes/2026/november#1.0.1)
