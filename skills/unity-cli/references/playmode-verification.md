# Verify a running game

Discover the connected schema first. The guidance below targets Pipeline 1.0. Pin the project on every invocation.

1. Record whether the Editor was already playing or paused. Preserve a user-owned session; do not stop or change its pacing as incidental validation.
2. For a session you start, inspect background settings. In 1.0 `editor.playmode start` and `start_scenario` turn Run In Background on until Play mode exits, then restore the project's value. `--run-in-background false` preserves the project's setting. `editor set_auto_tick` keeps Editor command/compile/test handling responsive but does not itself keep an unfocused game advancing. Restore any additional temporary overrides you make.
3. Start using `editor.playmode start`, then use `unity status --project-path <project> --until-ready` through the domain reload. Fix compile errors before retrying a refused start. Use `start_scenario` for an orchestrated multiplayer session; it enters Play mode itself.
4. Prove advancement with `editor status`'s `frameCount` and `playerLoopTicking`, a condition wait on `UnityEngine.Time.frameCount`, or equivalent schema-supported observations. `runInBackground` reports the setting; it does not prove the player loop is advancing. Merely reporting Play mode and returning a screenshot can describe a frozen game.
5. Capture with `capture game_view`; specify `source=screen` for composited overlay UI or `source=camera` for an offscreen camera render. Save to a path to avoid huge inline images. Inspect actual output, including suspicious blank/solid images and locked-desktop limitations.
6. Read errors/exceptions with `console get` and use `console status` for cheap counters. Verify the expected gameplay/UI state, not just absence of log errors.
7. Stop only the session you started, and restore temporary settings.

Use `--` before Pipeline flags to distinguish them from CLI flags. Long condition waits should use the package's async wait and wait-status/cancel commands rather than blocking work needed to satisfy the condition. This is separate from CLI detached jobs.

Pipeline 1.0 removes `capture screenshot`. Use `capture game_view` or `capture scene_view` with `output-path`, not the old `save_path` spelling. Relative paths resolve from the project root. Absolute paths are accepted and `savedPath` is absolute. Setting `output-path` returns a path without inline base64; use `include-inline-image=true` only when both are needed. Recheck destinations when migrating a script that expected paths relative to `Assets/`.

```sh
unity command --project-path <absolute-project> capture game_view -- --source screen --output-path Screenshots/verification.png
```

For the Scene view, `source=camera` renders its camera and `source=screen` captures the window as drawn. Use `capture editor_window` when the task calls for a specific open Editor window.

`capture game_view` can open a Game view on demand, including in batch mode. If a newly opened view lacks a frame, wait for rendering and retry an explicit `source=screen` request. When `source` is omitted it can fall back to a camera; read stderr warnings for that fallback and for a Play-mode view that has no new frame. A screen capture can hold the previous frame when Run In Background is off. In URP and HDRP, the camera capture's `overlay` setting can include Screen Space - Overlay UI. Check the installed schema and the returned image. [Pipeline 1.0 capture guide](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/capture.html)

[Editor observability](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/editor-lifecycle-and-observability.html), [waits](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/wait.html), [capture](https://docs.unity3d.com/Packages/com.unity.pipeline@1.0/manual/commands/capture.html). For a binary-matched recipe read `unity skill show --path references/playmode-verification-loop.md`, then check it against the project's package schema.
