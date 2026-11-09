# Milestone 6 — HOLOS Local Production Engine

**Project author:** Khaled AL-MAHDY  
**Status:** In progress. The local Python/Godot/FFmpeg engine, ordered resumable shot rendering, verified episode assembly, and stream-level A/V timing validation are implemented in the repository and covered by CI. Integration with the actual Khaled and Kevin rigs, production safeguards, and offline acceptance remain unverified.

## Objective

Integrate the existing Khaled and Kevin Godot character rigs and Python/FFmpeg tooling into one locally executable production system.

The production pipeline must operate offline. Manus may be used as optional development assistance, but it must never be a runtime dependency.

## Non-negotiable constraints

- Rendering, assembly, validation, and recovery must work without internet access.
- No paid software, subscriptions, AI credits, or external AI services without explicit authorization.
- Preserve source assets, dialogue, soundtrack, completed benchmarks, and existing project history.
- Back up before changes. Never overwrite or delete originals without explicit authorization and safeguards.
- Clearly distinguish prototype, validated component, and production-ready status.
- Do not claim offline acceptance until the test has actually been performed with the network disconnected.

## Architecture

| Component | Responsibility |
|---|---|
| Godot | Character rigs, animation, scenes, and frame rendering |
| Python | Production controller, configuration validation, asset resolution, shot scheduling, resumability, backups, logs, validation, and reports |
| FFmpeg / FFprobe | Media inspection, synchronization, encoding, and final assembly |
| JSON | Episode, scene, shot, dialogue, character-state, audio, and render configuration |
| Git | Version control and project history |

Avoid duplicated responsibilities across components.

## Existing work to preserve

- Khaled functional character rig and Milestone 3 benchmark.
- Kevin functional character rig and Milestone 4 benchmark.
- Existing two-character interaction prototype.
- Original dialogue, soundtrack, source artwork, scene plates, references, reports, and benchmark outputs.

Do not rebuild completed milestones unnecessarily. Do not relocate source assets until an inventory and backup exist.

## Current repository implementation status

| Capability | Evidence / boundary |
|---|---|
| Python CLI and versioned episode configuration | Implemented; configuration and CLI tests run in CI |
| Godot shot rendering | Implemented through the generic scene hook contract; real Godot offscreen render tests run in CI |
| Debug/production separation | Separate output trees; optional debug overlay is gated to debug mode and ignored in production; verified by comparing actual Godot PNGs |
| Ordered multi-shot rendering | Implemented with resumable manifest, per-frame SHA-256 integrity, attempt/error history, and recovery archival |
| Complete episode assembly | Implemented from verified per-shot folders; output is published only after FFprobe validation |
| Media validation | Resolution, frame rate, container duration, audio presence, audio/video start offset, and stream-duration difference checked |
| A/V tolerance | Configurable as \`audio.sync_tolerance_ms\`; default 80 ms |
| Existing character rigs | Not yet connected to the engine; the repository currently uses generic adapter fixtures |
| Offline acceptance on production machine | Not performed; CI is not a substitute for disconnected local acceptance |
| Source asset inventory and backup/restore | Not yet complete |

## Required capabilities

1. Central Python production controller.
2. Versioned JSON episode and shot schema with validation.
3. Integration of both existing Godot character rigs.
4. Reusable scene and animation configurations.
5. Individual shot rendering.
6. Batch scene and episode rendering.
7. FFmpeg audio/video assembly.
8. Preservation of original dialogue and soundtrack files.
9. Automated validation of resolution, frame rate, duration, frame count, missing assets, audio presence, A/V synchronization, and render completeness.
10. Production and debug modes; debug overlays must never appear in production output.
11. Versioned outputs, automated backups, manifests, and structured logs.
12. Git availability check and safe version-control integration without overwriting existing history.
13. Installation, offline operation, recovery, restore, and troubleshooting documentation.
14. An actual offline acceptance test.

## Intended command-line interface

```bash
python tools/render_episode.py --episode episode_01 --mode production
python tools/render_episode.py --episode episode_01 --scene scene_01 --mode production
python tools/render_episode.py --episode episode_01 --shot S01_B01 --mode debug
python tools/validate_episode.py --episode episode_01 --report
```

These are target commands, not claims of existing implementation.

## Implementation sequence

### A. Inventory and protect
- Inventory the project tree, rigs, benchmarks, audio, tool versions, and Git state.
- Record file paths, hashes, sizes, and relevant media metadata.
- Create a timestamped backup before modifying anything.
- Separate source assets from generated outputs.
- Record exact Godot, Python, FFmpeg, and FFprobe versions.

### B. Configuration contract
- Define a versioned JSON schema.
- Define episode, scene, shot, character, dialogue, audio, and render-profile fields.
- Use frame-based timing as the authoritative timing representation.
- Validate configuration before rendering.
- Define safe path resolution and missing-asset errors.

### C. Godot adapter
- Provide a headless adapter that loads each existing rig and renders an isolated shot.
- Keep shot configuration separate from rig implementation.
- Support explicit frame ranges and render settings.
- Exclude debug-only diagnostics from production renders.

### D. Python production controller
- Parse and validate configuration.
- Run preflight checks and resolve assets.
- Render individual shots and batch scenes/episodes.
- Resume safely from completed, validated shots.
- Produce structured progress and failure logs.
- Return meaningful non-zero exit codes.
- Never treat a partial render as complete.

### E. FFmpeg assembly
- Assemble shots in configured order.
- Apply explicit frame rate, codec, pixel format, audio mapping, and duration policy.
- Preserve source dialogue and soundtrack files unchanged.
- Record assembly settings and media metadata in a manifest.

### F. Validation and reporting
- Verify resolution, frame rate, duration, and expected frame count.
- Verify audio stream presence and mapping.
- Check stream-level A/V start-time offset and stream-duration difference within a documented tolerance.
- Detect missing assets, incomplete shots, corrupt media, and debug overlays.
- Produce machine-readable manifests and human-readable reports.

### G. Offline acceptance test
- Disconnect internet access.
- Start from a clean output directory.
- Run the documented production command.
- Load both existing character rigs.
- Render a configured scene containing multiple shots.
- Assemble the video with configured original audio.
- Run validation and inspect the report.
- Repeat from the same configuration and assess reproducibility.
- Use the Khaled and Kevin benchmarks as regression references.

### H. Documentation
Document installation, dependencies, offline operation, configuration, shot/scene/episode rendering, validation, backups, restoration, recovery, and troubleshooting.

## Acceptance criteria

Milestone 6 is complete only when a clean local setup can execute the documented workflow offline, render both existing rigs through the same controller, assemble audio/video, validate the result, and recover safely from an interrupted render.

Distinguish bit-identical output from visually and temporally equivalent output. Document nondeterministic behavior rather than hiding it.

## Known animation limitations

The current character benchmarks are functional prototypes, not finished production-quality animation. Known gaps include phoneme-level lip synchronization, facial-layer edge polish, more readable head movement, articulated torso/arms/hands/props, smooth gaze tracking, broader expression work, and removal of diagnostics from production output.

Milestone 6 must integrate and preserve current work, not misrepresent these gaps as solved.

## Completion evidence

- Inventory and backup report.
- Toolchain/version report.
- Versioned configuration schema and example episode.
- Source code and tests.
- Rendered shot and assembled episode samples.
- FFprobe metadata and validation report.
- A/V synchronization evidence.
- Offline acceptance-test log.
- Regression comparison against Khaled and Kevin benchmarks.
- Recovery and restore test evidence.
