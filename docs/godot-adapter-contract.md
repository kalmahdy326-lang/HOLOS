# HOLOS Godot Adapter Contract

**Project author:** Khaled AL-MAHDY  
**Status:** Initial adapter implementation; not yet executed against a real character project.

## Responsibility boundary

Python owns production orchestration: configuration validation, asset checks, shot scheduling, subprocess execution, output accounting, recovery, and reporting.

Godot owns scene loading, character animation, scene composition, deterministic frame stepping, and frame capture.

FFmpeg owns media assembly and encoding after frames have been validated.

## Runner

The generic runner is:

`godot/holos_shot_runner.gd`

It is intended to be invoked by Godot 4.x in headless mode:

```bash
godot --headless --path path/to/godot/project \
  --script res://path/to/holos_shot_runner.gd -- \
  --config path/to/shot.json --output path/to/output/shot
```

The runner expects a JSON object with:

```json
{
  "scene": "res://scenes/shot_scene.tscn",
  "start_frame": 0,
  "end_frame": 240,
  "fps": 24,
  "width": 1280,
  "height": 720,
  "shot_id": "S01_B01",
  "mode": "production"
}
```

Frame range is half-open: `start_frame <= frame < end_frame`.

Output names are zero-based within the shot: `frame_000000.png`, `frame_000001.png`, and so on.

## Scene integration hooks

A shot scene root may implement these optional methods:

- `holos_apply_shot(config: Dictionary)`: apply shot-level state before frame stepping.
- `holos_set_frame(frame_index: int, fps: float)`: place the scene at the requested absolute frame.

For reproducible rendering, `holos_set_frame` should set animation state from the supplied frame rather than depend on accumulated wall-clock delta. Existing rigs can be adapted incrementally; the runner does not require rewriting their internal rig logic.

## Python adapter

`holos_engine/godot_adapter.py` builds the headless command, runs Godot, captures process output, enforces a timeout, and verifies the expected number of PNG frames.

The caller must supply a shot JSON file and a safe output directory. The adapter does not overwrite or clear an existing output directory.

## Important current limitations

- The runner has not yet been executed against the actual Khaled or Kevin Godot projects.
- No claim is made that the current Godot runner is compatible with their scene structures until tested.
- The two scene hooks are an integration contract, not evidence that existing rigs already implement them.
- The current runner captures the root viewport; exact headless viewport behavior must be verified on the target Godot version.
- Audio is deliberately outside the Godot adapter. Dialogue and music remain external source assets and are assembled later by FFmpeg.
- Production/debug policy enforcement and render-manifest integration remain controller responsibilities.

## Acceptance checks for this adapter

1. Godot 4.x loads the runner in headless mode.
2. A minimal test scene renders a known number of PNG frames.
3. Frame dimensions match the requested resolution.
4. Frame numbering is contiguous and zero-based.
5. Invalid scene paths, frame ranges, and output paths fail clearly.
6. The same test configuration can be rendered twice without changing source assets.
7. A later integration test confirms the Khaled and Kevin rigs through their own scenes and hook implementations.
