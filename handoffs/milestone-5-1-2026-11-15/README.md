# HOLOS PR #6 Handoff Bundle

This bundle is prepared for upload to the existing draft PR #6 in `kalmahdy326-lang/HOLOS`.

## Source MP3

The local source MP3 hash matches the recorded handoff hash:

```text
e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f
```

## Included artifacts

- `HOLOS_FullEpisode_WhisperX_Aligned.json`: full-episode WhisperX word/character alignment.
- `HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json`: absolute full-MP3-time flat event timeline.
- `HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json`: timeline offset to the padded review WAV.
- `build_holos_full_episode_timeline.py`: Manus-environment builder supplied for provenance; its hard-coded `/home/ubuntu` paths and external processor import make it non-runnable from this repository as-is.
- `HOLOS_Episode1_four_turn_review_manifest.json`: source, extraction, format and artifact hashes.
- `HOLOS_FullEpisode_FourTurn_Approved_Handoff.md`: transcript, boundaries and verification record.
- `HOLOS_FullEpisode_FourTurn_Exchange_Timing_Report.md`: measured timing report.

## WAV hash discrepancy

The review WAV generated in this Manus sandbox is:

```text
HOLOS_Episode1_four_turn_review.wav
SHA-256: 4b8c1d78ac6ca233f9ae2ba3f31566baaa75a83802eac8257ba7cba48cd76730
```

The external workspace reports a different WAV hash beginning `e9d8a3a8` and ending `2db74194`.

These are different byte-level files. The source MP3 hash is identical, so the discrepancy is in the derived extraction, not the source episode. The likely causes are different extraction start/end semantics, decoder padding, encoder/decoder implementation, or WAV metadata/chunk layout. The external WAV cannot be treated as byte-identical to the Manus-derived WAV without its complete hash and extraction command.

For reproducibility, the Manus WAV was generated with FFmpeg using:

```bash
ffmpeg -y -v error \
  -ss 0.091 -to 16.916 \
  -i HOLOS_Episode_1_The_Moon_Has_Anger_Issues_FULL.mp3 \
  -ar 48000 -ac 2 -c:a pcm_s24le \
  HOLOS_Episode1_four_turn_review.wav
```

Measured Manus WAV properties:

```text
48,000 Hz
stereo
24-bit PCM
16.825 seconds
```

The two WAVs should remain separate provenance variants until the external WAV’s exact command, duration, format and complete SHA-256 are supplied.

## Validation boundary

The four-turn exchange passed the following checks:

- Source MP3 hash match.
- First word `Tell`.
- No leading `But`.
- Complete fourth line through `away from you`.
- Speaker order Kevin, Khaled, Kevin, Khaled.
- User pronunciation approval.
- Flat event schema and chronological positive-duration events.

The two timeline JSONs contain 189 flat events each, but omit top-level `schema_version`. The current Godot loader tolerates unversioned input; the canonical processor emits `schema_version: 1`. Internal phoneme intervals are dictionary-based subdivisions inside acoustically aligned word intervals, not dedicated phoneme-aligner output.

Godot integration was not performed and no production project files were changed.


## Portable timeline builder

The canonical builder is `tools/build_holos_full_episode_timeline.py`. It consumes a WhisperX alignment and hash-verified source MP3; it does not run ASR or modify audio. Relative input and output paths resolve from the repository root. It calls the repository's strict v2.1 processor and emits versioned flat `schema_version: 1` event timelines.

The source hash and measured source duration are required. To create a review-relative timeline, also provide a specific review WAV, its complete expected SHA-256, and the extraction offset. This is intentional while the two review WAV variants remain distinct.

Example shape (replace placeholders with the selected, verified files and hashes):

```text
python tools/build_holos_full_episode_timeline.py \
  --alignment handoffs/milestone-5-1-2026-11-15/HOLOS_FullEpisode_WhisperX_Aligned.json \
  --source-mp3 "<verified-source-mp3-path>" \
  --expected-source-sha256 "<64-character-sha256>" \
  --audio-duration-seconds 914.880 \
  --absolute-output "<new-absolute-timeline-path>" \
  --review-wav "<selected-review-wav-path>" \
  --expected-review-wav-sha256 "<64-character-sha256>" \
  --review-offset-seconds 0.091 \
  --relative-output "<new-review-relative-timeline-path>" \
  --manifest-output "<new-manifest-path>"
```

The builder refuses to replace existing outputs. Install the repository's alignment requirements, including `pronouncing`, before generating phoneme-labelled estimates. Internal phoneme subdivisions remain estimates; this builder does not provide dedicated phoneme alignment.
