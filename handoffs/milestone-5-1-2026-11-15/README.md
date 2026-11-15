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
- `build_holos_full_episode_timeline.py`: reproducible builder with explicit, user-approved `kilometers` → `kilometres` ASR normalization.
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

Internal phoneme intervals remain dictionary-based subdivisions inside acoustically aligned word intervals; they are not dedicated phoneme-aligner output.

Godot integration was not performed and no production project files were changed.
