# Episode 1 speaker-aware timeline pipeline

## Current implementation slice

The timeline builder now has two paths:

- The default compatibility path continues to build the approved four-turn opening.
- `--transcript <json>` accepts a canonical, speaker-cued, explicitly approved transcript for the full episode. The builder validates every aligned word against the approved turn text before assigning speaker IDs, fails closed on any mismatch, writes the transcript hash/version to the manifest, and emits flat schema-version-1 events.

The canonical transcript input must match `config/schemas/holos-canonical-transcript-v1.schema.json`. Its `utterances` array contains dialogue only, in exact audio order; do not include action, SFX, visual directions, or post-credit text that is not in the selected audio master. Set `approval_status` to `approved` only after the canonical source transcript/version is confirmed. Use stable speaker IDs: `KEVIN`, `KHALED`, `ORBIT`, and `THE_MOON`. `THE_MOON` and `ORBIT` are provisional because the available screenplay is an unverified extraction.

Example:

```json
{
  "transcript_version": "episode-01-canonical-2026-11-15-v1",
  "approval_status": "approved",
  "utterances": [
    {"utterance_id": "S01-U001", "scene_id": "S01", "speaker": "KEVIN", "text": "Tell me again why we're living inside a dead rock?"},
    {"utterance_id": "S01-U002", "scene_id": "S01", "speaker": "KHALED", "text": "Because the rock is interesting."}
  ]
}
```

## Run after prerequisites are present

The current builder consumes a WhisperX alignment JSON; it does not itself create the alignment or run diarization. After obtaining the exact source-audio master, author-approved transcript, and a freshly generated alignment from that same audio, run:

```bash
python tools/build_holos_full_episode_timeline.py \
  --alignment path/to/episode1-whisperx-alignment.json \
  --transcript path/to/episode1-canonical-transcript.json \
  --source-mp3 path/to/episode1-source.mp3 \
  --expected-source-sha256 <64-hex-source-hash> \
  --expected-alignment-sha256 <64-hex-alignment-hash> \
  --audio-duration-seconds <measured-duration> \
  --absolute-output output/episode1-timeline-v1.json
```

To generate a review-WAV-relative timeline, also provide `--review-wav`, `--expected-review-wav-sha256`, `--review-offset-seconds`, and `--relative-output`. The builder refuses to overwrite existing outputs. Review any mismatch or normalization explicitly; never change the approved dialogue to make an alignment pass.

## Validation and production limitations

The flat event array preserves per-phoneme viseme timing. Word boundaries come from the acoustic alignment; internal phoneme intervals remain pronunciation-dictionary subdivisions and are not dedicated acoustic phoneme alignment. Speaker attribution in this builder is inherited from verified screenplay turn cues. A diarization model is not run here; diarization can be added as an independent discrepancy/overlap check, not as an unreviewed replacement for canonical cues.

Python and Godot now recognize the four provisional IDs and check event word/speaker pairs against `approved_transcript`. Legacy fixture files with no `approved_transcript` retain the old opening-only safeguards. The original canonical screenplay, source audio, production Godot scenes, character rigs, and rig-control notes are still required before any production timeline, animation, or final episode render can be accepted.
