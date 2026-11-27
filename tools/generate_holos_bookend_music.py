#!/usr/bin/env python3
"""Render original HOLOS intro and credit-roll music with local synthesis.

This is a deterministic, locally generated draft theme: no external service,
model, sample library, or third-party audio asset is used. Requires NumPy and
writes 48 kHz, stereo, 16-bit PCM WAV files plus a SHA-256 manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import wave

import numpy as np

SAMPLE_RATE = 48_000
BPM = 80
BEAT_SECONDS = 60.0 / BPM
BAR_SECONDS = 4 * BEAT_SECONDS

# Dm9 – Bbmaj7 – Fadd9 – Csus2; a curious, slightly mischievous space tone.
CHORDS = [
    (50, [57, 60, 64, 69]),  # D bass + A C E A
    (46, [53, 57, 62, 65]),  # Bb + F A D F
    (41, [48, 53, 57, 60, 62]),  # F + C F A C D
    (48, [55, 60, 62, 67]),  # C + G C D G
]

# A compact four-bar signature motif, in MIDI note numbers.
MOTIF = [
    (0, 0.00, 74, 0.72), (0, 1.50, 69, 0.55), (0, 3.00, 72, 0.48),
    (1, 0.00, 77, 0.72), (1, 1.50, 74, 0.50), (1, 3.00, 69, 0.48),
    (2, 0.00, 72, 0.68), (2, 1.00, 74, 0.42), (2, 2.50, 77, 0.50),
    (3, 0.00, 79, 0.62), (3, 1.50, 77, 0.50), (3, 3.00, 74, 0.72),
]


def midi_hz(note: int) -> float:
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def pan_gains(pan: float) -> tuple[float, float]:
    angle = (pan + 1.0) * math.pi / 4.0
    return math.cos(angle), math.sin(angle)


def add_voice(
    stereo: np.ndarray,
    start: float,
    duration: float,
    frequency: float,
    amplitude: float,
    *,
    kind: str,
    pan: float = 0.0,
    detune_cents: float = 0.0,
) -> None:
    start_index = max(0, int(round(start * SAMPLE_RATE)))
    end_index = min(stereo.shape[1], int(round((start + duration) * SAMPLE_RATE)))
    count = end_index - start_index
    if count <= 0:
        return
    t = np.arange(count, dtype=np.float64) / SAMPLE_RATE
    actual_f = frequency * (2.0 ** (detune_cents / 1200.0))
    phase = 2.0 * np.pi * actual_f * t
    fundamental = np.sin(phase)
    if kind == "pad":
        signal = 0.62 * fundamental + 0.22 * np.sin(2.0 * phase + 0.2) + 0.08 * np.sin(3.0 * phase + 0.6)
        attack = min(0.7, duration * 0.30)
        release = min(0.9, duration * 0.35)
        env = np.minimum(1.0, t / max(attack, 1e-6))
        env *= np.minimum(1.0, (duration - t) / max(release, 1e-6))
        env *= 0.88 + 0.12 * np.sin(2.0 * np.pi * 0.17 * t + 0.3)
    elif kind == "pluck":
        signal = 0.72 * fundamental + 0.20 * np.sin(2.0 * phase + 0.15) + 0.08 * np.sin(3.0 * phase)
        attack = min(0.018, duration * 0.10)
        env = np.minimum(1.0, t / max(attack, 1e-6)) * np.exp(-3.8 * t / max(duration, 0.15))
    elif kind == "bass":
        signal = 0.82 * fundamental + 0.18 * np.sin(2.0 * phase)
        env = np.minimum(1.0, t / 0.025) * np.exp(-1.5 * t / max(duration, 0.1))
    elif kind == "bell":
        signal = 0.70 * fundamental + 0.22 * np.sin(2.76 * phase + 0.1) + 0.08 * np.sin(4.1 * phase)
        env = np.minimum(1.0, t / 0.006) * np.exp(-5.2 * t / max(duration, 0.1))
    else:
        raise ValueError(f"Unsupported voice kind: {kind}")
    left_gain, right_gain = pan_gains(max(-1.0, min(1.0, pan)))
    voice = (signal * env * amplitude).astype(np.float32)
    stereo[0, start_index:end_index] += voice * left_gain
    stereo[1, start_index:end_index] += voice * right_gain


def add_soft_kick(stereo: np.ndarray, start: float, amplitude: float = 0.09) -> None:
    duration = 0.28
    start_index = int(round(start * SAMPLE_RATE))
    end_index = min(stereo.shape[1], start_index + int(round(duration * SAMPLE_RATE)))
    if end_index <= start_index:
        return
    t = np.arange(end_index - start_index, dtype=np.float64) / SAMPLE_RATE
    # A soft low-frequency bloom, not a hard drum hit.
    phase = 2.0 * np.pi * (48.0 * t - 14.0 * t * t)
    signal = np.sin(phase) * np.exp(-12.0 * t) * amplitude
    stereo[0, start_index:end_index] += signal.astype(np.float32) * 0.70
    stereo[1, start_index:end_index] += signal.astype(np.float32) * 0.70


def render_piece(bars: int, *, credit_roll: bool) -> np.ndarray:
    duration = bars * BAR_SECONDS
    stereo = np.zeros((2, int(round(duration * SAMPLE_RATE))), dtype=np.float32)
    for bar in range(bars):
        chord_index = bar % len(CHORDS)
        bass_note, chord_notes = CHORDS[chord_index]
        bar_start = bar * BAR_SECONDS
        # Wide, slow warm synth bed; restrained low end leaves space for speech.
        for index, note in enumerate(chord_notes):
            pan = (-0.58, -0.20, 0.22, 0.58, 0.08)[index % 5]
            add_voice(stereo, bar_start, BAR_SECONDS + 0.06, midi_hz(note), 0.045,
                      kind="pad", pan=pan, detune_cents=(-4.0 if index % 2 else 3.0))
        add_voice(stereo, bar_start, BAR_SECONDS, midi_hz(bass_note), 0.095,
                  kind="bass", pan=0.0)

        # Pulse on beats one and three, gradually introduced in the opening.
        if credit_roll or bar >= 1:
            for beat in (0, 2):
                add_soft_kick(stereo, bar_start + beat * BEAT_SECONDS,
                              amplitude=0.070 if credit_roll else 0.055)

        # Reprise the signature motif; the credits arrangement grows gently, then resolves.
        motif_bar = bar % 4
        motif_gain = 0.105 if (not credit_roll or bar < bars - 2) else 0.075
        for note_bar, beat, note, duration_beats in MOTIF:
            if note_bar != motif_bar:
                continue
            start = bar_start + beat * BEAT_SECONDS
            note_duration = duration_beats * BEAT_SECONDS
            if credit_roll and bar >= 4:
                note_duration *= 1.15
            add_voice(stereo, start, note_duration, midi_hz(note), motif_gain,
                      kind="bell", pan=(-0.25 if int(beat * 2) % 2 == 0 else 0.25))

        # Sparse answering plucks keep the motif playful rather than ominous.
        if bar % 2 == 1:
            answer_note = (67, 69, 72, 74)[bar % 4]
            add_voice(stereo, bar_start + 2.25 * BEAT_SECONDS, 0.60,
                      midi_hz(answer_note), 0.048, kind="pluck", pan=0.38)

    # Short stereo reflections add a little space without obscuring dialogue.
    dry = stereo.copy()
    delay_a = int(0.115 * SAMPLE_RATE)
    delay_b = int(0.247 * SAMPLE_RATE)
    stereo[:, delay_a:] += dry[::-1, :-delay_a] * 0.11
    stereo[:, delay_b:] += dry[:, :-delay_b] * 0.055

    # Intro ends with a soft musical resolve; credits end with a longer fade.
    fade_seconds = 1.5 if not credit_roll else 3.5
    fade_count = int(fade_seconds * SAMPLE_RATE)
    if fade_count:
        fade = np.linspace(1.0, 0.0, fade_count, dtype=np.float32)
        stereo[:, -fade_count:] *= fade
    peak = float(np.max(np.abs(stereo))) if stereo.size else 0.0
    if peak > 0:
        stereo *= (0.68 / peak)
    return np.clip(stereo, -0.98, 0.98)


def write_wav(path: Path, samples: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = np.round(samples.T * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SAMPLE_RATE)
        out.writeframes(pcm.tobytes())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    intro_path = output_dir / "holos_intro_theme.wav"
    credits_path = output_dir / "holos_credits_theme.wav"
    intro = render_piece(4, credit_roll=False)
    credits = render_piece(8, credit_roll=True)
    write_wav(intro_path, intro)
    write_wav(credits_path, credits)
    manifest = {
        "composition": "Original deterministic HOLOS cosmic-mystery bookend theme",
        "generation": "Local additive synthesis; no external AI, samples, or third-party music",
        "key_center": "D minor / F major colors",
        "tempo_bpm": BPM,
        "sample_rate_hz": SAMPLE_RATE,
        "channels": 2,
        "sample_format": "signed 16-bit PCM",
        "tracks": [
            {"role": "intro", "path": intro_path.name, "duration_seconds": 4 * BAR_SECONDS,
             "sha256": sha256_file(intro_path)},
            {"role": "credits_outro", "path": credits_path.name, "duration_seconds": 8 * BAR_SECONDS,
             "sha256": sha256_file(credits_path)},
        ],
        "mix_note": "Standalone theme stems; set music gain below dialogue and align/fade to the final cut.",
    }
    manifest_path = output_dir / "holos_bookend_music_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
