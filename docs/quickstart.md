# HOLOS Engine — Quickstart

**Project author:** Khaled AL-MAHDY  
**Engine version:** 0.1.0  
**Status:** Single-shot and ordered multi-shot rendering, resumable manifests, and verified multi-shot FFmpeg episode assembly are implemented. Character-rig integration and production-machine acceptance remain in development.

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

## Create a source inventory before asset changes

Run the read-only inventory before moving, renaming, or backing up project
assets:

\`\`\`bash
python tools/holos.py inventory
\`\`\`

The command hashes regular source/project files with SHA-256 and writes a
timestamped report under \`output/reports/\`. It records path, category, file
extension, byte size, and hash, plus an aggregate inventory hash. It does not
follow symlinks, read common secret-file names such as \`.env\` and private-key
files, or scan generated output, Git metadata, dependency folders, and caches.
A custom report path is accepted only under \`output/reports/\`; existing reports
are never overwritten. This is an inventory, not a backup.

## Audit Godot resource dependencies

Before integrating a character scene, run a static audit of literal `res://`
references in the Godot project:

```bash
python tools/holos.py audit-godot-assets --godot-project godot
```

The audit reports resolved, missing, and unsafe resource paths, skips generated
Godot caches, and refuses to follow symbolic links. It also lists `uid://`
references separately because their resolution depends on Godot's resource UID
database. Dynamically constructed paths are not statically resolvable; a clean
report does not replace loading the project in Godot.

## Create and verify a source backup

After reviewing the inventory report, create a verified copy:

\`\`\`bash
python tools/holos.py backup \\
  --inventory output/reports/source-inventory-YYYYMMDDTHHMMSSZ.json
\`\`\`

The command accepts only a complete inventory from this project. It rechecks
the aggregate inventory hash and each source file's size and SHA-256 before
copying, then verifies every copied file. Backups are created as new directories
under \`output/backups/\`; existing backups are never overwritten. A failed copy
is preserved in a directory marked \`FAILED-\` instead of being silently deleted.
The command does not modify source files.

Use the exact backup directory reported by the command to verify and restore a
snapshot into a separate new folder:

\`\`\`bash
python tools/holos.py restore \\
  --backup output/backups/source-backup-YYYYMMDDTHHMMSSffffffZ
\`\`\`

Restore verifies the backup manifest, each file hash, and total size before
copying into a new directory under \`output/restores/\`. It never writes over the
working project or an existing restore directory. The result is a source
snapshot, not an in-place project replacement: Git metadata, generated output,
caches, and file names excluded from the inventory (including common secret
files) are not recreated. A failed restore is preserved in a \`FAILED-\`
directory for inspection.

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
`output/renders/adapter_test_episode/debug/ADAPTER_TEST/` and writes a JSON report
under `output/reports/`. It refuses to use a non-empty shot output directory.
Choose a new output location or safely archive the prior generated render
before repeating a render.

## Render a complete episode as an ordered shot batch

The batch command visits scenes and shots in configuration order:

```bash
python tools/holos.py render-episode \
  --episode examples/adapter_test_episode_batch.json \
  --mode debug
