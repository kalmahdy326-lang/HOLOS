# HOLOS — Milestone 6 Production Engine: Implementation Reference

**Project author:** Khaled AL-MAHDY  
**Scope:** Describe the current Python → Godot → PNG → FFmpeg/FFprobe implementation and separate verified code behavior from outstanding production integration.  
**Status:** Source-code inspection reference; not a claim of target-machine acceptance.

## 1. Architecture at a glance

```text
Episode JSON
    |
    v
tools/holos.py
    |-- holos_engine.config       parse and validate v1 config
    |-- holos_engine.preflight    check referenced source assets
    |-- holos_engine.batch        order, resume, hash, archive shot output
    |-- holos_engine.godot_adapter
    |       |
    |       v
    |    Godot 4.x process
    |       |
    |       v
    |    holos_shot_runner.gd --> configured PackedScene
    |                               | holos_apply_shot(config)
    |                               | holos_set_frame(frame, fps)
    |                               v
    |                         frame_000000.png ...
    |
    v
Verified shot manifest
    |
    v
holos_engine.episode_assembly --> ordered staging directory
    |
    v
FFmpeg --> temporary MP4 --> FFprobe --> validation
    |
    v
Publish final output only after validation
```

Responsibilities are intentionally separated:
- Python owns orchestration, configuration, paths, job order, retries/recovery, checksums, reports and process exit status.
- Godot owns scene loading, deterministic frame stepping and viewport capture.
- FFmpeg owns encoding and audio mapping.
- FFprobe supplies stream/container metadata for validation.
- Git tracks source code and text configuration; large media requires an explicit storage policy.

## 2. Python-to-Godot communication: what exists today

The CLI builds a per-shot JSON file under `output/.holos_runtime/`, then invokes Godot as a subprocess through `holos_engine.godot_adapter.render_shot()`.

The invocation passes:
- Godot executable;
- project path;
- runner script `res://holos_shot_runner.gd`;
- temporary shot-config path;
- fresh output directory.

The adapter uses `subprocess.run(capture_output=True, text=True, timeout=...)`. It waits for the process to finish, then inspects its return code and expected frame filenames. On failure it raises an exception with the last portion of stderr/stdout. On success it returns the command, return code, frame count, first/last frame and captured stdout/stderr.

The Godot runner emits a final line in the form `HOLOS_RENDER_COMPLETE frames=N output=...` and exits with code 0. Errors use `push_error` and a non-zero quit code.

**Important current limitation:** the present adapter captures process output after completion. It does not currently stream live per-frame progress events to the Python terminal or a UI. The batch manifest does persist status at shot boundaries. Do not describe the existing implementation as having live frame-by-frame progress reporting.

### Recommended next improvement (not yet implemented)

Introduce a versioned line-delimited JSON event protocol on stdout:
- `shot_started`
- `frame_completed` with frame index and total
- `shot_completed`
- `shot_failed`

Each event should include `protocol_version`, `run_id`, `episode_id`, `scene_id`, `shot_id`, UTC timestamp and relevant counts. Keep human diagnostics on stderr. Python should parse events incrementally, validate event order, persist progress at safe checkpoints and tolerate a process dying between events. A final process exit code remains authoritative; a printed completion event alone must never mark a shot complete.

Do not add this protocol without tests for malformed JSON, missing events, duplicate events, process termination and stdout noise.

## 3. Shot hook contract

The generic Godot runner loads the configured `res://` PackedScene and instantiates its root node.

Optional root methods:
```gdscript
func holos_apply_shot(config: Dictionary) -> void:
    pass

func holos_set_frame(frame_index: int, fps: float) -> void:
    pass
```

- `holos_apply_shot` is called once before the frame loop.
- `holos_set_frame` is called for each configured frame in ascending order.
- The frame index is the configured half-open episode frame number.
- The first PNG in each shot is still named `frame_000000.png`.
- The runner waits two process frames after the hook call before capture.
- A scene must set complete state for a requested frame. It must not rely on wall-clock elapsed time or previous-frame accumulation if deterministic rerendering is required.

This generic contract is not itself a character rig adapter. It does not define a particular rig's AnimationPlayer, skeleton, blend tree, face layers or mouth-shape controls.

## 4. Resumable batch manifest

The current batch renderer writes:
`output/manifests/<episode_id>-<mode>-render.json`

Manifest top-level fields observed in code:
- `schema_version` (currently 1)
- `episode_id`
- `mode` (`debug` or `production`)
- `episode_config_sha256`
- `created_at`
- `updated_at`
- `shots`

