"""Tests for safe ordering of frames from separate shot directories."""

from pathlib import Path
import tempfile
import unittest

from holos_engine.batch import (
    BatchRenderError,
    load_completed_batch_manifest,
    render_episode_batch,
)
from holos_engine.episode_assembly import stage_episode_frames


EPISODE = {
    "schema_version": 1,
    "episode_id": "assembly_test",
    "title": "Assembly Test",
    "render": {"width": 320, "height": 180, "fps": 24},
    "audio": {"dialogue": None, "music": None},
    "scenes": [
        {"scene_id": "scene_01", "shots": [
            {"shot_id": "S01_A", "start_frame": 0, "end_frame": 2},
            {"shot_id": "S01_B", "start_frame": 2, "end_frame": 4},
        ]},
    ],
}


class EpisodeFrameStagingTests(unittest.TestCase):
    def test_stages_separate_shot_folders_in_episode_order_without_changing_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            def render(scene, shot, output_dir):
                output_dir.mkdir(parents=True, exist_ok=True)
                count = shot["end_frame"] - shot["start_frame"]
                for index in range(count):
                    payload = f"{shot['shot_id']}:{index}".encode("utf-8")
                    (output_dir / f"frame_{index:06d}.png").write_bytes(payload)
                return {"return_code": 0, "frame_count": count}

            result = render_episode_batch(
                project_root=root, episode=EPISODE, mode="debug", render_one=render,
            )
            self.assertTrue(result["success"])
            manifest_path, manifest = load_completed_batch_manifest(
                project_root=root, episode=EPISODE, mode="debug",
            )

            staging = root / "output" / ".holos_runtime" / "assembly-frames"
            staged = stage_episode_frames(
                project_root=root,
                episode=EPISODE,
                manifest=manifest,
                staging_dir=staging,
            )
            self.assertEqual(staged["frame_count"], 4)
            self.assertEqual(staged["ordered_shots"], ["S01_A", "S01_B"])
            self.assertEqual(
                [(staging / f"frame_{i:06d}.png").read_bytes() for i in range(4)],
                [b"S01_A:0", b"S01_A:1", b"S01_B:0", b"S01_B:1"],
            )
            self.assertTrue(manifest_path.is_file())
            self.assertEqual(
                (root / "output" / "renders" / "assembly_test" / "debug" / "S01_A"
                 / "frame_000000.png").read_bytes(),
                b"S01_A:0",
            )

    def test_modified_completed_frame_invalidates_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            def render(scene, shot, output_dir):
                output_dir.mkdir(parents=True, exist_ok=True)
                for index in range(shot["end_frame"] - shot["start_frame"]):
                    (output_dir / f"frame_{index:06d}.png").write_bytes(b"original")
                return {}

            render_episode_batch(
                project_root=root, episode=EPISODE, mode="debug", render_one=render,
            )
            changed = (
                root / "output" / "renders" / "assembly_test" / "debug" / "S01_A"
                / "frame_000000.png"
            )
            changed.write_bytes(b"modified")
            with self.assertRaisesRegex(BatchRenderError, "has changed"):
                load_completed_batch_manifest(
                    project_root=root, episode=EPISODE, mode="debug",
                )


if __name__ == "__main__":
    unittest.main()
