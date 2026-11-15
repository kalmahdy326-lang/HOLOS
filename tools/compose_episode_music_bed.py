#!/usr/bin/env python3
"""Place intro and credits themes into one duration-exact music bed WAV.

The existing HOLOS FFmpeg assembler accepts one music stem. This helper places
separate intro/outro WAVs at their final cut positions and leaves the dialogue
middle silent on the music stem. It never modifies either source file.
"""
from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import wave
from typing import Any


class MusicBedError(ValueError):
    """Raised for unsupported audio format or invalid cue placement."""


def read_pcm16_stereo(path: Path) -> tuple[int, array]:
    if not path.is_file():
        raise MusicBedError(f"Music source does not exist: {path}")
    try:
        with wave.open(str(path), "rb") as src:
            channels = src.getnchannels()
            sample_width = src.getsampwidth()
            sample_rate = src.getframerate()
            frame_count = src.getnframes()
            raw = src.readframes(frame_count)
    except (wave.Error, OSError) as exc:
        raise MusicBedError(f"Could not read WAV source {path}: {exc}") from exc
    if channels != 2 or sample_width != 2 or sample_rate != 48_000:
        raise MusicBedError(
            f"{path} must be stereo, 48 kHz, signed 16-bit PCM; got "
            f"channels={channels}, sample_width={sample_width}, sample_rate={sample_rate}."
        )
    samples = array("h")
    samples.frombytes(raw)
    if samples.itemsize != 2:
        raise MusicBedError("This Python runtime does not provide 16-bit signed short samples.")
    return sample_rate, samples


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compose_music_bed(
    intro_path: Path,
    outro_path: Path,
    output_path: Path,
    duration_seconds: float,
) -> dict[str, Any]:
    if not math.isfinite(duration_seconds) or duration_seconds <= 0:
        raise MusicBedError("duration_seconds must be a positive finite number.")
    if output_path.exists():
        raise MusicBedError(f"Refusing to overwrite existing music bed: {output_path}")
    report_path = output_path.with_suffix(output_path.suffix + ".manifest.json")
    if report_path.exists():
        raise MusicBedError(f"Refusing to overwrite music bed manifest: {report_path}")

    sample_rate, intro = read_pcm16_stereo(intro_path)
    outro_rate, outro = read_pcm16_stereo(outro_path)
    if sample_rate != outro_rate:
        raise MusicBedError("Intro and outro sample rates do not match.")

    total_frames = int(round(duration_seconds * sample_rate))
    intro_frames = len(intro) // 2
    outro_frames = len(outro) // 2
    if intro_frames + outro_frames > total_frames:
        raise MusicBedError(
            f"Intro ({intro_frames / sample_rate:.3f}s) and outro "
            f"({outro_frames / sample_rate:.3f}s) exceed the final duration "
            f"({duration_seconds:.3f}s)."
        )

    bed = array("h", [0]) * (total_frames * 2)
    bed[0:len(intro)] = intro
    outro_start_frame = total_frames - outro_frames
    outro_start_sample = outro_start_frame * 2
    bed[outro_start_sample:outro_start_sample + len(outro)] = outro

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as dst:
        dst.setnchannels(2)
        dst.setsampwidth(2)
        dst.setframerate(sample_rate)
        dst.writeframes(bed.tobytes())

    report = {
        "output": str(output_path.resolve()),
        "duration_seconds": total_frames / sample_rate,
        "sample_rate_hz": sample_rate,
        "channels": 2,
        "sample_format": "signed 16-bit PCM",
        "intro": {
            "path": str(intro_path.resolve()),
            "sha256": sha256_file(intro_path),
            "start_seconds": 0.0,
            "end_seconds": intro_frames / sample_rate,
        },
        "credits_outro": {
            "path": str(outro_path.resolve()),
            "sha256": sha256_file(outro_path),
            "start_seconds": outro_start_frame / sample_rate,
            "end_seconds": total_frames / sample_rate,
        },
        "music_gain_db_under_dialogue": -18.0,
        "output_sha256": sha256_file(output_path),
        "source_modified": False,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intro", type=Path, required=True)
    parser.add_argument("--outro", type=Path, required=True, help="Credit-roll theme WAV.")
    parser.add_argument("--duration-seconds", type=float, required=True,
                        help="Exact final episode duration from the approved frame plan.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = compose_music_bed(args.intro.resolve(), args.outro.resolve(),
                               args.output.resolve(), args.duration_seconds)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
