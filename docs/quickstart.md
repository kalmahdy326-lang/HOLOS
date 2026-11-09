# HOLOS Engine — Quickstart

**Project author:** Khaled AL-MAHDY  
**Engine version:** 0.1.0  
**Status:** Single-shot Godot rendering and FFmpeg assembly are implemented and covered by automated integration tests. Character-rig integration and full-episode orchestration remain in development.

## Requirements

- Python 3.11 or newer.
- Godot 4.x.
- FFmpeg and FFprobe.
- A rendering-capable display for Godot viewport capture. On display-less Linux systems, use Xvfb and Mesa software rendering.

The strict Godot `--headless` option uses a dummy renderer and cannot provide viewport textures for PNG capture. The HOLOS render command therefore launches Godot in rendering mode. Use a normal desktop display, or provide `--display-wrapper xvfb-run` on Linux.

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

## Render the Godot adapter test shot

On a desktop with a working display:

```bash
python tools/holos.py render \
  --episode examples/adapter_test_episode.json \
  --shot ADAPTER_TEST \
  --mode debug
```

On display-less Linux with Godot, Xvfb, and Mesa installed:

```bash
LIBGL_ALWAYS_SOFTWARE=1 python tools/holos.py render \
  --episode examples/adapter_test_episode.json \
  --shot ADAPTER_TEST \
  --mode debug \
  --display-wrapper xvfb-run
```

The command renders the configured shot into
`output/renders/adapter_test_episode/ADAPTER_TEST/` and writes a JSON report
under `output/reports/`. It refuses to use a non-empty shot output directory.
Choose a new output location or safely archive the prior generated render
before repeating a render.

## Assemble rendered frames

After rendering a shot, assemble its contiguous numbered frames:

```bash
python tools/holos.py assemble \
  --episode examples/adapter_test_episode.json \
  --frames-dir output/renders/adapter_test_episode/ADAPTER_TEST \
  --output output/adapter_test_episode.mp4
```

The command derives the expected frame count from the configured shot ranges,
refuses to overwrite an existing MP4, uses FFmpeg to assemble the numbered
frames, probes the result with FFprobe, and writes a JSON validation report.
The configured dialogue and music files are read as inputs; they are not
modified.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The Python/media CI job installs FFmpeg and runs the media integration test.
A separate Godot CI job downloads a pinned Godot version and uses Xvfb plus
software rendering to execute the actual four-frame Godot test and the CLI
render test. This CI download is only a test setup step; the local production
pipeline uses locally installed tools and does not require an AI service or
network access at runtime.

## Current implementation boundary

Implemented and CI-tested:
- Version 1 episode configuration validation.
- Duplicate scene and shot ID detection.
- Frame-range validation.
- Toolchain detection.
- Safe project-root-bounded asset existence checks.
- JSON preflight report output.
- Python-to-Godot subprocess adapter with path and output safety checks.
- Single-shot rendering through the generic Godot scene hooks.
- Four-frame Godot rendering integration test.
- CLI single-shot render command and JSON render report.
- FFmpeg frame-sequence assembly with optional dialogue/music inputs.
- FFprobe metadata inspection and basic output validation.
- FFmpeg end-to-end integration test using two generated audio sources.
- CLI assembly command with no-overwrite behavior.

Still in development:
- Khaled and Kevin character-rig adapters and validation against their real project scenes.
- Multi-shot scene/episode scheduling and resumable batch rendering.
- Joining separate shot folders into one ordered episode sequence.
- A/V synchronization validation beyond basic stream/duration checks.
- Production/debug render separation and production overlay policy.
- Backup and recovery orchestration.
- Offline acceptance test on the target production machine.

## Configuration timing

Shot timing is expressed as a half-open frame interval:

`start_frame <= frame < end_frame`

For example, frames 0 through 239 are represented by `start_frame: 0` and
`end_frame: 240`. At 24 fps, that interval is 10 seconds.

## Safety

Do not put original dialogue, soundtrack, artwork, or benchmark files in generated-output folders. Do not overwrite source media during rendering. Inventory and backup must precede asset migration.
