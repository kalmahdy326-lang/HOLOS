# Milestone 5.1 four-turn source acceptance record

Status: **source wording and pronunciation approved; acoustic word-alignment evidence received; Godot integration and runtime validation remain pending.**

## Approved transcript

The repository's locked wording remains authoritative:

- **KEVIN:** Tell me again why we're living inside a dead rock?
- **KHALED:** Because the rock is interesting.
- **KEVIN:** It's 380,000 kilometres from the nearest decent restaurant.
- **KHALED:** The nearest restaurant is also 380,000 kilometres away from you.

The user confirmed that the pronunciation review was good. The approved spelling remains **kilometres**. WhisperX's **kilometers** output is retained as an explicit ASR spelling normalization; the approved transcript was not changed.

## Reported absolute timings

The supplied full-episode report gives these absolute MP3 times, not the old 15-second benchmark times:

| Turn | Speaker | Start (s) | End (s) |
|---|---|---:|---:|
| 1 | KEVIN | 0.191 | 3.192 |
| 2 | KHALED | 3.912 | 6.013 |
| 3 | KEVIN | 6.933 | 11.054 |
| 4 | KHALED | 11.834 | 16.816 |

## Handoff artifacts

The full-episode alignment, absolute event timeline, review-relative timeline, builder, review manifest, approved handoff, timing report, and provenance note are preserved in [the PR handoff directory](../handoffs/milestone-5-1-2026-11-15/README.md).

The Codex review records the checked archive hash, structural checks, event offset comparison, and limitations in [CODEX_REVIEW.md](../handoffs/milestone-5-1-2026-11-15/CODEX_REVIEW.md).

The source MP3 SHA-256 matches the recorded handoff hash. The MP3 itself is not committed. The Manus and Codex review WAV files have different hashes and remain separate provenance variants; the PR records both without substituting one for the other.

## Current gate

The supplied word-level boundaries are structurally consistent, and the user approved the pronunciation. Internal phoneme boundaries in the event timelines are dictionary-based estimates, not dedicated phoneme alignment. The bundled builder also references Manus-only absolute paths and a processor module absent from this repository. The timeline JSONs are unversioned; the current Godot loader accepts them, while the canonical repository processor emits `schema_version: 1`.

No Godot runtime, headless validation against these timelines, production scene integration, shared audio clock, character-rig mapping, or visual lip-sync validation has been performed. Milestone 5.1 is therefore **not yet production-accepted**.


## Production integration boundary

The checked-in `godot/` directory is the minimal adapter test project. It does not contain the Episode 1 production dialogue controller, director, Kevin or Khaled scenes/rig assets, or a WAV. The review WAVs remain distinct provenance variants and neither has been selected as the production asset.

This PR adds headless loading of the supplied event timelines to the adapter test suite. It does not connect the events to a production controller or claim an audio-derived runtime clock, rig mapping, rendered lip-sync, or visual review. Those steps require the actual production Godot project and an explicitly selected, hash-verified WAV variant.
