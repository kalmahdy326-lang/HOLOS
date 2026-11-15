# HOLOS Episode 1 — Four-Turn Exchange Approved Handoff

## Source verification

Source MP3:

```text
/home/ubuntu/HOLOS_Episode_1_The_Moon_Has_Anger_Issues_FULL.mp3
```

Recorded SHA-256 from the supplied handoff guidance:

```text
e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f
```

SHA-256 measured in this sandbox:

```text
e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f
```

Hash result:

```text
PASS — exact source hash match
```

The source MP3 was not modified.

## Approved transcript

```text
KEVIN: Tell me again why we're living inside a dead rock?

KHALED: Because the rock is interesting.

KEVIN: It's 380,000 kilometres from the nearest decent restaurant.

KHALED: The nearest restaurant is also 380,000 kilometres away from you.
```

The user auditioned the extracted review segment and approved the pronunciation. The approved transcript retains `kilometres`. WhisperX’s `kilometers` output is recorded as an accepted provisional ASR spelling normalization and must not replace the approved transcript.

## Measured full-episode turn boundaries

These are absolute times in the verified full-episode MP3. They are turn boundaries, not phoneme timings:

| Speaker | Start | End |
|---|---:|---:|
| Kevin | 0.191 s | 3.192 s |
| Khaled | 3.912 s | 6.013 s |
| Kevin | 6.933 s | 11.054 s |
| Khaled | 11.834 s | 16.816 s |

Recommended speech-word extraction range:

```text
0.191–16.816 seconds
```

A padded review range previously used was:

```text
0.091–16.916 seconds
```

The padded review WAV is a review intermediate and must not be confused with an accepted production WAV unless its hash and format are recorded in the repository handoff.

## Verification results

- Source MP3 available: PASS.
- Source SHA-256 match: PASS.
- First spoken word is `Tell`: PASS.
- Leading `But` detected: NO.
- All four turns present: PASS.
- Speaker order: Kevin, Khaled, Kevin, Khaled: PASS.
- Fourth line reaches `away from you`: PASS.
- Pronunciation review: APPROVED by user.
- Approved transcript spelling: `kilometres` retained.
- Full phoneme-level production timeline: NOT YET GENERATED.
- Godot runtime integration: NOT YET PERFORMED.

## Current handoff status

The full-episode source and turn-level evidence are now suitable as an audio handoff input. The next required artifact is a fresh alignment package generated from this exact hash-verified source or from a derived clip whose provenance and hash are recorded:

```text
HOLOS_FullEpisode_WhisperX_Aligned.json
HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json
```

No phoneme timings may be inferred from the four turn boundaries. The existing intermediate benchmark alignment remains non-authoritative.

