#!/usr/bin/env python3
"""Dependency-free structural validator for the HOLOS intro-theme package.

Checks files and declared timing only. It cannot assess musical quality,
licensing, generated audio, vocal delivery, or audiovisual synchronization.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "lyrics/holos-intro-v1.txt",
    "prompts/suno-style-v1.txt",
    "prompts/suno-exclude-v1.txt",
    "prompts/suno-master-instructions-v1.md",
    "arrangement/arrangement-v1.md",
    "arrangement/tempo-map-v1.json",
    "animation/cue-sheet-v1.csv",
    "animation/synchronization-notes-v1.md",
    "audio/README.md",
    "licenses/THIRD_PARTY_NOTICES.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    lyrics = (ROOT / "lyrics/holos-intro-v1.txt").read_text(encoding="utf-8")
    for marker in ("[CINEMATIC INTRO", "[VERSE 1]", "[PRE-CHORUS]", "[CHORUS]", "[FINAL CHORUS]", "HOLOS!"):
        if marker not in lyrics:
            fail(f"lyrics missing required marker: {marker}")
    if "Project author: Khaled AL-MAHDY" not in lyrics:
        fail("lyrics must preserve project attribution")

    tempo = json.loads((ROOT / "arrangement/tempo-map-v1.json").read_text(encoding="utf-8"))
    if tempo.get("status") != "proposed_not_audio_verified":
        fail("tempo map must remain provisional until measured against audio")
    target = float(tempo["target_duration_seconds"])
    sections = tempo["sections"]
    if not sections:
        fail("tempo map has no sections")
    previous_end = 0.0
    for section in sections:
        start, end = float(section["start_seconds"]), float(section["end_seconds"])
        if abs(start - previous_end) > 1e-6:
            fail(f"tempo-map gap/overlap before {section['name']}")
        if end <= start:
            fail(f"invalid duration for {section['name']}")
        previous_end = end
    if abs(previous_end - target) > 1e-6:
        fail("tempo-map end does not equal target duration")

    with (ROOT / "animation/cue-sheet-v1.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        fail("cue sheet is empty")
    previous_end = 0.0
    for index, row in enumerate(rows, start=1):
        start, end = float(row["start_seconds"]), float(row["end_seconds"])
        if abs(start - previous_end) > 1e-6:
            fail(f"cue-sheet gap/overlap at row {index}")
        if end <= start:
            fail(f"invalid cue duration at row {index}")
        previous_end = end
    if abs(previous_end - target) > 1e-6:
        fail("cue-sheet end does not equal target duration")

    style = (ROOT / "prompts/suno-style-v1.txt").read_text(encoding="utf-8").strip()
    if len(style) < 100:
        fail("style prompt unexpectedly short")

    print("PASS: HOLOS intro-theme source package is structurally complete.")
    print(f"Sections: {len(sections)}; cues: {len(rows)}; proposed duration: {target:.2f}s")
    print("LIMITATION: not audio, licensing, musical-quality or sync acceptance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
