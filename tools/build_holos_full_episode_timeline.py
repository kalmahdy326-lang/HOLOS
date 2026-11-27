#!/usr/bin/env python3
"""Build versioned HOLOS event timelines from a verified full-episode alignment.

This script consumes an existing WhisperX alignment; it does not run ASR or
modify audio. All relative file arguments resolve from the repository root.
The source audio hash is required so generated timelines cannot silently be
associated with a different recording.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
import process_holos_aligned_audio_v2 as strict  # noqa: E402

NORMALIZATION = "accepted_user_approved_asr_spelling_normalization"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (REPO_ROOT / path).resolve()


def prepare_exchange_words(aligned: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Select and strictly verify the opening approved exchange.

    Only the explicitly approved ASR spelling kilometers -> kilometres is
    normalized. Every word and its timestamps are otherwise retained.
    """
    expected = strict.approved_tokens()
    all_words = strict.flatten_words(aligned)
    if len(all_words) < len(expected):
        raise RuntimeError(f"Alignment has {len(all_words)} words; need at least {len(expected)}.")
    exchange = [dict(word) for word in all_words[:len(expected)]]
    observed = [strict.normalize_token(str(word["word"])) for word in exchange]
    normalizations: list[dict[str, Any]] = []
    for index, (asr_word, approved_word) in enumerate(zip(observed, expected)):
        if asr_word == approved_word:
            continue
        if asr_word == "kilometers" and approved_word == "kilometres":
            original = str(exchange[index]["word"])
            normalizations.append({
                "index": index,
                "asr": asr_word,
                "approved": approved_word,
                "start": float(exchange[index]["start"]),
                "end": float(exchange[index]["end"]),
            })
            exchange[index]["asr_word"] = original
            exchange[index]["word"] = "kilometres"
            continue
        context_start = max(0, index - 3)
        raise RuntimeError(
            "STRICT TRANSCRIPT FAILURE: first mismatch at token "
            f"{index}; observed={observed[context_start:index + 4]!r}; "
            f"expected={expected[context_start:index + 4]!r}"
        )
    strict.verify_transcript(exchange)
    return exchange, normalizations


