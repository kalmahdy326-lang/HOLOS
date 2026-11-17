#!/usr/bin/env python3
"""Validate the committed HOLOS Milestone 5.1 four-turn handoff using stdlib only.

This checks repository artifacts, not the absent WAV bytes, full production audio,
character rigs, or visual lip-sync. Run from any directory:
  python tools/validate_milestone_5_1_handoff.py
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoffs/milestone-5-1-2026-11-15"
ABSOLUTE = HANDOFF / "HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json"
RELATIVE = HANDOFF / "HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json"
MANIFEST = HANDOFF / "HOLOS_Episode1_four_turn_review_manifest.json"
EXPECTED_SOURCE_SHA256 = "e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f"
EXPECTED_OFFSET = 0.091
EXPECTED_TURNS = [
    ("KEVIN", "Tell me again why we're living inside a dead rock?"),
    ("KHALED", "Because the rock is interesting."),
    ("KEVIN", "It's 380,000 kilometres from the nearest decent restaurant."),
    ("KHALED", "The nearest restaurant is also 380,000 kilometres away from you."),
]
VISEMES = {"rest", "closed", "open", "wide", "round", "teeth"}


class ValidationError(Exception):
    pass


def load(path: Path) -> dict:
    if not path.is_file():
        raise ValidationError(f"Missing required handoff file: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"Expected a JSON object: {path}")
    return value


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_timeline(document: dict, label: str, expected_timebase: str) -> list[dict]:
    check(document.get("schema_version") == 1, f"{label}: schema_version must be 1")
    check(document.get("source_mp3_sha256") == EXPECTED_SOURCE_SHA256,
          f"{label}: source MP3 SHA-256 does not match approved source")
    turns = document.get("approved_transcript")
    check(isinstance(turns, list), f"{label}: approved_transcript must be an array")
    actual_turns = [(turn.get("speaker"), turn.get("text")) for turn in turns if isinstance(turn, dict)]
    check(actual_turns == EXPECTED_TURNS, f"{label}: approved four-turn transcript/speaker order changed")
    timebase = document.get("source_timebase_seconds", {})
    check(isinstance(timebase, dict), f"{label}: missing source_timebase_seconds")
    check(float(timebase.get("start", -1)) >= 0, f"{label}: invalid timebase start")
    check(float(timebase.get("end", 0)) > float(timebase.get("start", 0)), f"{label}: invalid timebase end")
    if expected_timebase == "absolute":
        check(math.isclose(float(timebase["start"]), EXPECTED_OFFSET, abs_tol=1e-6),
              "absolute timeline: unexpected source-time start")
    else:
        check(math.isclose(float(timebase["start"]), 0.0, abs_tol=1e-6),
              "relative timeline: expected zero-based timebase")

    events = document.get("events")
    check(isinstance(events, list) and len(events) == 189,
          f"{label}: expected exactly 189 events, got {len(events) if isinstance(events, list) else 'non-array'}")
    previous_start = -math.inf
    for index, event in enumerate(events):
        check(isinstance(event, dict), f"{label}: event {index} is not an object")
        speaker = event.get("speaker")
        check(speaker in {"KEVIN", "KHALED"}, f"{label}: event {index} has unexpected speaker {speaker!r}")
        start, end = event.get("start"), event.get("end")
        check(isinstance(start, (int, float)) and isinstance(end, (int, float)),
              f"{label}: event {index} has non-numeric bounds")
        check(math.isfinite(start) and math.isfinite(end) and start >= 0 and end > start,
              f"{label}: event {index} has invalid bounds")
        check(start >= previous_start - 1e-6, f"{label}: event {index} is out of chronological order")
        check(event.get("viseme") in VISEMES, f"{label}: event {index} has unsupported viseme")
        if event.get("phoneme") == "SIL":
            check(event.get("viseme") == "rest", f"{label}: SIL event {index} must map to rest")
        previous_start = start
    return events


def main() -> int:
    try:
        absolute = load(ABSOLUTE)
        relative = load(RELATIVE)
        manifest = load(MANIFEST)
        abs_events = validate_timeline(absolute, "absolute timeline", "absolute")
        rel_events = validate_timeline(relative, "relative timeline", "relative")
        check(len(abs_events) == len(rel_events), "timeline event counts differ")
        check(manifest.get("source_mp3_sha256") == EXPECTED_SOURCE_SHA256,
              "manifest source MP3 SHA-256 mismatch")
        check(math.isclose(float(manifest.get("relative_timeline_offset_seconds", -1)),
                           EXPECTED_OFFSET, abs_tol=1e-9), "manifest review offset mismatch")
        check(manifest.get("transcript_status") == "approved after pronunciation review",
              "manifest transcript approval status mismatch")

        for index, (absolute_event, relative_event) in enumerate(zip(abs_events, rel_events)):
            for field in ("speaker", "phoneme", "viseme", "source_word"):
                check(absolute_event.get(field) == relative_event.get(field),
                      f"event {index}: {field} differs between timelines")
            for field in ("start", "end", "acoustic_word_start", "acoustic_word_end"):
                if field in absolute_event or field in relative_event:
                    check(field in absolute_event and field in relative_event,
                          f"event {index}: {field} missing from one timeline")
                    delta = float(absolute_event[field]) - float(relative_event[field])
                    check(math.isclose(delta, EXPECTED_OFFSET, abs_tol=2e-6),
                          f"event {index}: {field} offset is {delta}, expected {EXPECTED_OFFSET}")

        print("PASS: both schema-versioned timelines load")
        print("PASS: exact approved four-turn transcript and speaker order preserved")
        print("PASS: 189 events per timeline; bounds, ordering, visemes and silence checked")
        print("PASS: absolute/relative timelines differ by the recorded 0.091-second offset")
        print("PASS: source MP3 hash and manifest provenance agree")
        print("LIMIT: review WAV bytes are not present; their conflicting hashes remain unresolved")
        print("LIMIT: internal phoneme subdivisions remain dictionary-based estimates")
        print("LIMIT: this does not validate the full episode, Godot runtime, rigs, or rendered lip-sync")
        return 0
    except (ValidationError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
