# Godot Offscreen and Visual Lip-Sync CI Reference

## Core distinction

`godot --headless` is suitable for scene loading, script parsing, timeline self-tests and deterministic logic. It does not provide useful rendered pixels for facial-seam, hair-continuity or lip-sync inspection. Do not mark a visual gate passed from headless exit code alone.

For pixel evidence on Linux CI, use a virtual display and a normal Godot window:

```bash
sudo apt-get update
sudo apt-get install -y xvfb
xvfb-run -a --server-args='-screen 0 1280x720x24' \
  ./Godot_v4.x_linux.x86_64 \
  --path . \
  --rendering-method gl_compatibility \
  --display-driver x11 \
  --resolution 1280x720 \
  --quit-after 300
```

The exact Godot flags depend on the project version. Validate them against the installed binary before committing a workflow change.

## Required pixel-capture architecture

A visual lip-sync check needs all of the following:

1. **Real rendering context:** `xvfb-run`, a parked desktop window, or another supported display server.
2. **Known renderer:** GL Compatibility is usually the most portable choice for Linux CI; record the driver and renderer.
3. **Deterministic transport:** drive animation from the playing audio clock or a fixed test clock; do not use a second unconstrained timer.
4. **Capture trigger:** an autoload or test scene waits for `frame_post_draw` and writes PNGs, or Godot Movie Writer produces a video sequence.
5. **Known timestamps:** capture frames at dialogue starts, consonant transitions, silence boundaries, speaker changes and final-line completion.
6. **Artifact publication:** upload the captured PNGs/video and a JSON manifest containing commit SHA, Godot version, renderer, resolution, frame rate, audio/timeline hashes and capture timestamps.
7. **Automated assertions:** verify that expected files exist, are non-empty, have the expected dimensions and correspond to the requested timestamps. Pixel similarity or visual review may remain a separate human gate.

## Example capture flow

```bash
mkdir -p artifacts/godot-capture
xvfb-run -a --server-args='-screen 0 1280x720x24' \
  ./Godot_v4.x_linux.x86_64 \
  --path . \
  --rendering-method gl_compatibility \
  --display-driver x11 \
  --resolution 1280x720 \
  --quit-after 300

test -s artifacts/godot-capture/manifest.json
test -n "$(find artifacts/godot-capture -type f -name '*.png' -print -quit)"
```

A capture script should write a manifest similar to:

```json
{
  "commit": "<head-sha>",
  "godot_version": "4.x",
  "renderer": "gl_compatibility",
  "resolution": "1280x720",
  "fps": 30,
  "audio_sha256": "<selected-wav-hash>",
  "timeline_sha256": "<timeline-hash>",
  "frames": [
    {"time_seconds": 0.100, "file": "frame_000003.png"},
    {"time_seconds": 6.842, "file": "frame_000206.png"}
  ]
}
```

## Godot workflow gates

Keep these gates separate:

- **Headless logic gate:** project import, script parse, timeline schema, event order, audio-clock behavior.
- **Pixel render gate:** virtual/real display starts, capture files are created, image dimensions and manifest are valid.
- **Visual acceptance gate:** inspect frames for facial seams, hair pops, mouth-layer discontinuities, incorrect speaker ownership, timing drift and unwanted artifacts.

## Common false positives

- A successful `--headless` run with no images is not a visual pass.
- A workflow step named `offscreen-render` may still only run logic tests.
- A minimized window without a capture trigger does not prove pixels were recorded.
- A timeline with absolute full-MP3 timestamps must not be paired with a clipped WAV without applying the extraction offset.
- Different WAV hashes require separate manifests; do not substitute one variant silently.

## Acceptance rule

Milestone 5.1 visual acceptance requires a reproducible pixel-producing capture and review. If CI cannot provide a valid display/capture path, record visual validation as manual/desktop-gated and keep production acceptance pending.
