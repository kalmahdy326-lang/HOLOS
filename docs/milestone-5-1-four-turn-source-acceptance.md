# Milestone 5.1 four-turn source acceptance record

Status: **source wording and pronunciation approved; acoustic alignment and Godot runtime validation remain pending.**

## Approved transcript

The repository's locked wording remains authoritative:

- **KEVIN:** Tell me again why we're living inside a dead rock?
- **KHALED:** Because the rock is interesting.
- **KEVIN:** It's 380,000 kilometres from the nearest decent restaurant.
- **KHALED:** The nearest restaurant is also 380,000 kilometres away from you.

The user confirmed that the pronunciation review was good. The approved spelling remains **kilometres**. The reported WhisperX spelling **kilometers** is treated as an ASR orthographic normalization and is not copied into the transcript.

## Reported absolute timings in the full-episode MP3

These timings were supplied in the full-episode analysis report and are absolute MP3 times. They are not the timings from the 15-second benchmark WAV.

| Turn | Speaker | Start (s) | End (s) |
|---|---|---:|---:|
| 1 | KEVIN | 0.191 | 3.192 |
| 2 | KHALED | 3.912 | 6.013 |
| 3 | KEVIN | 6.933 | 11.054 |
| 4 | KHALED | 11.834 | 16.816 |

Reported extraction envelope: 0.191–16.816 s. A padded audition derivative was previously created locally using 0.091–16.916 s; the source MP3 was not modified.

## Evidence and provenance

- Source named in the supplied report: `HOLOS_Episode_1_The_Moon_Has_Anger_Issues_FULL.mp3`
- Source SHA-256 recorded during local review: `e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f`
- The report states the exchange begins with “Tell”, follows KEVIN → KHALED → KEVIN → KHALED, and includes the complete final words “away from you”.
- The user explicitly approved the pronunciation after auditioning the review segment.
- The timing measurements and transcript checks above are reported evidence; the original MP3 and full WhisperX alignment JSON are not stored in this repository.

## Remaining gate

This record does **not** supply word-level or phoneme-level timestamps. Do not synthesize phoneme events from turn boundaries. Milestone 5.1 still requires a fresh alignment artifact derived from the accepted source, validation against the strict processor and flat `schema_version` event contract, and Godot/runtime validation before production acceptance.

## Manus availability

No Manus connector or Manus project access was available in the authoring workspace when this record was prepared. No Manus artifact is claimed.
