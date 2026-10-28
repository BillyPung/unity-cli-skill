# Verify a running game

Discover the connected schema first. These names follow Pipeline 0.9; older packages differ. Pin the project on every invocation.

1. Record whether the Editor was already playing or paused. Preserve a user-owned session; do not stop or change its pacing as incidental validation.
2. For a session you start, inspect background settings. `editor set_auto_tick` and `editor.playmode set_run_in_background` can keep an unfocused game advancing. Restore temporary changes after verification.
3. Start using `editor.playmode start`, then use `unity status --project-path <project> --until-ready` through the domain reload.
4. Prove advancement with `job wait` on `UnityEngine.Time.frameCount` and `op: changed`, or equivalent schema-supported observations. Merely reporting Play mode and returning a screenshot can describe a frozen game.
5. Capture with `capture game_view`; specify `source=screen` for composited overlay UI or `source=camera` for an offscreen camera render. Save to a path to avoid huge inline images. Inspect actual output, including suspicious blank/solid images and locked-desktop limitations.
6. Read errors/exceptions with `console get` and use `console status` for cheap counters. Verify the expected gameplay/UI state, not just absence of log errors.
7. Stop only the session you started, and restore temporary settings.

Use `--` before Pipeline flags to distinguish them from CLI flags. Long condition waits should use the package's async wait and wait-status/cancel commands rather than blocking work needed to satisfy the condition. This is separate from CLI detached jobs.

[Editor observability](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/commands/editor-lifecycle-and-observability.html), [waits](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/commands/wait.html), [capture](https://docs.unity3d.com/Packages/com.unity.pipeline@0.9/manual/commands/capture.html). For a binary-matched recipe read `unity skill show --path references/playmode-verification-loop.md`.