```

On display-less Linux, add `--display-wrapper xvfb-run` and run with
`LIBGL_ALWAYS_SOFTWARE=1`.

Each shot is rendered into its own directory under
`output/renders/{episode_id}/{mode}/{shot_id}/`. The command writes a resumable
manifest to `output/manifests/{episode_id}-{mode}-render.json` and a batch
summary under `output/reports/`.

On a subsequent run, a shot marked completed is skipped only when its exact
expected numbered PNG sequence still exists and every frame file is non-empty.
An interrupted, failed, or invalid shot directory is moved—not deleted—to
`output/recovery/` before it is rendered again. Each completed frame is recorded
with its size and SHA-256 hash; resume and episode assembly re-hash the files
rather than trusting a status flag alone. The manifest rejects duplicate,
reordered, malformed, or invalid-attempt records. Batch render, manifest, and
recovery paths reject symbolic-link traversal so a generated-output symlink
cannot redirect an archive or overwrite an unrelated directory. The manifest
is atomically updated as each shot changes state. If the episode configuration or render
mode changes, the existing manifest refuses to resume; preserve that run and
use a new episode ID for a distinct configuration.

Render modes use isolated output folders, so debug renders cannot be mistaken
for production renders. The optional `render.debug_overlay` boolean defaults
to `false`; when enabled, it appears only in debug renders and is forcibly
disabled by the production CLI.

The two-shot example is a test fixture, not Episode 1 content.

## Assemble a complete episode from rendered shots

First render or resume the ordered batch:

\`\`\`bash
python tools/holos.py render-episode \\
  --episode examples/adapter_test_episode_batch.json \\
  --mode debug
\`\`\`

Then assemble only after every shot has a completed manifest entry and its
frame hashes still match:

\`\`\`bash
python tools/holos.py assemble-episode \\
  --episode examples/adapter_test_episode_batch.json \\
  --mode debug \\
  --output output/adapter_test_episode_batch.mp4
\`\`\`

The command verifies the manifest against the episode configuration and the
configured shot order. It stages a contiguous sequence from the individual
shot folders in a temporary directory, then uses FFmpeg to encode the complete
episode. FFprobe validates dimensions, frame rate, total duration, required
audio presence, audio/video stream start-time offset, and stream-duration
difference. The permitted stream timing difference is controlled by
`audio.sync_tolerance_ms` (default: 80 ms). The final MP4 is published only
after validation succeeds. Existing shot renders and source dialogue/music
remain unchanged. Existing episode output files are never overwritten.

The batch fixture is for testing the engine; it is not Episode 1 content.

## Assemble rendered frames

After rendering a shot, assemble its contiguous numbered frames:

```bash
python tools/holos.py assemble \
  --episode examples/adapter_test_episode.json \
  --frames-dir output/renders/adapter_test_episode/debug/ADAPTER_TEST \
  --output output/adapter_test_episode.mp4
```

The command derives the expected frame count from the configured shot ranges,
refuses to overwrite an existing MP4, uses FFmpeg to assemble the numbered
frames, probes the result with FFprobe, and writes a JSON validation report.
The configured dialogue and music files are read as inputs; they are not
modified. When audio is included, FFprobe also checks stream start-time and
duration alignment against `audio.sync_tolerance_ms` (default: 80 ms). This
checks encoded stream timing; it does not prove sample-accurate synchronization
with dialogue cues or animation events.

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
- Read-only project source inventory with per-file and aggregate SHA-256 hashes.
- Verified source backup with pre-copy and post-copy hash checks.
- Non-overwriting restore into a separate source snapshot directory, with verification.
- Python-to-Godot subprocess adapter with path and output safety checks.
- Single-shot rendering through the generic Godot scene hooks.
- Four-frame Godot rendering integration test.
- CLI single-shot render command and mode-specific JSON render report.
- Separate debug/production render directories and a debug-only overlay gate, tested with actual Godot frame output.
- Ordered multi-shot episode rendering with a resumable status manifest.
- Verified-completion skipping, per-frame SHA-256 integrity records, and preservation of partial output in recovery.
- Ordered staging of separate verified shot folders into one contiguous episode frame sequence.
- Verified multi-shot `assemble-episode` workflow with final output publication after FFprobe validation.
- FFmpeg frame-sequence assembly with optional dialogue/music inputs.
- FFprobe metadata inspection, stream-level A/V start/duration checks, and configurable tolerance.
- FFmpeg end-to-end integration test using two generated audio sources.
- CLI assembly command with no-overwrite behavior.

Still in development:
- Khaled and Kevin character-rig adapters and validation against their real project scenes.
- Sample-accurate synchronization against dialogue cues, phoneme timing, and animation events; current validation checks encoded stream start times and durations only.
- One-click backup/restore of the actual external Khaled/Kevin rig directories once those source assets are present and inventoried.
- Offline acceptance test on the target production machine.

## Configuration timing

Shot timing is expressed as a half-open frame interval:

`start_frame <= frame < end_frame`

For example, frames 0 through 239 are represented by `start_frame: 0` and
`end_frame: 240`. At 24 fps, that interval is 10 seconds.

## Safety

Do not put original dialogue, soundtrack, artwork, or benchmark files in generated-output folders. Do not overwrite source media during rendering. Inventory and backup must precede asset migration.
