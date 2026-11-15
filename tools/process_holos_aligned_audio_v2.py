#!/usr/bin/env python3
"""HOLOS Milestone 5.1 strict audio processor (corrected v2.1).

This script deliberately refuses to invent dialogue. It performs:
1. WAV format inspection.
2. WhisperX transcription and wav2vec2 word/character alignment.
3. Exact token verification against the approved transcript.
4. 48 kHz stereo 24-bit PCM WAV normalization only after transcript acceptance.
5. Phoneme-labelled viseme timeline generation from acoustically aligned words.

Important limitation (preserved, not weakened):
WhisperX word/character alignment is not a dedicated phoneme-level aligner.
Internal phoneme intervals are dictionary-based subdivisions inside acoustically
aligned word intervals and are labelled as estimates in the output JSON.
Word boundaries are acoustically aligned; internal phoneme boundaries are not.

Changelog
---------
v2 (relative to the supplied script):
1. Transactional output promotion is now actually used. The supplied script
   defined promote_outputs() but never called it: main() wrote the normalized
   WAV directly to its final path and then replaced the timeline separately.
   Both outputs are now staged next to their destinations, validated, and
   committed together with backup and rollback.
2. Staged files live in the destination directories: os.replace() cannot
   rename across filesystems, so staging inside /tmp risked EXDEV failures.
3. Accurate failure reporting: messages state exactly what was created,
   replaced, restored, or left behind.
4. --align-model is now passed through to whisperx.load_align_model
   ("wav2vec2"/"default" select the WhisperX default alignment model).
5. assert statements replaced with explicit RuntimeError checks.
6. inspect_wav rejects zero-frame files; the staged WAV is re-inspected after
   ffmpeg normalization and must be 24-bit.
7. The staged timeline is schema-validated before promotion (chronology,
   positive durations, supported visemes, approved speakers, no unapproved
   "But", required fourth-line words, events within the measured duration).
8. --self-test runs safeguard regression tests without whisperx/pronouncing.

v2.1 (crash safety and expanded failure-mode tests):
1. Interrupted-commit recovery. A commit journal (JSON, written atomically
   before any change) records the destinations, whether each existed before,
   its backup path, and the staged paths. promote_outputs() deletes the
   journal only after both commits succeed. If a process or machine crash
   leaves a journal behind, the next run (or --recover) restores the previous
   outputs from backups, removes outputs that were newly created, cleans up
   staged files, and deletes the journal. After a successful recovery the
   destinations are guaranteed to be in their pre-run state; the run then
   proceeds normally. If rollback during a failed promotion is itself
   incomplete, the journal is deliberately KEPT so recovery can retry.
2. --recover flag to run recovery explicitly without processing audio.
3. Self-tests extended to cover: failure after the first output replacement,
   failure during rollback, and recovery after an interrupted commit, in
   addition to the normal promotion success and failure paths.

On any transcript, format or alignment failure, no output WAV or timeline is
committed. The current benchmark input is expected to FAIL because it contains
a leading "But" and an incomplete fourth line.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path
from typing import Any, Callable

try:
    import pronouncing
except ImportError:  # pragma: no cover
    pronouncing = None

try:
    import whisperx
except ImportError:  # pragma: no cover
    whisperx = None


APPROVED_TURNS = [
    ("KEVIN", "Tell me again why we're living inside a dead rock?"),
    ("KHALED", "Because the rock is interesting."),
    ("KEVIN", "It's 380,000 kilometres from the nearest decent restaurant."),
    ("KHALED", "The nearest restaurant is also 380,000 kilometres away from you."),
]

EXPECTED_SPEAKERS = [speaker for speaker, _ in APPROVED_TURNS]
EXPECTED_TEXT = " ".join(text for _, text in APPROVED_TURNS)
SUPPORTED_VISEMES = {"rest", "closed", "open", "wide", "round", "teeth"}
VALID_SPEAKERS = {"KEVIN", "KHALED"}
# Events may not exceed the measured audio duration by more than this epsilon.
DURATION_EPSILON_SECONDS = 0.05

# Keep the vocabulary in lockstep with godot/holos_timeline.gd. These are
# semantic viseme labels; a character-specific rig maps them to real controls.
VISEME_TO_GODOT = {name: name for name in ("rest", "closed", "open", "wide", "round", "teeth")}
SPEAKER_NORMALIZE = {"KEVIN": "KEVIN", "KHALED": "KHALED"}


def build_godot_timeline(
    events: list[dict[str, Any]],
    audio_duration: float | None = None,
    version: int = 1,
) -> dict[str, Any]:
    """Serialize validated phoneme events for the existing HolosTimeline consumer.

    Events remain flat because the Godot consumer evaluates phoneme intervals;
    grouping turns would discard the per-phoneme animation timing.
    """
    if version != 1:
        raise ValueError(f"Unsupported Godot timeline schema version: {version}")
    converted: list[dict[str, Any]] = []
    previous_start = -1.0
    for index, event in enumerate(events):
        speaker = SPEAKER_NORMALIZE.get(str(event.get("speaker", "")).upper())
        viseme = VISEME_TO_GODOT.get(str(event.get("viseme", "")).lower())
        try:
            start, end = float(event["start"]), float(event["end"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid event timing at index {index}") from exc
        if speaker is None or viseme is None or not math.isfinite(start) or not math.isfinite(end):
            raise ValueError(f"Unsupported speaker, viseme, or timing at event {index}")
        if start < previous_start - 1e-6 or start < 0 or end <= start:
            raise ValueError(f"Invalid event ordering or duration at index {index}")
        if audio_duration is not None and end > audio_duration + DURATION_EPSILON_SECONDS:
            raise ValueError(f"Event {index} exceeds audio duration")
        converted.append({**event, "speaker": speaker, "viseme": viseme})
        previous_start = start
    return {"schema_version": version, "events": converted}
JOURNAL_SUFFIX = ".commit-journal.json"
JOURNAL_VERSION = 1


def normalize_token(value: str) -> str:
    """Normalize punctuation for strict transcript comparison.

    Commas inside numbers are removed on BOTH sides of the comparison, so an
    approved "380,000", an aligned "380,000", and an aligned "380000" all
    normalize to "380000". No other punctuation is folded into words.
    """
    value = value.lower().replace("\u2019", "'")
    value = re.sub(r"(?<=\d),(?=\d)", "", value)
    return re.sub(r"[^a-z0-9']", "", value)


def tokens(text: str) -> list[str]:
    pattern = r"\d{1,3}(?:,\d{3})+|[A-Za-z]+(?:'[A-Za-z]+)?|\d+"
    return [normalize_token(x) for x in re.findall(pattern, text)]


def approved_tokens() -> list[str]:
    return tokens(EXPECTED_TEXT)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_wav(path: Path, allowed_widths: tuple[int, ...] = (2, 3)) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_size == 0:
        raise RuntimeError(f"Missing or empty WAV: {path}")
    with wave.open(str(path), "rb") as wav:
        info = {
            "channels": wav.getnchannels(),
            "sample_rate_hz": wav.getframerate(),
            "sample_width_bytes": wav.getsampwidth(),
            "frames": wav.getnframes(),
            "duration_seconds": wav.getnframes() / wav.getframerate(),
            "compression": wav.getcomptype(),
        }
    if info["compression"] != "NONE":
        raise RuntimeError(f"Not uncompressed PCM WAV: {info}")
    if info["sample_rate_hz"] != 48000:
        raise RuntimeError(f"Sample rate must be 48000 Hz: {info}")
    if info["channels"] != 2:
        raise RuntimeError(f"Must be stereo: {info}")
    if info["frames"] <= 0:
        raise RuntimeError(f"WAV contains zero frames: {info}")
    if info["sample_width_bytes"] not in allowed_widths:
        raise RuntimeError(f"Unsupported PCM sample width: {info}")
    return info


# ---------------------------------------------------------------------------
# Commit journal and crash recovery
# ---------------------------------------------------------------------------


def journal_path_for(output_wav: Path) -> Path:
    return output_wav.with_name(output_wav.name + JOURNAL_SUFFIX)


def _fsync_file(path: Path) -> None:
    with path.open("r+b") as stream:
        os.fsync(stream.fileno())


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_journal(journal: Path, payload: dict[str, Any]) -> None:
    """Write the journal atomically: temp file + os.replace."""
    temp = journal.with_name(journal.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(payload, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, journal)
    _fsync_directory(journal.parent)


def read_journal(journal: Path) -> dict[str, Any] | None:
    if not journal.exists():
        return None
    try:
        payload = json.loads(journal.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Commit journal exists but is invalid; refusing to continue: {journal}") from exc
    if not isinstance(payload, dict) or payload.get("version") != JOURNAL_VERSION:
        raise RuntimeError(f"Commit journal version/shape is invalid; refusing to continue: {journal}")
    return payload


def recover_interrupted_promotion(
    output_wav: Path,
    output_timeline: Path,
) -> dict[str, list[str]] | None:
    """Detect and undo an interrupted promotion.

    Called automatically at startup and by --recover. Returns a summary of the
    recovery actions, or None when no interrupted promotion was found.

    Guarantees after a successful recovery: every destination is either
    restored to its pre-run content (backup restored) or removed (it did not
    exist before the interrupted run), and no staged files remain.
    """
    journal = journal_path_for(output_wav)
    payload = read_journal(journal)
    if payload is None:
        return None
    expected = {output_wav.resolve(), output_timeline.resolve()}
    entries = payload.get("destinations")
    staged_entries = payload.get("staged")
    if not isinstance(entries, list) or len(entries) != 2 or not isinstance(staged_entries, list) or len(staged_entries) != 2:
        raise RuntimeError(f"Invalid commit journal structure; preserving it for inspection: {journal}")
    seen: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("existed"), bool):
            raise RuntimeError(f"Invalid journal destination; preserving it: {journal}")
        try:
            destination = Path(entry["path"]).resolve()
            backup = Path(entry["backup"]).resolve()
        except (KeyError, TypeError, OSError) as exc:
            raise RuntimeError(f"Invalid journal path; preserving it: {journal}") from exc
        if destination not in expected or destination in seen or backup == destination or backup in expected:
            raise RuntimeError(f"Journal paths do not match requested outputs; preserving it: {journal}")
        seen.add(destination)
    staged_paths = [Path(item).resolve() for item in staged_entries if isinstance(item, str)]
    expected_staged = {
        output_wav.with_name(output_wav.name + ".staged").resolve(),
        output_timeline.with_name(output_timeline.name + ".staged").resolve(),
    }
    expected_backup_names = {p.name + ".bak" for p in expected}
    backup_paths = [Path(entry["backup"]).resolve() for entry in entries]
    if (seen != expected or set(staged_paths) != expected_staged
            or len(set(backup_paths)) != 2
            or any(p.name not in expected_backup_names
                   or not p.parent.is_relative_to(output_wav.parent.resolve())
                   for p in backup_paths)):
        raise RuntimeError(f"Journal paths do not match requested outputs; preserving it: {journal}")
    summary: dict[str, list[str]] = {"restored": [], "removed": [], "left": []}
    try:
        for entry in payload.get("destinations", []):
            destination = Path(entry["path"])
            backup = Path(entry["backup"]) if entry.get("backup") else None
            existed_before = bool(entry.get("existed", False))
            if backup is not None and backup.exists():
                os.replace(backup, destination)
                summary["restored"].append(str(destination))
            elif not existed_before and destination.exists():
                destination.unlink()
                summary["removed"].append(str(destination))
            else:
                # Destination holds its pre-run content (no replace reached it,
                # or the backup was externally deleted). Nothing to undo.
                summary["left"].append(str(destination))
        for staged in payload.get("staged", []):
            staged_path = Path(staged)
            if staged_path.exists():
                staged_path.unlink()
    except Exception as exc:
        # The journal is intentionally kept so recovery can be retried.
        raise RuntimeError(
            f"Interrupted-promotion recovery failed; journal kept at {journal}. "
            f"Inspect the output directory, then re-run with --recover. Error: {exc}"
        ) from exc
    journal.unlink()
    return summary


def promote_outputs(
    staged_wav: Path,
    staged_timeline: Path,
    output_wav: Path,
    output_timeline: Path,
    backup_dir: Path,
    fault_hook: Callable[[str], None] | None = None,
) -> dict[str, list[str]]:
    """Commit both outputs or restore the previous destinations on failure.

    Staged files live in the same directories as their destinations, so
    os.replace() is an atomic same-filesystem rename. A commit journal is
    written before any change so a crash between the two commits can be
    recovered by recover_interrupted_promotion(). If any commit fails, every
    committed destination is restored from its backup (or removed if it did
    not exist before), staged files are cleaned up, and the journal is
    deleted. If rollback itself fails, the journal is kept for recovery.

    fault_hook is a test-only instrumentation point invoked at named
    checkpoints ("after_backups", "after_commit:0", "after_commit:1",
    "rollback:start"). It is None in production runs.
    """
    destinations = [output_wav, output_timeline]
    staged = [staged_wav, staged_timeline]
    backups: dict[Path, Path | None] = {}
    committed: list[Path] = []
    backup_dir.mkdir(parents=True, exist_ok=True)
    journal = journal_path_for(output_wav)

    # Ensure staged bytes are durable before recording a recoverable transaction.
    for source in staged:
        _fsync_file(source)
        _fsync_directory(source.parent)

    # Journal first: it records the pre-state before anything is modified.
    write_journal(journal, {
        "version": JOURNAL_VERSION,
        "destinations": [
            {
                "path": str(destination),
                "existed": destination.exists(),
                "backup": str(backup_dir / (destination.name + ".bak")),
            }
            for destination in destinations
        ],
        "staged": [str(p) for p in staged],
    })
    try:
        for destination in destinations:
            if destination.exists():
                backup = backup_dir / (destination.name + ".bak")
                backup_dir.mkdir(parents=True, exist_ok=True)
                temp_backup = backup.with_name(backup.name + ".tmp")
                try:
                    temp_backup.unlink()
                except FileNotFoundError:
                    pass
                shutil.copy2(destination, temp_backup)
                _fsync_file(temp_backup)
                os.replace(temp_backup, backup)
                if os.name != "nt":
                    backup_fd = os.open(backup_dir, os.O_RDONLY)
                    try:
                        os.fsync(backup_fd)
                    finally:
                        os.close(backup_fd)
                backups[destination] = backup
            else:
                backups[destination] = None
        if fault_hook:
            fault_hook("after_backups")
        for index, (source, destination) in enumerate(zip(staged, destinations)):
            os.replace(source, destination)
            _fsync_directory(destination.parent)
            committed.append(destination)
            if fault_hook:
                fault_hook(f"after_commit:{index}")
    except Exception as exc:
        rollback_errors: list[str] = []
        try:
            if fault_hook:
                fault_hook("rollback:start")
            for destination in committed:
                if destination.exists():
                    destination.unlink()
                backup = backups.get(destination)
                if backup is not None and backup.exists():
                    os.replace(backup, destination)
            for source in staged:
                if source.exists():
                    source.unlink()
            journal.unlink()
        except Exception as rollback_exc:
            rollback_errors.append(str(rollback_exc))
        if rollback_errors:
            # Journal deliberately kept so the next run can recover.
            raise RuntimeError(
                "Output promotion failed AND rollback was incomplete; the commit journal was kept "
                f"at {journal} for recovery on the next run. Inspect destination files immediately. "
                f"Rollback errors: {rollback_errors}"
            ) from exc
        raise RuntimeError(
            "Output promotion failed; rollback completed and the commit journal was removed. "
            "Previously existing outputs were restored and no new partial outputs remain."
        ) from exc
    # The journal is the recovery authority until both replacements are durable.
    replaced = [str(d) for d in destinations if backups.get(d) is not None]
    created = [str(d) for d in destinations if backups.get(d) is None]
    journal.unlink()
    _fsync_directory(journal.parent)
    return {"replaced": replaced, "created": created}


# ---------------------------------------------------------------------------
# Transcript verification and event construction
# ---------------------------------------------------------------------------


def run_asr(audio_path: Path, model_name: str, device: str, compute_type: str) -> dict[str, Any]:
    if whisperx is None:
        raise RuntimeError("Missing dependency: whisperx. Run this script in the alignment venv.")
    print(f"[1/6] Loading WhisperX ASR model: {model_name}", flush=True)
    model = whisperx.load_model(model_name, device, compute_type=compute_type, language="en")
    print("[2/6] Transcribing source WAV", flush=True)
    audio = whisperx.load_audio(str(audio_path))
    result = model.transcribe(audio, batch_size=4, language="en")
    return {"result": result, "audio": audio}


def run_alignment(
    asr_result: dict[str, Any],
    model_name: str,
    device: str,
    audio: Any,
) -> dict[str, Any]:
    # "wav2vec2"/"default" select the WhisperX default English alignment model.
    # Any other value is passed through to load_align_model verbatim.
    align_model_arg: str | None = None
    if model_name.lower() not in {"wav2vec2", "default"}:
        align_model_arg = model_name
    print(f"[3/6] Loading WhisperX alignment model: {model_name}", flush=True)
    model_a, metadata = whisperx.load_align_model(
        language_code="en", device=device, model_name=align_model_arg
    )
    print("[4/6] Running acoustic word/character alignment", flush=True)
    aligned = whisperx.align(
        asr_result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=True,
    )
    return aligned


def flatten_words(aligned: dict[str, Any]) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []
    if aligned.get("word_segments"):
        words.extend(aligned["word_segments"])
    else:
        for segment in aligned.get("segments", []):
            words.extend(segment.get("words", []))
    return [w for w in words if w.get("word") and w.get("start") is not None and w.get("end") is not None]


def verify_transcript(words: list[dict[str, Any]]) -> None:
    observed = [normalize_token(str(w["word"])) for w in words]
    expected = approved_tokens()
    if observed != expected:
        # Precise first-difference diagnosis. Note: if the recognizer splits
        # "380,000" into two word tokens ("380", "000"), this comparison fails
        # by design; that output is ambiguous and must be reviewed manually.
        first_diff = next(
            (i for i, (a, b) in enumerate(zip(observed, expected)) if a != b),
            min(len(observed), len(expected)),
        )
        observed_context = observed[max(0, first_diff - 3): first_diff + 4]
        expected_context = expected[max(0, first_diff - 3): first_diff + 4]
        raise RuntimeError(
            "STRICT TRANSCRIPT FAILURE: aligned words do not exactly match the approved transcript.\n"
            f"First difference index: {first_diff}\n"
            f"Observed context: {observed_context}\n"
            f"Expected context: {expected_context}\n"
            "No output files were committed. Correct or re-record the WAV; do not fabricate words."
        )
    print("[5/6] PASS: exact approved transcript matched", flush=True)


def pronunciation_tokens(word: str) -> list[str]:
    """Return CMU-style phones without stress digits.

    380,000 is treated as an approved lexical number and expanded only for
    internal mouth-event labelling. The acoustic interval remains the aligned
    interval of the original number token.
    """
    if pronouncing is None:
        raise RuntimeError("Missing dependency: pronouncing. Install it in the alignment venv.")
    normalized = normalize_token(word)
    if normalized == "380000":
        parts = ["three", "hundred", "and", "eighty", "thousand"]
        phones: list[str] = []
        for part in parts:
            variants = pronouncing.phones_for_word(part)
            if not variants:
                raise RuntimeError(f"No pronunciation dictionary entry for {part!r}")
            phones.extend(re.sub(r"\d", "", p) for p in variants[0].split())
        return phones

    candidates = [normalized, normalized.replace("'", "")]
    if normalized == "it's":
        candidates.extend(["its", "it"])
    for candidate in candidates:
        variants = pronouncing.phones_for_word(candidate)
        if variants:
            return [re.sub(r"\d", "", p) for p in variants[0].split()]
    raise RuntimeError(f"No pronunciation dictionary entry for {word!r}")


def phone_to_viseme(phone: str) -> tuple[str, str]:
    p = re.sub(r"\d", "", phone.upper())
    if p in {"P", "B", "M"}:
        return "closed", "bilabial closure"
    if p in {"F", "V"}:
        return "teeth", "lip-to-teeth approximation"
    if p in {"TH", "DH"}:
        return "open", "interdental approximation"
    if p in {"T", "D", "N", "L", "S", "Z", "SH", "ZH", "CH", "JH", "R"}:
        return "wide", "narrow consonant"
    if p in {"K", "G", "NG"}:
        return "open", "velar consonant"
    if p in {"AO", "AW", "OW", "OY", "UH", "UW"}:
        return "round", "rounded vowel"
    if p in {"AE", "EH", "EY", "IY", "ER"}:
        return "wide", "front/rhotic vowel"
    return "open", "open vowel"


def expand_internal_events(word: dict[str, Any], speaker: str) -> list[dict[str, Any]]:
    raw_word = str(word["word"]).strip()
    start = float(word["start"])
    end = float(word["end"])
    if not math.isfinite(start) or not math.isfinite(end) or end <= start:
        raise RuntimeError(f"Invalid acoustic word interval: {word}")
    phones = pronunciation_tokens(raw_word)
    step = (end - start) / len(phones)
    score = float(word.get("score", word.get("confidence", 0.5)) or 0.5)
    events = []
    for index, phone in enumerate(phones):
        event_start = start + step * index
        event_end = end if index == len(phones) - 1 else start + step * (index + 1)
        viseme, category = phone_to_viseme(phone)
        if viseme not in SUPPORTED_VISEMES:
            raise RuntimeError(f"Internal error: unsupported viseme {viseme!r} for phone {phone!r}")
        events.append({
            "speaker": speaker,
            "start": round(event_start, 6),
            "end": round(event_end, 6),
            "phoneme": phone,
            "viseme": viseme,
            "category": category,
            "source_word": raw_word,
            "acoustic_word": raw_word,
            "acoustic_word_start": round(start, 6),
            "acoustic_word_end": round(end, 6),
            "acoustic_word_score": round(score, 6),
            "confidence": round(max(0.3, min(0.92, score)), 6),
            "verification_status": "WhisperX_acoustic_word_boundary_plus_dictionary_internal_estimate",
            "notes": "Word interval is acoustically aligned; internal phoneme interval is a dictionary-based subdivision, not a dedicated phoneme-aligner output."
        })
    return events


def map_words_to_speakers(aligned_words: list[dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    """Map aligned words to turns derived from the approved transcript.

    Turn boundaries are computed from the exact approved turn token arrays.
    For this transcript the counts are [10, 5, 8, 10]; they are derived here,
    not hard-coded, and the full observed sequence is re-verified per turn, so
    punctuation, contractions, and the number token cannot shift boundaries
    silently. Any mismatch fails safely before speaker labels are assigned.
    """
    approved_turn_tokens = [tokens(text) for _, text in APPROVED_TURNS]
    expected_lengths = [len(turn) for turn in approved_turn_tokens]
    if len(aligned_words) != sum(expected_lengths):
        raise RuntimeError(
            f"Expected {sum(expected_lengths)} aligned words after exact transcript match; got {len(aligned_words)}"
        )
    mapped: list[tuple[str, dict[str, Any]]] = []
    cursor = 0
    for (speaker, _), expected_turn, count in zip(APPROVED_TURNS, approved_turn_tokens, expected_lengths):
        observed_turn = [normalize_token(str(w["word"])) for w in aligned_words[cursor:cursor + count]]
        if observed_turn != expected_turn:
            raise RuntimeError(
                f"Ambiguous speaker mapping for {speaker}: observed {observed_turn}, expected {expected_turn}"
            )
        mapped.extend((speaker, word) for word in aligned_words[cursor:cursor + count])
        cursor += count
    return mapped


def build_events(aligned_words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mapped = map_words_to_speakers(aligned_words)
    events: list[dict[str, Any]] = []
    for speaker, word in mapped:
        events.extend(expand_internal_events(word, speaker))

    # Add reviewed acoustic gaps as rest events. These do not count as speech.
    # A gap spanning a speaker change is attributed to the outgoing speaker;
    # the mouth is at rest either way, so this does not affect animation.
    for (speaker_a, a), (speaker_b, b) in zip(mapped, mapped[1:]):
        gap_start = float(a["end"])
        gap_end = float(b["start"])
        if gap_end - gap_start >= 0.08:
            events.append({
                "speaker": speaker_a,
                "start": round(gap_start, 6),
                "end": round(gap_end, 6),
                "phoneme": "SIL",
                "viseme": "rest",
                "category": "acoustic word gap",
                "source_word": None,
                "confidence": 0.85,
                "verification_status": "WhisperX_word_gap_reviewed",
                "notes": "Gap between aligned words; inspect playback to distinguish breath from silence."
            })
    events.sort(key=lambda event: (event["start"], event["end"]))
    return events


def validate_timeline_document(document: dict[str, Any], audio_duration: float) -> dict[str, Any]:
    """Schema validation applied to the staged timeline before promotion."""
    events = document.get("events", [])
    if not events:
        raise RuntimeError("Timeline validation failed: no events")
    last = -1.0
    for i, event in enumerate(events):
        speaker = event.get("speaker")
        if speaker not in VALID_SPEAKERS:
            raise RuntimeError(f"Timeline validation failed at event {i}: speaker {speaker!r}")
        try:
            start = float(event["start"])
            end = float(event["end"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(f"Timeline validation failed at event {i}: invalid start/end") from exc
        if not math.isfinite(start) or not math.isfinite(end):
            raise RuntimeError(f"Timeline validation failed at event {i}: non-finite time")
        if start < 0 or end <= start:
            raise RuntimeError(f"Timeline validation failed at event {i}: non-positive duration")
        if start < last - 1e-6:
            raise RuntimeError(f"Timeline validation failed at event {i}: out of order")
        if event.get("viseme") not in SUPPORTED_VISEMES:
            raise RuntimeError(f"Timeline validation failed at event {i}: viseme {event.get('viseme')!r}")
        if str(event.get("phoneme", "")) == "SIL" and event.get("viseme") != "rest":
            raise RuntimeError(f"Timeline validation failed at event {i}: SIL must map to rest")
        if end > audio_duration + DURATION_EPSILON_SECONDS:
            raise RuntimeError(
                f"Timeline validation failed at event {i}: end {end} exceeds audio duration {audio_duration}"
            )
        last = start

    words = " ".join(str(e.get("source_word") or "") for e in events).lower()
    if re.search(r"\bbut\b", words):
        raise RuntimeError("Timeline validation failed: unapproved leading 'But' present")
    for required in ["tell", "interesting", "380,000", "kilometres", "away", "from", "you"]:
        if required not in words and required.replace(",", "") not in words:
            raise RuntimeError(f"Timeline validation failed: missing approved word {required!r}")
    return {
        "phoneme_count": sum(e["phoneme"] != "SIL" for e in events),
        "silence_event_count": sum(e["phoneme"] == "SIL" for e in events),
        "event_count": len(events),
    }


def normalize_audio(input_path: Path, staged_path: Path) -> None:
    """Write the normalized WAV to a STAGED path; promotion is separate."""
    staged_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-y", "-v", "error", "-i", str(input_path),
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(staged_path),
    ]
    subprocess.run(command, check=True)


def build_output_document(
    events: list[dict[str, Any]],
    input_wav: Path,
    output_wav: Path,
) -> dict[str, Any]:
    return {
        "status": "accepted only after exact approved transcript verification",
        "method": "WhisperX acoustic word/character alignment plus pronunciation-dictionary internal phoneme subdivision",
        "audio_reference": str(output_wav),
        "input_audio_reference": str(input_wav.resolve()),
        "approved_transcript": [{"speaker": s, "text": t} for s, t in APPROVED_TURNS],
        "source_sha256": sha256(input_wav.resolve()),
        "schema_version": 1,
        "events": build_godot_timeline(events)["events"],
        "limitations": [
            "WhisperX supplies acoustic word/character timing here, not dedicated phoneme timing.",
            "Internal phoneme boundaries are dictionary-based subdivisions inside aligned word intervals; they are estimates, not acoustically verified phoneme timings.",
            "No output is committed unless the observed transcript exactly matches the approved transcript.",
            "If the recognizer splits the number 380,000 into separate word tokens, verification fails by design and the alignment must be reviewed manually.",
        ],
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test() -> int:
    """Regression tests for the safeguards. Requires neither whisperx nor pronouncing."""
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {name}{(' \u2014 ' + detail) if detail else ''}")
        if not condition:
            failures.append(name)

    print("Self-test 1: tokenization of 380,000")
    check("approved tokens('380,000') -> ['380000']", tokens("380,000") == ["380000"])
    check("normalize '380,000' == normalize '380000'", normalize_token("380,000") == normalize_token("380000") == "380000")
    approved = approved_tokens()
    check("approved transcript yields 33 tokens", len(approved) == 33, f"got {len(approved)}")
    counts = [len(tokens(t)) for _, t in APPROVED_TURNS]
    check("turn token counts are [10, 5, 8, 10]", counts == [10, 5, 8, 10], f"got {counts}")

    print("Self-test 2: strict transcript verification")
    def synth(text: str) -> list[dict[str, Any]]:
        return [
            {"word": w, "start": i * 0.2, "end": i * 0.2 + 0.1}
            for i, w in enumerate(text.split())
        ]
    try:
        verify_transcript(synth(EXPECTED_TEXT))
        check("exact approved transcript passes", True)
    except RuntimeError as exc:
        check("exact approved transcript passes", False, str(exc)[:80])
    for name, text in [
        ("leading 'But' rejected", "But " + EXPECTED_TEXT),
        ("truncated fourth line rejected", EXPECTED_TEXT.rsplit("kilometres away from you.", 1)[0]),
        ("wrong number rejected", EXPECTED_TEXT.replace("380,000", "385,000")),
        ("'kilometers' spelling rejected", EXPECTED_TEXT.replace("kilometres", "kilometers")),
    ]:
        try:
            verify_transcript(synth(text))
            check(name, False, "verification unexpectedly passed")
        except RuntimeError:
            check(name, True)

    print("Self-test 3: timeline document validation")
    def doc(events: list[dict[str, Any]]) -> dict[str, Any]:
        return {"events": events}
    valid_fixture = []
    for index, token in enumerate(approved_tokens()):
        valid_fixture.append({
            "speaker": "KEVIN" if index < 10 or 15 <= index < 23 else "KHALED",
            "start": index * 0.1, "end": index * 0.1 + 0.05,
            "phoneme": "T", "viseme": "wide", "source_word": token,
        })
    try:
        validate_timeline_document(doc(valid_fixture), 15.0)
        check("complete valid approved timeline accepted", True)
    except RuntimeError as exc:
        check("complete valid approved timeline accepted", False, str(exc)[:80])
    converted = build_godot_timeline([
        {"speaker": "kevin", "start": 0.0, "end": 0.1, "phoneme": "SIL", "viseme": "rest", "source_word": None},
        {"speaker": "KHALED", "start": 0.2, "end": 0.3, "phoneme": "M", "viseme": "closed", "source_word": "me"},
    ], audio_duration=1.0)
    check("Godot conversion keeps flat event schema and normalizes speakers",
          converted["events"][0]["speaker"] == "KEVIN" and converted["events"][1]["speaker"] == "KHALED")
    check("silence remains rest in Godot vocabulary",
          converted["events"][0]["phoneme"] == "SIL" and converted["events"][0]["viseme"] == "rest")
    for bad_event in [
        {"speaker": "NARRATOR", "start": 0.0, "end": 0.1, "viseme": "open"},
        {"speaker": "KEVIN", "start": 0.0, "end": 0.1, "viseme": "jawdrop"},
        {"speaker": "KEVIN", "start": 0.0, "end": 1.1, "viseme": "open"},
    ]:
        try:
            build_godot_timeline([bad_event], audio_duration=1.0)
            check("unknown or out-of-range Godot values rejected", False)
        except ValueError:
            check("unknown or out-of-range Godot values rejected", True)

    for name, events in [
        ("out-of-order rejected", [dict(valid_fixture[0], start=0.2, end=0.3), dict(valid_fixture[0], start=0.1, end=0.15)]),
        ("bad viseme rejected", [dict(valid_fixture[0], viseme="jawdrop")]),
        ("non-positive duration rejected", [dict(valid_fixture[0], start=0.1, end=0.1)]),
        ("SIL not rest rejected", [dict(valid_fixture[0], phoneme="SIL", viseme="open", source_word=None)]),
        ("event beyond audio duration rejected", [dict(valid_fixture[0], start=15.0, end=15.2)]),
    ]:
        try:
            validate_timeline_document(doc(events), 15.0)
            check(name, False, "validation unexpectedly passed")
        except RuntimeError:
            check(name, True)

    print("Self-test 4: transactional promotion \u2014 success path")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        staged_wav, staged_json = tmp / "out.wav.staged", tmp / "out.json.staged"
        staged_wav.write_bytes(b"NEW-WAV")
        staged_json.write_bytes(b"{}")
        report = promote_outputs(staged_wav, staged_json, out_wav, out_json, tmp / "backup")
        check("both outputs committed", out_wav.read_bytes() == b"NEW-WAV" and out_json.read_bytes() == b"{}")
        check("report lists both as created", sorted(report["created"]) == sorted([str(out_wav), str(out_json)]))
        check("commit journal removed after success", not journal_path_for(out_wav).exists())
        check("staged files removed after success", not staged_wav.exists() and not staged_json.exists())

    print("Self-test 5: failure AFTER the first output replacement")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        staged_wav, staged_json = tmp / "out.wav.staged", tmp / "out.json.staged"
        staged_wav.write_bytes(b"NEW-WAV")
        staged_json.write_bytes(b"{}")
        out_wav.write_bytes(b"OLD-WAV")
        out_json.write_bytes(b"OLD-JSON")
        def fail_second_commit(checkpoint: str) -> None:
            if checkpoint == "after_commit:0":
                raise OSError("injected second-commit failure")
        try:
            promote_outputs(staged_wav, staged_json, out_wav, out_json, tmp / "backup", fault_hook=fail_second_commit)
            check("promotion failure detected", False, "promotion unexpectedly succeeded")
        except RuntimeError as exc:
            check("promotion failure detected", True)
            check("first-committed WAV rolled back to previous content", out_wav.read_bytes() == b"OLD-WAV")
            check("no partial new WAV left staged", not staged_wav.exists())
            check("timeline restored to previous content", out_json.read_bytes() == b"OLD-JSON")
            check("commit journal removed after successful rollback", not journal_path_for(out_wav).exists())
            check("failure message reports rollback", "rollback completed" in str(exc))

    print("Self-test 6: failure DURING rollback")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        staged_wav, staged_json = tmp / "out.wav.staged", tmp / "out.json.staged"
        staged_wav.write_bytes(b"NEW-WAV")
        staged_json.write_bytes(b"{}")
        out_wav.write_bytes(b"OLD-WAV")
        out_json.write_bytes(b"OLD-JSON")

        def hook(checkpoint: str) -> None:
            if checkpoint == "after_commit:0":
                raise OSError("injected second-commit failure")
            if checkpoint == "rollback:start":
                raise ValueError("injected rollback fault (test)")

        try:
            promote_outputs(staged_wav, staged_json, out_wav, out_json, tmp / "backup", fault_hook=hook)
            check("rollback failure detected", False, "promotion unexpectedly succeeded")
        except RuntimeError as exc:
            check("rollback failure detected", True)
            check(
                "message reports incomplete rollback and kept journal",
                ("rollback was incomplete" in str(exc)) and (journal_path_for(out_wav).name in str(exc)),
            )
            check("commit journal KEPT for recovery", journal_path_for(out_wav).exists())

        # Recovery must now undo the interrupted promotion.
        summary = recover_interrupted_promotion(out_wav, out_json)
        check("recovery ran after failed rollback", summary is not None)
        if summary:
            check("WAV restored to previous content by recovery", out_wav.read_bytes() == b"OLD-WAV")
            check("journal deleted after recovery", not journal_path_for(out_wav).exists())

    print("Self-test 7: recovery after an INTERRUPTED commit (simulated crash)")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        staged_wav, staged_json = tmp / "out.wav.staged", tmp / "out.json.staged"
        backup_dir = tmp / "backup"
        backup_dir.mkdir()
        # Crash state: WAV was committed (NEW), timeline commit never happened,
        # backups exist for both, staged timeline still present, journal present.
        out_wav.write_bytes(b"NEW-WAV")
        out_json.write_bytes(b"OLD-JSON")
        (backup_dir / "out.wav.bak").write_bytes(b"OLD-WAV")
        (backup_dir / "out.json.bak").write_bytes(b"OLD-JSON")
        staged_json.write_bytes(b"{}")
        write_journal(journal_path_for(out_wav), {
            "version": JOURNAL_VERSION,
            "destinations": [
                {"path": str(out_wav), "existed": True, "backup": str(backup_dir / "out.wav.bak")},
                {"path": str(out_json), "existed": True, "backup": str(backup_dir / "out.json.bak")},
            ],
            "staged": [str(staged_wav), str(staged_json)],
        })
        summary = recover_interrupted_promotion(out_wav, out_json)
        check("interrupted promotion detected", summary is not None)
        if summary:
            check("WAV restored to pre-run content", out_wav.read_bytes() == b"OLD-WAV")
            check("timeline untouched at pre-run content", out_json.read_bytes() == b"OLD-JSON")
            check("staged files cleaned up", not staged_wav.exists() and not staged_json.exists())
            check("journal deleted after recovery", not journal_path_for(out_wav).exists())
            check("both destinations reported restored", sorted(summary["restored"]) == sorted([str(out_wav), str(out_json)]))

    print("Self-test 8: recovery removes newly created outputs (no pre-existing files)")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        staged_wav, staged_json = tmp / "out.wav.staged", tmp / "out.json.staged"
        backup_dir = tmp / "backup"
        backup_dir.mkdir()
        # Crash state: neither output existed before; the WAV was committed.
        out_wav.write_bytes(b"NEW-WAV")
        staged_json.write_bytes(b"{}")
        write_journal(journal_path_for(out_wav), {
            "version": JOURNAL_VERSION,
            "destinations": [
                {"path": str(out_wav), "existed": False, "backup": str(backup_dir / "out.wav.bak")},
                {"path": str(out_json), "existed": False, "backup": str(backup_dir / "out.json.bak")},
            ],
            "staged": [str(staged_wav), str(staged_json)],
        })
        summary = recover_interrupted_promotion(out_wav, out_json)
        check("interrupted promotion detected (created case)", summary is not None)
        if summary:
            check("newly committed WAV removed by recovery", not out_wav.exists())
            check("timeline not created", not out_json.exists())
            check("journal deleted after recovery", not journal_path_for(out_wav).exists())

    print("Self-test 9: invalid recovery journals fail closed")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        out_wav.write_bytes(b"KEEP-WAV")
        out_json.write_bytes(b"KEEP-JSON")
        journal = journal_path_for(out_wav)
        journal.write_text("{not-json", encoding="utf-8")
        try:
            recover_interrupted_promotion(out_wav, out_json)
            check("malformed journal rejected", False)
        except RuntimeError:
            check("malformed journal rejected", True)
        check("malformed journal preserved", journal.exists())
        check("destinations untouched on invalid journal",
              out_wav.read_bytes() == b"KEEP-WAV" and out_json.read_bytes() == b"KEEP-JSON")

    print("Self-test 10: incomplete backup temp cannot replace original")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        out_wav, out_json = tmp / "out.wav", tmp / "out.json"
        backup_dir = tmp / "backup"
        backup_dir.mkdir()
        out_wav.write_bytes(b"KEEP-WAV")
        out_json.write_bytes(b"KEEP-JSON")
        (backup_dir / "out.wav.bak.tmp").write_bytes(b"PARTIAL")
        write_journal(journal_path_for(out_wav), {
            "version": JOURNAL_VERSION,
            "destinations": [
                {"path": str(out_wav), "existed": True, "backup": str(backup_dir / "out.wav.bak")},
                {"path": str(out_json), "existed": True, "backup": str(backup_dir / "out.json.bak")},
            ],
            "staged": [str(out_wav.with_name("out.wav.staged")), str(out_json.with_name("out.json.staged"))],
        })
        summary = recover_interrupted_promotion(out_wav, out_json)
        check("partial temporary backup ignored", summary is not None and not summary["restored"])
        check("original files remain intact",
              out_wav.read_bytes() == b"KEEP-WAV" and out_json.read_bytes() == b"KEEP-JSON")

    print()
    if failures:
        print(f"SELF-TEST FAIL: {len(failures)} check(s) failed: {failures}")
        return 1
    print("SELF-TEST PASS: all safeguard checks passed")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-wav",
        type=Path,
        default=Path("/home/ubuntu/output/holos_animation_test_audio_15s.wav"),
    )
    parser.add_argument(
        "--output-wav",
        type=Path,
        default=Path("/home/ubuntu/output/holos_animation_test_audio_15s_aligned.wav"),
    )
    parser.add_argument(
        "--output-timeline",
        type=Path,
        default=Path("/home/ubuntu/output/HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json"),
    )
    parser.add_argument("--asr-model", default="tiny.en")
    parser.add_argument("--align-model", default="wav2vec2")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run safeguard regression tests (no whisperx/pronouncing required) and exit.",
    )
    parser.add_argument(
        "--recover",
        action="store_true",
        help="Recover an interrupted output promotion (commit journal) and exit.",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    output_wav = args.output_wav.resolve()
    output_timeline = args.output_timeline.resolve()

    recovery = recover_interrupted_promotion(output_wav, output_timeline)
    if args.recover:
        if recovery is None:
            print("PASS: no interrupted promotion found; nothing to recover")
            return 0
        print("PASS: interrupted promotion recovered")
        print(f"      Restored: {recovery['restored'] or 'none'}")
        print(f"      Removed: {recovery['removed'] or 'none'}")
        print(f"      Left unchanged: {recovery['left'] or 'none'}")
        return 0
    if recovery is not None:
        print("RECOVERY: an interrupted promotion was found and rolled back before processing")
        print(f"          Restored: {recovery['restored'] or 'none'}")
        print(f"          Removed: {recovery['removed'] or 'none'}")

    if whisperx is None:
        print("FAIL: Missing dependency: whisperx. Run this script in the alignment venv.", file=sys.stderr)
        return 1
    if pronouncing is None:
        print("FAIL: Missing dependency: pronouncing. Install it in the alignment venv.", file=sys.stderr)
        return 1

    # Stage next to the destinations: os.replace() is atomic only within one
    # filesystem, so staging inside /tmp would risk cross-device rename errors.
    staged_wav = output_wav.with_name(output_wav.name + ".staged")
    staged_timeline = output_timeline.with_name(output_timeline.name + ".staged")
    backup_dir = output_wav.parent / f"holos_pre_promote_backup_{time.strftime('%Y%m%d_%H%M%S')}"

    for staged in (staged_wav, staged_timeline):
        try:
            staged.unlink()
        except FileNotFoundError:
            pass

    try:
        print("HOLOS Milestone 5.1 strict processor (v2.1)")
        print(f"Input: {args.input_wav}")
        print(f"Output WAV: {output_wav}")
        print(f"Output timeline: {output_timeline}")
        wav_info = inspect_wav(args.input_wav)
        print(f"[0/6] PASS: input WAV format verified: {wav_info}")

        asr = run_asr(args.input_wav, args.asr_model, args.device, args.compute_type)
        aligned = run_alignment(asr["result"], args.align_model, args.device, asr["audio"])
        words = flatten_words(aligned)
        if not words:
            raise RuntimeError("No aligned word timestamps were produced")
        verify_transcript(words)
        events = build_events(words)

        print("[6/6] Staging normalized WAV and timeline for validation")
        normalize_audio(args.input_wav.resolve(), staged_wav)
        staged_info = inspect_wav(staged_wav, allowed_widths=(3,))
        print(f"      Staged WAV verified: {staged_info}")

        document = build_output_document(events, args.input_wav, output_wav)
        staged_timeline.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
        counts = validate_timeline_document(document, staged_info["duration_seconds"])
        document["phoneme_count"] = counts["phoneme_count"]
        document["silence_event_count"] = counts["silence_event_count"]
        staged_timeline.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
        print(
            f"      Staged timeline verified: {counts['event_count']} events "
            f"({counts['phoneme_count']} phonemes, {counts['silence_event_count']} silence)"
        )

        print("      Committing outputs transactionally")
        report = promote_outputs(staged_wav, staged_timeline, output_wav, output_timeline, backup_dir)
        print("PASS: aligned WAV and phoneme timeline committed")
        print(f"      Created: {report['created'] or 'none'}")
        print(f"      Replaced: {report['replaced'] or 'none'}")
        print(f"      Output WAV SHA-256: {sha256(output_wav)}")
        print(f"      Output timeline SHA-256: {sha256(output_timeline)}")
        print(f"      Measured dialogue duration: {staged_info['duration_seconds']:.6f} s")
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        print(
            "No new aligned WAV or timeline was committed. If a promotion or rollback failure "
            "occurred, see the message above; a kept commit journal is recovered automatically "
            "on the next run, or explicitly with --recover.",
            file=sys.stderr,
        )
        return 1
    finally:
        for staged in (staged_wav, staged_timeline):
            try:
                staged.unlink()
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
