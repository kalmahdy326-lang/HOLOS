# HOLOS Episode 1 — Full-Video Production Roadmap

**Status:** Production preparation in progress; no complete Episode 1 video has been rendered. The canonical screenplay, source audio, and original production Godot rigs/scenes are still required.

## Production structure

The intended final cut is organized as:

1. **Opening title sequence** — series title, canonical episode title, and approved visual identity, with the intro theme.
2. **Animated episode body** — shot-by-shot Godot renders driven by the canonical screenplay, verified dialogue timing, and the original character/environment assets.
3. **End credits** — approved credits text, a readable hold/scroll, and the closing theme.
4. **Final assembly** — ordered frames plus the approved dialogue/audio master and duration-matched music bed, followed by FFprobe checks and a complete playback review.

The present example episode configuration remains a starter placeholder; its sample frame range and shot are not the episode edit.

## Reusable title and credits card

The selected bookend direction is Alternative B: near-black indigo, restrained silver/amber accents, a sparse eclipse/orbit field, and a short, sharp title reveal. The reusable Godot scene is `godot/scenes/episode_bookend_card.tscn`; each shot passes its content under `scene_config` (for example, `card_mode: "title"` with `series_title` and `episode_title`, or `card_mode: "credits"` with `credits_heading` and approved `credit_lines`). The nested object cannot override renderer-owned frame size or timing fields.

`examples/episode_01_bookends_preview.json` is a 12-second title-card plus 24-second credits-card template for previewing those graphics only. Its “Episode 1” wording and “CREDITS PENDING APPROVAL” line are placeholders; this configuration is not the episode edit and must not be treated as a completed video.

The current Alternative B preview was rendered in production mode as 288 title frames and 576 credits frames. Both music-backed preview clips passed FFprobe checks at 1280×720, 24 fps, with 0.0-second audio/video start and duration deltas. Visual review covered the title reveal and hold, the final credits-line hold, the returning HOLOS slate, and the fade to black. This verifies the reusable bookends only; it does not validate the missing episode body or approve placeholder text/music for release.

## New audio preparation

Two **draft** instrumental WAV themes were synthesized locally with `tools/generate_holos_bookend_music.py`; no external AI service, purchased credit, sample library, or third-party track was used. The 80 BPM motif uses a D-minor/F-major palette. The intro is 12 seconds; the credits theme is 24 seconds. Draft outputs and their hash manifest are in the production-draft folder outside the repository until their use is approved and repository media handling is ready.

Regenerate the drafts with:

```bash
python tools/generate_holos_bookend_music.py --output-dir /path/to/drafts
```

Once the final cut duration is locked, place the two cues at the beginning and end of a single music stem (silent underneath the episode body by default):

```bash
python tools/compose_episode_music_bed.py \
  --intro assets/audio/holos_intro_theme.wav \
  --outro assets/audio/holos_credits_theme.wav \
  --duration-seconds <approved-final-duration> \
  --output assets/audio/episode_01_music_bed.wav
```

The composer requires stereo 48 kHz signed 16-bit PCM WAV inputs, refuses to overwrite existing files, verifies that both themes fit, preserves the source themes, and writes a SHA-256 manifest. If both dialogue and music are present, `audio.music_gain_db` controls music relative to dialogue; its default is `-18 dB`.

## Binary asset intake and Git LFS

`.gitattributes` now routes production textures/art, editable art, 3D source models, audio, and video through Git LFS while keeping Godot scripts/scenes/resources and JSON diffable. The current sandbox does not have `git-lfs`, so no LFS objects or original production binaries have been added. Before asset upload, install Git LFS in the authorized upload environment, run `git lfs install`, and verify representative paths with `git check-attr filter -- <path>` and `git lfs ls-files`. Upload the original project/resource tree and its inventory/backup manifest; do not rewrite repository history to migrate unrelated existing files.

## Required source handoff before the animated body can be produced

- **Canonical screenplay:** exact approved version, including the ending, scene headings, speaker cues, and any approved revisions. This resolves the known ending/transcript conflict.
- **Source audio master:** selected production file with provenance and its SHA-256; provide the exact recording/edit that the canonical screenplay is intended to match.
- **Character assets:** complete original Godot project or the full Khaled/Kevin source resource sets, including primary scenes, scripts, textures, animation resources, plugins/addons, project settings, and their known-good benchmarks. The current repository has neither original rig and their dependencies.
- **Episode world assets:** approved environments, props, logos/title design, fonts, and any required reference images; preserve originals and provide a source inventory before integration.
- **Credits approval:** confirm the exact series/episode title and credit wording for creator, writing, direction, voice cast, animation, music, sound, and any rights/acknowledgement lines. Do not publish placeholder names or imply rights that have not been confirmed.
- **Delivery target:** confirm whether the existing 1280×720, 24 fps starter settings are appropriate or whether another delivery size/frame rate is required.

## After source intake

1. Inventory and SHA-256 hash the source package; create and verify a protected backup before copying or adapting anything.
2. Confirm the canonical transcript against the source audio. Resolve disputed words by listening to the exact audio region; keep corrections auditable.
3. Generate the approved speaker-cued transcript, align it to audio, and validate all word/speaker assignments. Produce a full-episode timeline only after canonical transcript approval.
4. Inspect the real Godot rigs and dependencies. Implement wrappers against their actual controls; preserve the original projects and compare renders with the existing benchmarks.
5. Build a frame-accurate shot list and episode JSON from the screenplay; add the title/credits shots and validated audio paths only after the wording and timing are approved.
6. Render low-resolution or short debug samples first, then production shots. Review acting, mouth timing, continuity, background art, and scene transitions with the project owner.
7. Lock the final frame count, compose the exact-duration bookend music bed, assemble without overwriting sources, and validate frame rate, dimensions, runtime, audio presence, and A/V sync.
8. Watch the complete export from start to finish, correct any issues, re-render affected shots, and record final hashes, tool versions, approvals, and export metadata in a production manifest.

## Acceptance boundary

Passing CI, the generic Godot renderer, or an audio smoke test proves tooling behavior only. A complete Episode 1 deliverable requires the real screenplay, approved audio, original character/environment assets, rendered episode shots, approved credits, final mix, and full-playback review. The local theme tracks are drafts and require the project owner's approval before they are treated as final music.
