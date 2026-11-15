#!/usr/bin/env python3
"""Build the HOLOS four-turn timeline from a verified full-episode alignment.

This wrapper preserves the strict processor's default rejection behavior and
adds one explicit, user-approved ASR normalization: WhisperX `kilometers` is
accepted as the recognition spelling for approved transcript word `kilometres`.
Both forms remain recorded in the output.
"""
from __future__ import annotations

import hashlib
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/home/ubuntu")
import process_holos_aligned_audio as strict  # noqa: E402

ALIGNMENT = Path("/home/ubuntu/output/HOLOS_FullEpisode_WhisperX_Aligned.json")
MP3 = Path("/home/ubuntu/HOLOS_Episode_1_The_Moon_Has_Anger_Issues_FULL.mp3")
REVIEW_WAV = Path("/home/ubuntu/output/HOLOS_Episode1_four_turn_review.wav")
TIMELINE = Path("/home/ubuntu/output/HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json")
MANIFEST = Path("/home/ubuntu/output/HOLOS_Episode1_four_turn_review_manifest.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    aligned = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    words = []
    for segment in aligned.get("segments", []):
        words.extend(
            w for w in segment.get("words", [])
            if w.get("word") and w.get("start") is not None and w.get("end") is not None
        )
    exchange = words[:33]
    if len(exchange) != 33:
        raise RuntimeError(f"Expected 33 exchange words; got {len(exchange)}")

    observed = [strict.normalize_token(str(w["word"])) for w in exchange]
    expected = strict.approved_tokens()
    normalization_pairs = []
    for i, (obs, exp) in enumerate(zip(observed, expected)):
        if obs == exp:
            continue
        if obs == "kilometers" and exp == "kilometres":
            normalization_pairs.append({"index": i, "asr": obs, "approved": exp})
            exchange[i] = dict(exchange[i])
            exchange[i]["asr_word"] = exchange[i]["word"]
            exchange[i]["word"] = "kilometres"
            continue
        raise RuntimeError(f"Unapproved transcript mismatch at index {i}: {obs!r} != {exp!r}")

    if len(normalization_pairs) != 2:
        raise RuntimeError(f"Expected exactly two approved ASR normalizations; got {normalization_pairs}")

    # The word field now follows the approved transcript, while asr_word is
    # retained where a normalization was applied. Acoustic timings are unchanged.
    strict.verify_transcript(exchange)
    events = strict.build_events(exchange)
    for event in events:
        if event.get("source_word") == "kilometres":
            event["asr_word"] = "kilometers"
            event["normalization"] = "accepted_user_approved_asr_spelling_normalization"

    document = {
        "status": "acoustic word boundaries accepted; internal phoneme boundaries are estimates",
        "source_mp3": str(MP3),
        "source_mp3_sha256": sha256(MP3),
        "alignment_source": str(ALIGNMENT),
        "alignment_source_sha256": sha256(ALIGNMENT),
        "derived_review_wav": str(REVIEW_WAV),
        "approved_transcript": [{"speaker": s, "text": t} for s, t in strict.APPROVED_TURNS],
        "source_timebase_seconds": {"start": 0.091, "end": 16.916},
        "speech_word_envelope_seconds": {"start": 0.191, "end": 16.816},
        "asr_normalizations": normalization_pairs,
        "alignment_method": "WhisperX tiny.en transcription plus wav2vec2 English word/character alignment; dictionary-based internal phoneme subdivision",
        "events": events,
        "limitations": [
            "WhisperX word/character boundaries are acoustically aligned.",
            "Internal phoneme boundaries are dictionary-based subdivisions and are not dedicated phoneme-aligner output.",
            "The approved transcript retains kilometres; the two WhisperX kilometers outputs are retained as explicit user-approved normalizations.",
        ],
    }
    tmp_timeline = TIMELINE.with_suffix(".json.tmp")
    tmp_timeline.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp_timeline.replace(TIMELINE)

    with wave.open(str(REVIEW_WAV), "rb") as wav:
        wav_info = {
            "sample_rate_hz": wav.getframerate(),
            "channels": wav.getnchannels(),
            "sample_width_bytes": wav.getsampwidth(),
            "frames": wav.getnframes(),
            "duration_seconds": wav.getnframes() / wav.getframerate(),
        }
    manifest = {
        "source_mp3": str(MP3),
        "source_mp3_sha256": sha256(MP3),
        "review_wav": str(REVIEW_WAV),
        "review_wav_sha256": sha256(REVIEW_WAV),
        "review_wav_format": wav_info,
        "extract_start_seconds": 0.091,
        "extract_end_seconds": 16.916,
        "speech_start_seconds": 0.191,
        "speech_end_seconds": 16.816,
        "timeline": str(TIMELINE),
        "timeline_sha256": sha256(TIMELINE),
        "transcript_status": "approved after pronunciation review",
        "asr_normalizations": normalization_pairs,
        "leading_but": "absent",
        "final_phrase": "away from you present",
        "godot_integration": "not performed",
    }
    tmp_manifest = MANIFEST.with_suffix(".json.tmp")
    tmp_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tmp_manifest.replace(MANIFEST)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

