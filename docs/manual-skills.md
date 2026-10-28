# Loose skill locations

For clients without a marketplace, copy the complete `skills/unity-cli/` folder to their skill directory. Keep its `references/` folder. The Agent Skills format does not prescribe a universal installation path.

| Host | User skill folder | Project skill folder |
| --- | --- | --- |
| Codex | `~/.agents/skills/unity-cli` | `.agents/skills/unity-cli` |
| Older Codex setups | `~/.codex/skills/unity-cli` | `.codex/skills/unity-cli` |
| Claude Code | `~/.claude/skills/unity-cli` | `.claude/skills/unity-cli` |
| OpenCode | `~/.config/opencode/skills/unity-cli` | `.opencode/skills/unity-cli` or `.agents/skills/unity-cli` |
| OMP | `~/.omp/agent/skills/unity-cli` | `.omp/skills/unity-cli` |

Back up customizations before replacing or removing a loose copy. For OMP profiles and configured roots, consult the host's discovery documentation. Prefer the native marketplace flows in the [README](../README.md) where available.
