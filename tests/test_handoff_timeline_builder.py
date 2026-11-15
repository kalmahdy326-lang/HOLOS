from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))
import build_holos_full_episode_timeline as builder
import process_holos_aligned_audio_v2 as strict


HANDOFF = REPO_ROOT / "handoffs" / "milestone-5-1-2026-11-15"
ALIGNMENT_PATH = HANDOFF / "HOLOS_FullEpisode_WhisperX_Aligned.json"
ABSOLUTE_PATH = HANDOFF / "HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json"
RELATIVE_PATH = HANDOFF / "HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json"


class HandoffTimelineBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.alignment = json.loads(ALIGNMENT_PATH.read_text(encoding="utf-8"))
        cls.absolute = json.loads(ABSOLUTE_PATH.read_text(encoding="utf-8"))
        cls.relative = json.loads(RELATIVE_PATH.read_text(encoding="utf-8"))
        cls.manifest = json.loads(
            (HANDOFF / "HOLOS_Episode1_four_turn_review_manifest.json").read_text(encoding="utf-8")
        )

    def test_opening_exchange_matches_approved_transcript_with_two_normalizations(self) -> None:
        words, normalizations = builder.prepare_exchange_words(self.alignment)
        self.assertEqual([strict.normalize_token(w["word"]) for w in words], strict.approved_tokens())
        self.assertEqual(len(words), 33)
        self.assertEqual([item["asr"] for item in normalizations], ["kilometers", "kilometers"])
        self.assertEqual([item["approved"] for item in normalizations], ["kilometres", "kilometres"])

    def test_unapproved_leading_but_fails(self) -> None:
        aligned = {"word_segments": copy.deepcopy(self.alignment["word_segments"])}
        aligned["word_segments"][0]["word"] = "But"
        with self.assertRaisesRegex(RuntimeError, "STRICT TRANSCRIPT FAILURE"):
            builder.prepare_exchange_words(aligned)

    def test_wrong_number_fails(self) -> None:
        aligned = {"word_segments": copy.deepcopy(self.alignment["word_segments"])}
        number = next(w for w in aligned["word_segments"] if w["word"] == "380,000")
        number["word"] = "385,000"
        with self.assertRaisesRegex(RuntimeError, "STRICT TRANSCRIPT FAILURE"):
            builder.prepare_exchange_words(aligned)

    def test_handoff_timelines_validate_against_processor_contract(self) -> None:
        absolute = copy.deepcopy(self.absolute)
        relative = copy.deepcopy(self.relative)
        absolute["schema_version"] = 1
        relative["schema_version"] = 1
        absolute_counts = builder.validate_event_contract(absolute, 914.880)
        relative_counts = builder.validate_event_contract(relative, 16.825)
        self.assertEqual(absolute_counts["event_count"], 189)
        self.assertEqual(relative_counts["event_count"], 189)
        self.assertEqual(len(absolute["asr_normalizations"]), 2)

    def test_review_timeline_is_offset_from_absolute_timeline(self) -> None:
        self.assertEqual(len(self.absolute["events"]), len(self.relative["events"]))
        for absolute, relative in zip(self.absolute["events"], self.relative["events"]):
            self.assertAlmostEqual(absolute["start"] - 0.091, relative["start"], places=6)
            self.assertAlmostEqual(absolute["end"] - 0.091, relative["end"], places=6)
            self.assertEqual(absolute["phoneme"], relative["phoneme"])
            self.assertEqual(absolute["speaker"], relative["speaker"])

    def test_review_manifest_records_distinct_wav_variant(self) -> None:
        self.assertEqual(self.manifest["review_wav_format"]["sample_rate_hz"], 48000)
        self.assertEqual(self.manifest["review_wav_format"]["channels"], 2)
        self.assertEqual(self.manifest["review_wav_format"]["sample_width_bytes"], 3)
        self.assertNotEqual(
            self.manifest["review_wav_sha256"],
            "e9d8a3a88f310b1558a884fcec87f8cf16741019ddbcede2a2db2cc2db74194f",
        )


if __name__ == "__main__":
    unittest.main()