def prepare_full_episode_words(
    aligned: dict[str, Any], approved_turns: list[tuple[str, str]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Verify the entire aligned word sequence against user-approved turns.

    Unlike the opening-exchange compatibility path, this function performs no
    implicit spelling normalization. Any discrepancy must be resolved in the
    canonical transcript or recorded through an explicit review decision.
    """
    if not approved_turns:
        raise ValueError("Full-episode transcript contains no spoken turns")
    for speaker, text in approved_turns:
        if strict.normalize_speaker(speaker) not in strict.VALID_SPEAKERS:
            raise RuntimeError(f"Unsupported transcript speaker ID: {speaker!r}")
        if not text.strip():
            raise RuntimeError(f"Empty transcript text for speaker {speaker!r}")
    words = strict.flatten_words(aligned)
    expected_by_turn = [strict.tokens(text) for _, text in approved_turns]
    expected = [token for turn in expected_by_turn for token in turn]
    observed = [strict.normalize_token(str(word["word"])) for word in words]
    if observed != expected:
        first_diff = next(
            (i for i, (a, b) in enumerate(zip(observed, expected)) if a != b),
            min(len(observed), len(expected)),
        )
        raise RuntimeError(
            "FULL-EPISODE TRANSCRIPT FAILURE: aligned words do not exactly match the approved transcript; "
            f"first difference {first_diff}, observed={observed[first_diff:first_diff + 5]!r}, "
            f"expected={expected[first_diff:first_diff + 5]!r}, "
            f"word counts {len(observed)} vs {len(expected)}"
        )
    return words, []


def validate_event_contract(document: dict[str, Any], audio_duration: float) -> dict[str, int]:
    """Apply the existing Python event validator and require schema version 1."""
    if document.get("schema_version") != 1:
        raise RuntimeError("Timeline validation failed: schema_version must be 1")
    return strict.validate_timeline_document(document, audio_duration)


def _annotate_normalizations(
    events: list[dict[str, Any]], normalizations: list[dict[str, Any]]
) -> None:
    for item in normalizations:
        for event in events:
            if (
                abs(float(event.get("acoustic_word_start", -10.0)) - item["start"]) <= 1e-6
                and abs(float(event.get("acoustic_word_end", -10.0)) - item["end"]) <= 1e-6
            ):
                event["asr_word"] = item["asr"]
                event["normalization"] = NORMALIZATION


def build_absolute_document(
    aligned: dict[str, Any],
    source_name: str,
    source_hash: str,
    alignment_name: str,
    alignment_hash: str,
    audio_duration: float,
    approved_turns: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    if not math.isfinite(audio_duration) or audio_duration <= 0:
        raise ValueError("Audio duration must be finite and greater than zero.")
    turns = strict.APPROVED_TURNS if approved_turns is None else approved_turns
    if turns == strict.APPROVED_TURNS:
        words, normalizations = prepare_exchange_words(aligned)
    else:
        words, normalizations = prepare_full_episode_words(aligned, turns)
    events = strict.build_events(words, turns)
    _annotate_normalizations(events, normalizations)
    converted = strict.build_godot_timeline(events, audio_duration=audio_duration, version=1)
    document: dict[str, Any] = {
        **converted,
        "status": "approved transcript matched; acoustic word boundaries aligned; internal phoneme boundaries estimated",
        "timebase": "absolute_source_audio_seconds",
        "source_audio_name": source_name,
        "source_audio_sha256": source_hash,
        "alignment_name": alignment_name,
        "alignment_sha256": alignment_hash,
        "approved_transcript": [
            {"speaker": strict.normalize_speaker(speaker), "text": text} for speaker, text in turns
        ],
        "speech_word_envelope_seconds": {
            "start": float(words[0]["start"]),
            "end": float(words[-1]["end"]),
        },
        "asr_normalizations": normalizations,
        "alignment_method": (
            "WhisperX acoustic word/character alignment; pronunciation-dictionary "
            "subdivision for internal phoneme estimates"
        ),
        "limitations": [
            "Word boundaries are supplied by the acoustic alignment.",
            "Internal phoneme boundaries are dictionary-based subdivisions, not dedicated phoneme-aligner output.",
            "The user-approved transcript retains kilometres; ASR kilometers is preserved in normalization metadata.",
        ],
    }
    document.update(validate_event_contract(document, audio_duration))
    return document


def inspect_review_wav(path: Path, expected_hash: str) -> dict[str, Any]:
    if sha256_file(path).lower() != expected_hash.lower():
        raise RuntimeError(
            f"Review WAV SHA-256 mismatch for {path.name}; refusing to associate the timeline with this WAV."
        )
    return strict.inspect_wav(path, allowed_widths=(3,))


def build_review_relative_document(
    absolute: dict[str, Any],
    offset_seconds: float,
    review_duration: float,
    review_wav_name: str,
    review_wav_hash: str,
    absolute_timeline_hash: str,
) -> dict[str, Any]:
    if not math.isfinite(offset_seconds) or offset_seconds < 0:
        raise ValueError("Review offset must be finite and non-negative.")
    if not math.isfinite(review_duration) or review_duration <= 0:
        raise ValueError("Review WAV duration must be finite and greater than zero.")
    relative = copy.deepcopy(absolute)
    relative["timebase"] = "review_wav_relative_seconds"
    relative["review_wav_name"] = review_wav_name
    relative["review_wav_sha256"] = review_wav_hash
    relative["review_offset_seconds"] = offset_seconds
    relative["absolute_source_timeline_sha256"] = absolute_timeline_hash
    relative["speech_word_envelope_seconds"] = {
        key: value - offset_seconds
        for key, value in absolute["speech_word_envelope_seconds"].items()
    }
    for event in relative["events"]:
        for key in ("start", "end", "acoustic_word_start", "acoustic_word_end"):
            if key in event and event[key] is not None:
                event[key] = round(float(event[key]) - offset_seconds, 6)
    relative.update(validate_event_contract(relative, review_duration))
    return relative


def json_text(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def publish_new_files(files: dict[Path, str]) -> None:
    """Publish a set of new outputs atomically per file and clean partial writes."""
    paths = list(files)
    if len(set(paths)) != len(paths):
        raise ValueError("Output paths must be distinct.")
    existing = [str(path) for path in paths if path.exists()]
    if existing:
        raise FileExistsError(
            "Refusing to replace existing outputs: " + ", ".join(existing)
        )
    staged: dict[Path, Path] = {}
    committed: list[Path] = []
    try:
        for target, content in files.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary_name = tempfile.mkstemp(
                prefix=target.name + ".", suffix=".tmp", dir=target.parent
            )
            temporary = Path(temporary_name)
            staged[target] = temporary
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        for target, temporary in staged.items():
            os.replace(temporary, target)
            committed.append(target)
    except Exception:
        for target in committed:
            target.unlink(missing_ok=True)
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alignment", required=True, help="WhisperX alignment JSON; relative paths use repository root.")
    parser.add_argument("--transcript", help="Optional canonical transcript JSON with transcript_version and ordered utterances[].")
    parser.add_argument("--source-mp3", required=True, help="Verified source MP3 path.")
    parser.add_argument("--expected-source-sha256", required=True, help="Expected source MP3 SHA-256.")
    parser.add_argument("--expected-alignment-sha256", help="Optional expected alignment-file SHA-256.")
    parser.add_argument("--audio-duration-seconds", type=float, required=True, help="Measured full source audio duration.")
    parser.add_argument("--absolute-output", required=True, help="Absolute-time JSON output path.")
    parser.add_argument("--review-wav", help="Optional 48 kHz stereo 24-bit PCM review WAV.")
    parser.add_argument("--expected-review-wav-sha256", help="Required when --review-wav is supplied.")
    parser.add_argument("--review-offset-seconds", type=float, default=0.091)
    parser.add_argument("--relative-output", help="Review-WAV-relative JSON output; requires --review-wav.")
    parser.add_argument("--manifest-output", help="Manifest output; defaults beside the absolute timeline.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", args.expected_source_sha256):
            raise ValueError("--expected-source-sha256 must be 64 hexadecimal characters.")
        source = resolve_repo_path(args.source_mp3)
        alignment_path = resolve_repo_path(args.alignment)
        absolute_path = resolve_repo_path(args.absolute_output)
        transcript_path = resolve_repo_path(args.transcript) if args.transcript else None
        if not source.is_file():
            raise FileNotFoundError(f"Source MP3 not found: {source}")
        if not alignment_path.is_file():
            raise FileNotFoundError(f"Alignment JSON not found: {alignment_path}")
        source_hash = sha256_file(source)
        if source_hash.lower() != args.expected_source_sha256.lower():
            raise RuntimeError(
                f"Source MP3 SHA-256 mismatch: expected {args.expected_source_sha256}, got {source_hash}"
            )
        alignment_hash = sha256_file(alignment_path)
        if args.expected_alignment_sha256 and alignment_hash.lower() != args.expected_alignment_sha256.lower():
            raise RuntimeError("Alignment JSON SHA-256 mismatch.")
        transcript_version = "opening-four-turn-approved"
        if transcript_path is None:
            approved_turns = strict.APPROVED_TURNS
            transcript_name = "embedded-four-turn-approval"
            canonical_payload = json.dumps(
                [{"speaker": s, "text": t} for s, t in approved_turns],
                ensure_ascii=False, separators=(",", ":"),
            ).encode("utf-8")
            transcript_hash = hashlib.sha256(canonical_payload).hexdigest()
        else:
            if not transcript_path.is_file():
                raise FileNotFoundError(f"Canonical transcript not found: {transcript_path}")
            transcript_data = json.loads(transcript_path.read_text(encoding="utf-8"))
            if not isinstance(transcript_data, dict) or not isinstance(transcript_data.get("utterances"), list):
                raise RuntimeError("Canonical transcript JSON must be an object with an utterances array.")
            if transcript_data.get("approval_status") != "approved":
                raise RuntimeError("Canonical transcript must carry approval_status='approved' before production alignment.")
            if not isinstance(transcript_data.get("transcript_version"), str) or not transcript_data["transcript_version"].strip():
                raise RuntimeError("Canonical transcript must carry a non-empty transcript_version.")
            approved_turns = []
            for index, utterance in enumerate(transcript_data["utterances"]):
                if not isinstance(utterance, dict) or not isinstance(utterance.get("speaker"), str) or not isinstance(utterance.get("text"), str):
                    raise RuntimeError(f"Malformed canonical transcript utterance at index {index}.")
                approved_turns.append((utterance["speaker"], utterance["text"]))
            transcript_version = str(transcript_data.get("transcript_version", "unversioned"))
            transcript_name = transcript_path.name
            transcript_hash = sha256_file(transcript_path)
        aligned = json.loads(alignment_path.read_text(encoding="utf-8"))
        if not isinstance(aligned, dict):
            raise RuntimeError("Alignment JSON root must be an object.")
        absolute = build_absolute_document(
            aligned, source.name, source_hash, alignment_path.name, alignment_hash,
            args.audio_duration_seconds, approved_turns,
        )
        absolute_text = json_text(absolute)
        absolute_hash = hashlib.sha256(absolute_text.encode("utf-8")).hexdigest()
        outputs: dict[Path, str] = {absolute_path: absolute_text}
        review_info = None
        relative_path = None
        if args.review_wav:
            if not args.expected_review_wav_sha256:
                raise ValueError("--expected-review-wav-sha256 is required with --review-wav.")
            if not re.fullmatch(r"[0-9a-fA-F]{64}", args.expected_review_wav_sha256):
                raise ValueError("--expected-review-wav-sha256 must be 64 hexadecimal characters.")
            if not args.relative_output:
                raise ValueError("--relative-output is required with --review-wav.")
            review_path = resolve_repo_path(args.review_wav)
            relative_path = resolve_repo_path(args.relative_output)
            review_info = inspect_review_wav(review_path, args.expected_review_wav_sha256)
            if args.review_offset_seconds + review_info["duration_seconds"] > args.audio_duration_seconds + strict.DURATION_EPSILON_SECONDS:
                raise RuntimeError("Review WAV window extends beyond the measured source duration.")
            relative = build_review_relative_document(
                absolute, args.review_offset_seconds, review_info["duration_seconds"],
                review_path.name, args.expected_review_wav_sha256.lower(), absolute_hash,
            )
            outputs[relative_path] = json_text(relative)
        elif args.relative_output:
            raise ValueError("--relative-output requires --review-wav.")
        manifest_path = resolve_repo_path(args.manifest_output) if args.manifest_output else absolute_path.with_suffix(".manifest.json")
        if manifest_path in outputs:
            raise ValueError("Manifest output path must be distinct from timeline outputs.")
        manifest = {
            "source_audio_name": source.name,
            "source_audio_sha256": source_hash,
            "alignment_name": alignment_path.name,
            "alignment_sha256": alignment_hash,
            "canonical_transcript_name": transcript_name,
            "canonical_transcript_sha256": transcript_hash,
            "transcript_version": transcript_version,
            "audio_duration_seconds": args.audio_duration_seconds,
            "absolute_timeline_name": absolute_path.name,
            "absolute_timeline_sha256": absolute_hash,
            "review_wav": None if review_info is None else {
                "name": Path(args.review_wav).name,
                "sha256": args.expected_review_wav_sha256.lower(),
                "format": review_info,
                "offset_seconds": args.review_offset_seconds,
                "relative_timeline_name": relative_path.name if relative_path else None,
                "relative_timeline_sha256": hashlib.sha256(
                    outputs[relative_path].encode("utf-8")
                ).hexdigest() if relative_path else None,
            },
            "transcript_status": (
                "approved after pronunciation review" if transcript_path is None
                else "approved canonical transcript; aligned tokens matched exactly"
            ),
            "godot_integration": "not performed",
        }
        outputs[manifest_path] = json_text(manifest)
        publish_new_files(outputs)
        print(json.dumps(manifest, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
