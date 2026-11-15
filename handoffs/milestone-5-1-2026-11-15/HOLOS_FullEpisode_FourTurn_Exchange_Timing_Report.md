# HOLOS Episode 1 — Full-Episode Four-Turn Exchange Timing Report

## Source

```text
/home/ubuntu/HOLOS_Episode_1_The_Moon_Has_Anger_Issues_FULL.mp3
```

Acoustic artifacts:

```text
/home/ubuntu/output/HOLOS_FullEpisode_WhisperX_Transcript.json
/home/ubuntu/output/HOLOS_FullEpisode_WhisperX_Aligned.json
```

The MP3 was not modified.

## Measured exchange location

WhisperX acoustic word alignment locates the four-turn exchange at the beginning of the full episode.

### Speech-word envelope

```text
Start of first approved word: 0.191 s
End of final approved word:   16.816 s
```

Recommended extraction envelope if only the speech words are required:

```text
00:00.191 – 00:16.816
```

The first detected word begins at 0.191 seconds. The parent VAD segment begins at approximately 0.031 seconds and includes lead-in silence; it does not indicate an additional spoken word before `Tell`.

## Approved-turn timestamps

| Turn | Speaker | Locked approved line | Acoustic start | Acoustic end |
|---|---|---|---:|---:|
| 1 | Kevin | `Tell me again why we're living inside a dead rock?` | 0.191 s | 3.192 s |
| 2 | Khaled | `Because the rock is interesting.` | 3.912 s | 6.013 s |
| 3 | Kevin | `It's 380,000 kilometres from the nearest decent restaurant.` | 6.933 s | 11.054 s |
| 4 | Khaled | `The nearest restaurant is also 380,000 kilometres away from you.` | 11.834 s | 16.816 s |

Inter-turn gaps measured from aligned word boundaries:

- Turn 1 → Turn 2: approximately 0.720 s.
- Turn 2 → Turn 3: approximately 0.920 s.
- Turn 3 → Turn 4: approximately 0.780 s.

## Word-level boundaries

### Turn 1 — Kevin

| Word | Start | End |
|---|---:|---:|
| Tell | 0.191 | 0.471 |
| me | 0.491 | 0.611 |
| again | 0.691 | 1.011 |
| why | 1.191 | 1.691 |
| we're | 1.791 | 1.972 |
| living | 2.032 | 2.272 |
| inside | 2.312 | 2.652 |
| a | 2.672 | 2.712 |
| dead | 2.752 | 2.892 |
| rock | 2.932 | 3.192 |

### Turn 2 — Khaled

| Word | Start | End |
|---|---:|---:|
| Because | 3.912 | 4.332 |
| the | 4.392 | 4.512 |
| rock | 4.572 | 5.312 |
| is | 5.392 | 5.472 |
| interesting | 5.553 | 6.013 |

### Turn 3 — Kevin

| Word | Start | End |
|---|---:|---:|
| It's | 6.933 | 7.053 |
| 380,000 | 7.373 | 8.673 |
| kilometers — ASR spelling; verify against approved `kilometres` | 8.693 | 9.154 |
| from | 9.194 | 9.334 |
| the | 9.374 | 9.454 |
| nearest | 9.514 | 9.894 |
| decent | 10.034 | 10.394 |
| restaurant | 10.474 | 11.054 |

### Turn 4 — Khaled

| Word | Start | End |
|---|---:|---:|
| The | 11.834 | 11.914 |
| nearest | 11.954 | 12.274 |
| restaurant | 12.314 | 12.714 |
| is | 12.795 | 12.875 |
| also | 13.035 | 13.375 |
| 380,000 | 13.395 | 14.135 |
| kilometers — ASR spelling; verify against approved `kilometres` | 15.015 | 15.515 |
| away | 15.575 | 15.775 |
| from | 15.855 | 16.075 |
| you | 16.616 | 16.816 |

## Transcript gate results

### Passed observations

- The exchange is located at the beginning of the full-episode MP3.
- The first detected spoken word is `Tell`.
- No leading `But` was detected.
- All four dialogue turns are present.
- The fourth line is complete through `away from you`.
- Speaker order is consistent with Kevin, Khaled, Kevin, Khaled.
- The full exchange is substantially longer than the defective 15-second benchmark because the complete fourth line is present.

### User decision

WhisperX transcribed the two occurrences as `kilometers`; the locked transcript uses `kilometres`. The user auditioned the review segment and approved the pronunciation. The approved transcript remains unchanged, and the two ASR spellings are recorded as explicit normalization metadata.

This approval resolves the pronunciation review. It does not validate the dictionary-based internal phoneme subdivisions as measured phoneme boundaries, nor does it establish Godot runtime or visual lip-sync acceptance.

## Extraction recommendation

The user approved the pronunciation after auditioning the review segment. For the reviewed exchange, use the approved `kilometres` transcript and the recorded word-alignment timestamps:

```text
Input:  /home/ubuntu/HOLOS_Episode_1_The_Moon_Has_Anger_Issues_FULL.mp3
Start:  0.191 seconds
End:    16.816 seconds
```

Retain at least 50–100 ms of context around the cut for auditioning, then perform a zero-crossing or short equal-power edit if a standalone WAV is required. Do not overwrite the original MP3.

The ASR spelling remains a documented normalization only; it does not alter the approved dialogue.

## Status

```text
Exchange located: YES
Four turns complete: YES
Leading But absent: YES
Final line complete: YES
Transcript pronunciation review: APPROVED by user
Four-turn review WAV generated: YES (two provenance variants; hashes differ)
Godot integration performed: NO
```
