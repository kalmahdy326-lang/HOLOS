import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BREAKDOWN = ROOT / "config" / "episode1" / "episode1_storyboard_breakdown_v1.json"


class Episode1StoryboardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(BREAKDOWN.read_text(encoding="utf-8"))

    def test_provenance_and_approval_state_are_explicit(self):
        source = self.document["source"]
        self.assertEqual(source["provenance_status"],
                         "consolidated chat-derived text extraction; not certified verbatim against original DOCX")
        self.assertTrue(self.document["approval_status"].startswith("DRAFT"))
        self.assertIn("No frame ranges", self.document["timing_policy"])

    def test_all_screenplay_sequences_are_present_in_order(self):
        scenes = self.document["scenes"]
        self.assertEqual([scene["scene_id"] for scene in scenes],
                         ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "PC"])
        self.assertEqual([scene["number"] for scene in scenes], list(range(1, 9)))

    def test_shot_ids_are_unique_and_complete(self):
        shot_ids = [
            shot[0]
            for scene in self.document["scenes"]
            for shot in scene["shots"]
        ]
        self.assertEqual(len(shot_ids), len(set(shot_ids)))
        self.assertGreaterEqual(len(shot_ids), 60)
        self.assertTrue(all(shot_id.startswith(("S0", "PC_")) for shot_id in shot_ids))

    def test_each_shot_has_editorial_and_production_fields(self):
        required = range(7)
        for scene in self.document["scenes"]:
            self.assertGreaterEqual(scene["pages"][0], 1)
            self.assertLessEqual(scene["pages"][1], 25)
            self.assertTrue(scene["continuity"].strip())
            for shot in scene["shots"]:
                self.assertEqual(set(required), set(range(len(shot))))
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in shot))
                self.assertRegex(shot[0], r"^(S0[1-7]_[0-9]{3}|PC_[0-9]{3})$")

    def test_timing_is_not_falsely_locked(self):
        serialized = json.dumps(self.document)
        self.assertNotIn('"start_frame"', serialized)
        self.assertNotIn('"end_frame"', serialized)
        self.assertIn("No frame ranges or durations are assigned", self.document["timing_policy"])


if __name__ == "__main__":
    unittest.main()