Each shot record contains:
- `scene_id`, `shot_id`
- `start_frame`, `end_frame`
- `expected_frame_count`
- `output_dir`
- `status`: pending, running, failed or completed
- `error` and cumulative `errors`
- `attempts`
- compact `result` (return code, frame count, first/last frame)
- `frame_integrity`: ordered frame name, byte size and SHA-256 records
- `recovered_outputs`: prior incomplete output directories archived before retry

The episode configuration is canonicalized with sorted JSON keys and compact separators before hashing. A manifest is rejected if the config digest, mode, schema version, shot count/order or expected frame count differs.

Before a shot attempt, the manifest is persisted with status `running`. If an output directory already exists but is not a verified completion, it is moved into a unique `output/recovery/` directory; it is not deleted. After rendering, the controller requires the exact expected sequence of non-empty PNG files, hashes every frame, then persists `completed`. The manifest is written through a temporary file, flushed/fsynced and atomically replaced.

On restart, a shot is skipped only when status is completed and the actual frame list and hashes match the manifest. A stale or partial directory is archived and rerendered.

**Recovery boundary:** this is shot-level resume, not arbitrary in-shot frame resume. A crash during a shot can cause that shot to be rerendered from its first frame. Previously completed, hash-verified shots are retained.

## 5. FFmpeg and FFprobe validation

The assembly path checks that all expected numbered PNG files exist, refuses to overwrite an existing MP4, invokes FFmpeg with explicit frame rate, frame count, duration, CFR mode, H.264/libx264, yuv420p and fast-start flags. Audio is optional; with no audio inputs the command explicitly uses `-an`.

FFprobe is invoked with `-show_streams -show_format -of json`. The current validator checks:
- presence of a video stream;
- video width and height;
- average frame rate (or fallback real frame rate);
- container/format duration against expected duration and tolerance;
- audio presence when audio is required;
- video and audio stream start times when audio is required;
- video and audio stream durations when audio is required;
- A/V start offset and stream-duration difference against the configured sync tolerance.

The default A/V tolerance is 80 ms.

### Validation gaps to close before calling the engine production-grade

The current `validate_media` function does **not** explicitly validate:
- video codec name;
- pixel format;
- decoded frame count;
- audio codec, sample rate, channel count or loudness/true peak;
- black-frame/frozen-frame content;
- visual correctness or continuity;
- subtitle/data stream policy;
- full-file decode success (this needs a separate FFmpeg decode pass).

FFmpeg currently requests libx264/yuv420p, but a requested encoder setting is not the same as a validator assertion. Add explicit checks and tests before claiming those properties are automatically enforced.

For a silent review output, call validation with `require_audio=False`; an absent audio stream is then expected, not an error.

## 6. Debug overlay isolation

The Godot runner creates its diagnostic CanvasLayer only if both conditions are true:
1. `mode == "debug"`;
2. `debug_overlay == true`.

The Python shot configuration sets `debug_overlay` only when the CLI mode is debug and the episode render setting enables it. The overlay displays shot ID and frame number. In production mode the setup function returns without creating the layer.

The project has previously documented image-comparison verification of debug and production renders. Repeat that test after changes to the runner. Do not rely on a config flag inspection alone.

## 7. Error and fallback policy

- Missing executable: fail with a clear dependency error; do not download a binary automatically.
- Godot non-zero exit or timeout: mark the shot failed, preserve logs, retain/archive partial frames and do not mark completion.
- Wrong or missing frame sequence: fail the shot.
- Manifest/config mismatch: stop and require a new run identity or an explicit migration; never silently reinterpret old output.
- FFmpeg failure: do not publish the final output.
- FFprobe validation failure: retain the temporary failed output/log for diagnosis, but do not publish it as final.
- Disk full or permission failure: stop safely, preserve already completed shots and report remaining free-space requirements.
- Toolchain unavailable offline: mark the workflow blocked; never silently switch to cloud rendering or an unapproved external service.

## 8. Source inspection basis

This reference was prepared from the following files on branch `docs/holos-artwork-production-specs`:
- `tools/holos.py` — blob `f355c68f6b27da0f12a8463dbcbd9627193b6cd6`
- `holos_engine/batch.py` — blob `9fa5f520c701788b743a3f370104dd9358d67f7d`
- `holos_engine/godot_adapter.py` — blob `b7c5ab7ee6650084a7b56012c35478639da1d1d0`
- `holos_engine/media.py` — blob `51532035e7213113e662cfec3e58118c0dfed505`
- `holos_engine/config.py` — blob `d402a11472a53678efdce43bcafc27fcef223a9b`
- `godot/holos_shot_runner.gd` — blob `33e97a63639178f29362097301bbd8bd69127e23`

A source inspection is not a test run. The target production-machine offline test remains a separate required gate.
