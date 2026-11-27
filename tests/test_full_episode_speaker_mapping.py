from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))
import build_holos_full_episode_timeline as builder  # noqa: E402
import process_holos_aligned_audio_v2 as strict  # noqa: E402


class FullEpisodeSpeakerMappingTests(unittest.TestCase):
    def test_working_cast_ids_normalize_to_stable_timeline_ids(self) -> None:
        self.assertEqual(strict.normalize_speaker("THE MOON"), "THE_MOON")
        self.assertEqual(strict.normalize_speaker("the_moon"), "THE_MOON")
        self.assertEqual(strict.normalize_speaker("ORBIT"), "ORBIT")
        self.assertIsNone(strict.normalize_speaker("UNCONFIRMED VOICE"))

    def test_generic_turn_mapper_checks_text_before_assigning_speakers(self) -> None:
        turns = [
            ("THE MOON", "But the whole changed."),
            ("ORBIT", "Acknowledged."),
        ]
        words = [
            {"word": word, "start": i * 0.2, "end": i * 0.2 + 0.1}
            for i, word in enumerate("But the whole changed. Acknowledged.".split())
        ]
        mapped = strict.map_words_to_speakers_for_turns(words, turns)
        self.assertEqual([speaker for speaker, _ in mapped], ["THE_MOON"] * 4 + ["ORBIT"])
        wrong = [dict(word) for word in words]
        wrong[2]["word"] = "parts"
        with self.assertRaisesRegex(RuntimeError, "Ambiguous speaker mapping"):
            strict.map_words_to_speakers_for_turns(wrong, turns)

    def test_full_episode_alignment_preparation_accepts_canonical_but(self) -> None:
        turns = [("THE MOON", "But the whole changed."), ("ORBIT", "Acknowledged.")]
        aligned = {
            "word_segments": [
                {"word": word, "start": i * 0.2, "end": i * 0.2 + 0.1}
                for i, word in enumerate("But the whole changed. Acknowledged.".split())
            ]
        }
        words, normalizations = builder.prepare_full_episode_words(aligned, turns)
        self.assertEqual(len(words), 5)
        self.assertEqual(normalizations, [])

    def test_full_episode_alignment_preparation_fails_on_unreviewed_difference(self) -> None:
        turns = [("THE MOON", "But the whole changed.")]
        aligned = {"word_segments": [
            {"word": word, "start": i * 0.2, "end": i * 0.2 + 0.1}
            for i, word in enumerate("But the boat changed.".split())
        ]}
        with self.assertRaisesRegex(RuntimeError, "FULL-EPISODE TRANSCRIPT FAILURE"):
            builder.prepare_full_episode_words(aligned, turns)

    def test_builder_emits_versioned_full_cast_event_document(self) -> None:
        turns = [("THE MOON", "But the whole changed."), ("ORBIT", "Acknowledged.")]
        words = "But the whole changed. Acknowledged.".split()
        aligned = {"word_segments": [
            {"word": word, "start": i * 0.25, "end": i * 0.25 + 0.18, "score": 0.9}
            for i, word in enumerate(words)
        ]}
        def fake_expand(word: dict, speaker: str) -> list[dict]:
            raw = str(word["word"])
            start, end = float(word["start"]), float(word["end"])
            return [{
                "speaker": speaker,
                "start": start,
                "end": end,
                "phoneme": "AH",
                "viseme": "open",
                "category": "test fixture",
                "source_word": raw,
                "acoustic_word": raw,
                "acoustic_word_start": start,
                "acoustic_word_end": end,
                "acoustic_word_score": float(word.get("score", 0.5)),
                "confidence": float(word.get("score", 0.5)),
                "verification_status": "test fixture",
                "notes": "phoneme subdivision stubbed in unit test",
            }]

        with patch.object(strict, "expand_internal_events", side_effect=fake_expand):
            document = builder.build_absolute_document(
                aligned, "episode.wav", "a" * 64, "alignment.json", "b" * 64, 3.0,
                approved_turns=turns,
            )
        self.assertEqual(document["schema_version"], 1)
        self.assertEqual(document["approved_transcript"][0]["speaker"], "THE_MOON")
        self.assertIn("But", [event["source_word"] for event in document["events"] if event["source_word"]])
        self.assertEqual(document["event_count"], len(document["events"]))

    def test_full_episode_validation_matches_canonical_tokens_and_speakers(self) -> None:
        transcript = [
            {"speaker": "THE MOON", "text": "But the whole changed."},
            {"speaker": "ORBIT", "text": "Acknowledged."},
        ]
        events = []
        for i, (speaker, word) in enumerate([
            ("THE_MOON", "But"), ("THE_MOON", "the"),
            ("THE_MOON", "whole"), ("THE_MOON", "changed."),
            ("ORBIT", "Acknowledged."),
        ]):
            events.append({
                "speaker": speaker,
                "start": i * 0.2,
                "end": i * 0.2 + 0.1,
                "phoneme": "B",
                "viseme": "closed",
                "source_word": word,
            })
        counts = strict.validate_timeline_document({
            "schema_version": 1,
            "approved_transcript": transcript,
            "events": events,
        }, 2.0)
        self.assertEqual(counts["event_count"], 5)

    def test_full_episode_validation_rejects_wrong_speaker_assignment(self) -> None:
        document = {
            "schema_version": 1,
            "approved_transcript": [{"speaker": "THE_MOON", "text": "The whole changed."}],
            "events": [
                {"speaker": "ORBIT", "start": 0.0, "end": 0.1, "phoneme": "DH", "viseme": "open", "source_word": "The"},
                {"speaker": "THE_MOON", "start": 0.1, "end": 0.2, "phoneme": "W", "viseme": "open", "source_word": "whole"},
                {"speaker": "THE_MOON", "start": 0.2, "end": 0.3, "phoneme": "CH", "viseme": "wide", "source_word": "changed."},
            ],
        }
        with self.assertRaisesRegex(RuntimeError, "do not match approved_transcript"):
            strict.validate_timeline_document(document, 1.0)

    def test_full_episode_validation_rejects_word_change_inside_acoustic_interval(self) -> None:
        document = {
            "schema_version": 1,
            "approved_transcript": [{"speaker": "THE_MOON", "text": "Moon."}],
            "events": [
                {"speaker": "THE_MOON", "start": 0.0, "end": 0.1, "phoneme": "M", "viseme": "closed", "source_word": "Moon", "acoustic_word_start": 0.0, "acoustic_word_end": 0.2},
                {"speaker": "THE_MOON", "start": 0.1, "end": 0.2, "phoneme": "UW", "viseme": "round", "source_word": "Moonbeam", "acoustic_word_start": 0.0, "acoustic_word_end": 0.2},
            ],
        }
        with self.assertRaisesRegex(RuntimeError, "source_word changes inside one acoustic word"):
            strict.validate_timeline_document(document, 1.0)

    def test_godot_event_conversion_normalizes_full_cast_alias(self) -> None:
        result = strict.build_godot_timeline([
            {"speaker": "THE MOON", "start": 0.0, "end": 0.1, "phoneme": "M", "viseme": "closed"},
            {"speaker": "ORBIT", "start": 0.2, "end": 0.3, "phoneme": "AO", "viseme": "round"},
        ], audio_duration=1.0)
        self.assertEqual([event["speaker"] for event in result["events"]], ["THE_MOON", "ORBIT"])


if __name__ == "__main__":
    unittest.main()
