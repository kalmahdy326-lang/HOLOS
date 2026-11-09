# HOLOS Engine — Quickstart

**Project author:** Khaled AL-MAHDY  
**Engine version:** 0.1.0  
**Status:** Initial scaffold; preflight and configuration validation only.

## Requirements

- Python 3.11 or newer.
- Git (recommended).
- Godot 4.x for the upcoming rendering adapter.
- FFmpeg and FFprobe for the upcoming assembly and media-validation stages.

The current preflight command detects these tools. It does not install them.

## Get the project

Clone the private repository using an account that has access:

```bash
git clone https://github.com/kalmahdy326-lang/HOLOS.git
cd HOLOS
```

## Validate the example configuration

```bash
python tools/holos.py validate --episode examples/episode_01.json
```

## Run local preflight

```bash
python tools/holos.py preflight --episode examples/episode_01.json
```

The command prints detected tool versions and checks configured asset paths. It writes a JSON report under `output/reports/`.

The example audio path is intentionally a placeholder. A missing-asset result is expected until real project assets are inventoried and mapped.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Assemble rendered frames

Once a complete, contiguous frame sequence exists, configure the original
dialogue and optional music paths in the episode JSON, then run:

```bash
python tools/holos.py assemble \
  --episode examples/episode_01.json \
  --frames-dir output/episode_01/frames \
  --output output/episode_01/episode_01.mp4
```

The command derives the expected frame count from the configured shot ranges,
refuses to overwrite an existing MP4, uses FFmpeg to assemble the numbered
frames, probes the result with FFprobe, and writes a JSON validation report.
The frame directory must contain one contiguous sequence named
`frame_000000.png`, `frame_000001.png`, and so on. The configured dialogue
and music files are read as inputs; they are not modified.

## Current implementation boundary

Implemented:
- Version 1 episode configuration validation.
- Duplicate scene and shot ID detection.
- Frame-range validation.
- Toolchain detection.
- Safe project-root-bounded asset existence checks.
- JSON preflight report output.
- FFmpeg frame-sequence assembly with optional dialogue/music inputs.
- FFprobe metadata inspection and basic output validation.
- CLI assembly command with no-overwrite behavior.

Not implemented yet:
- A passing Godot headless render against the minimal test project.
- Khaled and Kevin rig adapters.
- Shot scheduling and resumable batch rendering.
- A/V synchronization validation beyond basic stream/duration checks.
- Production/debug render separation.
- Backup and recovery orchestration.
- Offline acceptance test.

The `render` command currently exits with a clear not-implemented message. Do not treat the scaffold as a production renderer.

## Configuration timing

Shot timing is expressed as a half-open frame interval:

`start_frame <= frame < end_frame`

For example, frames 0 through 239 are represented by `start_frame: 0` and `end_frame: 240`. At 24 fps, that interval is 10 seconds.

## Safety

Do not put original dialogue, soundtrack, artwork, or benchmark files in generated-output folders. Do not overwrite source media during rendering. Inventory and backup must precede asset migration.
