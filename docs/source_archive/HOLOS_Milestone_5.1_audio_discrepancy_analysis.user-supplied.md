# HOLOS Milestone 5.1 — Audio Discrepancy Analysis and Correction Plan

## Scope

This analysis compares the approved four-turn benchmark dialogue against `/home/ubuntu/output/holos_animation_test_audio_15s.wav`, the WhisperX/wav2vec2 alignment, and the existing manual phoneme timeline.

The approved benchmark dialogue is:

1. **Kevin:** “Tell me again why we're living inside a dead rock?”
2. **Khaled:** “Because the rock is interesting.”
3. **Kevin:** “It's 380,000 kilometres from the nearest decent restaurant.”
4. **Khaled:** “The nearest restaurant is also 380,000 kilometres away from you.”

The approved dialogue remains the source of truth.

## Recording facts

The source file is a stereo, 48 kHz, 16-bit WAV with a duration of exactly 15.000 seconds. WhisperX detected four speech regions:

| Turn | Speaker | Acoustic interval | WhisperX text |
|---|---|---:|---|
| 1 | Kevin | 0.031–3.193 s | “But tell me again why we're living inside a dead rock?” |
| 2 | Khaled | 3.914–6.015 s | “Because the rock is interesting.” |
| 3 | Kevin | 6.936–11.059 s | “It's 380,000 kilometers from the nearest decent restaurant.” |
| 4 | Khaled | 11.840–13.541 s | “The nearest restaurant is also 380,000” |

The source is therefore not a complete acoustic realization of the approved four-turn transcript.

## Discrepancy 1 — Unapproved leading “But”

### Evidence

WhisperX detects the following opening sequence:

| Word | Acoustic start | Acoustic end | Alignment score |
|---|---:|---:|---:|
| “But” | 0.031 s | 0.151 s | 0.25 |
| “tell” | 0.191 s | 0.471 s | 0.861 |
| “me” | 0.491 s | 0.631 s | 0.665 |
| “again” | 0.691 s | 1.012 s | 0.764 |
| “why” | 1.192 s | 1.692 s | 0.810 |
| “we're” | 1.792 s | 1.972 s | 0.802 |
| “living” | 2.032 s | 2.273 s | 0.862 |
| “inside” | 2.333 s | 2.653 s | 0.836 |
| “a” | 2.673 s | 2.713 s | 0.494 |
| “dead” | 2.753 s | 2.893 s | 0.730 |
| “rock” | 2.933 s | 3.193 s | 0.816 |

The first word has a lower confidence score than the remainder, but it is also detected by the earlier independent transcription pass. The evidence is sufficient to treat it as spoken audio, not a Whisper-only hallucination.

### Interpretation

This is most likely an unscripted pickup, conversational carry-over, or an accidental inclusion from a preceding rehearsal. It changes the approved line from:

> “Tell me again why we're living inside a dead rock?”

to:

> “But tell me again why we're living inside a dead rock?”

That is an editorial change, even though it is only one word. It should not be solved by changing the script or by creating a phoneme event for “But.”

### Recommended correction

**Preferred:** re-record Turn 1 from the beginning using the exact approved text, with no leading conjunction:

> “Tell me again why we're living inside a dead rock?”

Use the same Kevin/Puck voice and the existing performance direction. Do not ask the performer to “remove the but” through editing if the cut would damage the onset of “tell.” A clean pickup avoids a residual /t/ onset, altered breath timing, or a perceptible splice.

**Acceptable edit-only fallback:** remove or mute the interval containing “But,” approximately 0.031–0.151 s, then preserve a short natural lead-in before “tell.” This is not recommended as the primary fix because the following “tell” begins at 0.191 s and the cut would leave only approximately 40 ms between the end of the unwanted word and the onset of the approved word. The edit may sound abrupt and could remove part of the intended opening breath.

If an edit-only fix is unavoidable:

1. Place a cut after the unwanted word’s release and before the onset of “tell,” using zero-crossing or short equal-power fades.
2. Keep a clean room-tone bed under the cut.
3. Do not time-stretch the remaining phrase to compensate before checking the natural cadence.
4. Re-run WhisperX after the edit and verify that the first detected word is “tell.”

### Acceptance test for Turn 1

- First intelligible word: **Tell**.
- No audible or measurable residual “But.”
- Same speaker identity and emotional attitude as the existing Kevin take.
- No splice click, breath discontinuity, or unnatural onset.
- Approved wording must remain exactly unchanged.

## Discrepancy 2 — Truncated final line

### Evidence

The approved fourth turn is:

> “The nearest restaurant is also 380,000 kilometres away from you.”

The available recording contains only:

> “The nearest restaurant is also 380,000”

WhisperX aligns the observed portion as follows:

| Word | Acoustic start | Acoustic end | Alignment score |
|---|---:|---:|---:|
| “The” | 11.840 s | 11.920 s | 0.983 |
| “nearest” | 11.960 s | 12.220 s | 0.772 |
| “restaurant” | 12.320 s | 12.720 s | 0.704 |
| “is” | 12.800 s | 12.880 s | 0.668 |
| “also” | 13.041 s | 13.361 s | 0.957 |
| “380,000” | 13.381 s | 13.541 s | 0.999 |

The independent speech-to-text pass also ended at approximately “380,000 k-,” supporting the conclusion that the missing continuation is not merely an alignment failure.

The waveform remains non-silent after approximately 13.54 s, but residual energy is not evidence of the missing words. It may represent room tone, an unfinished vocal tail, noise, or another non-verbal sound. No phonemes for “kilometres away from you” should be invented from that residual waveform.

### Interpretation

This is a content truncation, not a timing offset. The source take does not provide an acoustic basis for animating:

- “kilometres”
- “away”
- “from”
- “you”

The manual timeline currently assigns these words through approximately 14.91 s, but those intervals are estimates derived from the approved transcript, not verified audio.

### Recommended correction

**Preferred:** record a complete replacement for Turn 4, beginning at the same conversational entry point and speaking the full approved sentence:

> “The nearest restaurant is also 380,000 kilometres away from you.”

Use Khaled/Kore with the established dry, empirical delivery. Preserve the intended comic reveal by giving a slight emphasis to **“also”** and **“380,000 kilometres,”** but do not add words, substitutions, or improvisation.

Record at least three complete takes:

1. **Natural continuity take:** match the existing turn’s calm analytical rhythm.
2. **Slightly slower clarity take:** articulate “kilometres,” “away,” and “from you” cleanly for lip-sync.
3. **Neutral safety take:** minimal emphasis and no extra pause beyond the approved punctuation.

The replacement should be recorded as a complete turn rather than as only the missing phrase. A phrase-only punch-in is possible, but it is more likely to produce a mismatch in timbre, breath, room tone, pitch, or prosody at the join after “380,000.”

**Fallback punch-in:** if a complete replacement is impossible, record only:

> “kilometres away from you.”

Start with a short pickup breath or neutral onset only if it is intended to follow the existing “380,000” take. The edit must be auditioned carefully because the existing take ends immediately after the number and may not leave a natural prosodic handoff.

### Timing guidance

Do not force the replacement to the old manual slots before hearing it. First align the complete take acoustically. Then:

1. Preserve the existing turn entry near 11.84–12.00 s if the new performance matches that entry.
2. Allow the full line to end according to the natural delivery.
3. Use only transparent time compression or expansion if necessary for the scene edit; keep the correction small and inspect formant stability and consonant clarity.
4. Re-run WhisperX and manually inspect the transitions in `restaurant`, `also`, `three hundred/eighty thousand` or the selected number pronunciation, `kilometres`, `away`, `from`, and `you`.

The current take is approximately 1.70 s from “The” to the end of the detected number. The approved line is substantially longer because it contains four additional lexical words. A natural replacement will therefore almost certainly require more duration than the incomplete take; it should not be compressed to 1.70 s merely to preserve the defective timing.

## Important pronunciation decision

WhisperX transcribes the third-turn unit as **“kilometers”**, while the approved transcript uses **“kilometres.”** This is not necessarily a real audio error because the two pronunciations can be difficult for an automatic recognizer to distinguish in a short clip. The re-recording brief should explicitly spell the approved reading as:

> “kilometres”

If the intended production pronunciation is the US form, that must be an explicit script approval. It should not be changed silently by the recognizer.

For TTS, the transcript field must contain the exact words to be spoken, while delivery instructions belong in the style field. For a human pickup, provide the exact line on the page and do not add labels or stage directions to the spoken text.

## Recommended edit order

1. Replace or clean Turn 1 so the first audible word is “Tell.”
2. Replace Turn 4 with a complete take containing the full approved sentence.
3. Reassemble the benchmark WAV while preserving the existing Turns 2 and 3 unless their voice or performance review identifies a separate issue.
4. Run WhisperX alignment on the corrected WAV.
5. Confirm all four approved turns are detected without additions or omissions.
6. Review word gaps and the consonant transitions relevant to viseme switching.
7. Only after the corrected audio passes transcript and timing review, promote its derived timeline into the Godot production controller.

## Final recommendation

Do not patch the current production timeline to accommodate the defective audio. The lowest-risk, highest-fidelity solution is two clean pickups: Kevin re-records Turn 1 without “But,” and Khaled re-records Turn 4 in full. This preserves the approved narrative, avoids fabricated phonemes, and gives the lip-sync system a complete acoustic source.
