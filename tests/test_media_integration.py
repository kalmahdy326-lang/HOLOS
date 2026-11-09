"""End-to-end FFmpeg/FFprobe test using generated temporary media.

This test runs only when both executables are available. It never touches
repository source assets.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from holos_engine.batch import render_episode_batch
from holos_engine.episode_assembly import stage_episode_frames
from holos_engine.media import assemble_video, probe_media, validate_media


FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")


@unittest.skipUnless(FFMPEG and FFPROBE, "FFmpeg and FFprobe are required")
class FFmpegIntegrationTests(unittest.TestCase):
    def test_assembles_frames_and_mixes_original_audio_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            frames = root / "frames"
            frames.mkdir()
            dialogue = root / "dialogue.wav"
            music = root / "music.wav"

            subprocess.run([
                FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "color=c=navy:s=320x180:r=24:d=1",
                "-start_number", "0", "-frames:v", "24",
                str(frames / "frame_%06d.png"),
            ], check=True, capture_output=True)

            for output, frequency in ((dialogue, "440"), (music, "660")):
                subprocess.run([
                    FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i", f"sine=frequency={frequency}:duration=1",
                    "-c:a", "pcm_s16le", str(output),
                ], check=True, capture_output=True)

            result = assemble_video(
                frames_dir=frames,
                fps=24,
                frame_count=24,
                output=root / "assembled.mp4",
                dialogue=dialogue,
                music=music,
                ffmpeg_executable=FFMPEG,
            )
            self.assertEqual(result["frame_count"], 24)
            self.assertTrue((root / "assembled.mp4").is_file())
            self.assertTrue(dialogue.is_file())
            self.assertTrue(music.is_file())

            metadata = probe_media(root / "assembled.mp4", ffprobe_executable=FFPROBE)
            validation = validate_media(
                metadata,
                width=320,
                height=180,
                fps=24,
                expected_duration=1.0,
                require_audio=True,
                duration_tolerance_seconds=0.15,
            )
            self.assertTrue(validation["valid"], validation["errors"])
            self.assertEqual(validation["audio_stream_count"], 1)


    def test_assembles_two_verified_shot_folders_into_one_episode(self):
        from holos_engine.batch import load_completed_batch_manifest

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            master_frames = root / "master_frames"
            master_frames.mkdir()
            subprocess.run([
                FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "testsrc=size=320x180:rate=24",
                "-frames:v", "4", "-start_number", "0",
                str(master_frames / "frame_%06d.png"),
            ], check=True, capture_output=True)

            episode = {
                "schema_version": 1,
                "episode_id": "ffmpeg_multishot_test",
                "title": "FFmpeg Multi-shot Assembly Test",
                "render": {"width": 320, "height": 180, "fps": 24},
                "audio": {"dialogue": None, "music": None},
                "scenes": [{"scene_id": "scene_01", "shots": [
                    {"shot_id": "SHOT_A", "start_frame": 0, "end_frame": 2},
                    {"shot_id": "SHOT_B", "start_frame": 2, "end_frame": 4},
                ]}],
            }

            def render_fixture(scene, shot, output_dir):
                output_dir.mkdir(parents=True, exist_ok=True)
                offset = 0 if shot["shot_id"] == "SHOT_A" else 2
                for index in range(2):
                    shutil.copy2(
                        master_frames / f"frame_{offset + index:06d}.png",
                        output_dir / f"frame_{index:06d}.png",
                    )
                return {"return_code": 0, "frame_count": 2}

            batch = render_episode_batch(
                project_root=root, episode=episode, mode="debug",
                render_one=render_fixture,
            )
            self.assertTrue(batch["success"])
            _, manifest = load_completed_batch_manifest(
                project_root=root, episode=episode, mode="debug",
            )

            staging_root = root / "output" / ".holos_runtime" / "staged"
            staging_root.mkdir(parents=True)
            staged = stage_episode_frames(
                project_root=root, episode=episode, manifest=manifest,
                staging_dir=staging_root,
            )
            self.assertEqual(staged["frame_count"], 4)
            output = root / "output" / "episode.mp4"
            assembled = assemble_video(
                frames_dir=staging_root, fps=24, frame_count=4, output=output,
                ffmpeg_executable=FFMPEG,
            )
            metadata = probe_media(output, ffprobe_executable=FFPROBE)
            validation = validate_media(
                metadata, width=320, height=180, fps=24,
                expected_duration=4 / 24, require_audio=False,
                duration_tolerance_seconds=0.08,
            )
            self.assertEqual(assembled["frame_count"], 4)
            self.assertTrue(validation["valid"], validation["errors"])
            self.assertTrue(
                (root / "output" / "renders" / "ffmpeg_multishot_test"
                 / "SHOT_A" / "frame_000000.png").is_file()
            )


    def test_cli_assembles_verified_multi_shot_episode(self):
        import json
        import os
        import sys

        from holos_engine.batch import render_episode_batch

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for folder in ("holos_engine", "tools"):
                shutil.copytree(
                    Path(__file__).resolve().parents[1] / folder,
                    root / folder,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                )
            source_frames = root / "source_frames"
            source_frames.mkdir()
            subprocess.run([
                FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "testsrc=size=320x180:rate=24",
                "-frames:v", "4", "-start_number", "0",
                str(source_frames / "frame_%06d.png"),
            ], check=True, capture_output=True)

            episode = {
                "schema_version": 1,
                "episode_id": "cli_episode_test",
                "title": "CLI Episode Assembly Test",
                "render": {"width": 320, "height": 180, "fps": 24},
                "audio": {"dialogue": None, "music": None},
                "scenes": [{"scene_id": "scene_01", "shots": [
                    {"shot_id": "SHOT_A", "start_frame": 0, "end_frame": 2,
                     "scene": "res://unused_fixture.tscn"},
                    {"shot_id": "SHOT_B", "start_frame": 2, "end_frame": 4,
                     "scene": "res://unused_fixture.tscn"},
                ]}],
            }
            episode_dir = root / "examples"
            episode_dir.mkdir()
            episode_path = episode_dir / "episode.json"
            episode_path.write_text(json.dumps(episode, indent=2), encoding="utf-8")

            def render_fixture(scene, shot, output_dir):
                output_dir.mkdir(parents=True, exist_ok=True)
                offset = 0 if shot["shot_id"] == "SHOT_A" else 2
                for index in range(2):
                    shutil.copy2(
                        source_frames / f"frame_{offset + index:06d}.png",
                        output_dir / f"frame_{index:06d}.png",
                    )
                return {"return_code": 0, "frame_count": 2}

            batch = render_episode_batch(
                project_root=root, episode=episode, mode="debug",
                render_one=render_fixture,
            )
            self.assertTrue(batch["success"])

            env = os.environ.copy()
            env["PYTHONPATH"] = str(root)
            output = root / "output" / "episode.mp4"
            command = [
                sys.executable, str(root / "tools" / "holos.py"),
                "--project-root", str(root),
                "assemble-episode",
                "--episode", "examples/episode.json",
                "--mode", "debug",
                "--output", "output/episode.mp4",
            ]
            result = subprocess.run(
                command, cwd=root, env=env, capture_output=True,
                text=True, timeout=120, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertTrue(output.is_file())

            report_path = (
                root / "output" / "reports"
                / "cli_episode_test-debug-episode-assembly.json"
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertTrue(report["validation"]["valid"], report["validation"]["errors"])
            self.assertEqual(report["ordered_shots"], ["SHOT_A", "SHOT_B"])
            self.assertEqual(report["frame_staging"]["frame_count"], 4)
            self.assertTrue(
                (root / "output" / "renders" / "cli_episode_test"
                 / "SHOT_A" / "frame_000000.png").is_file()
            )
            self.assertFalse((root / "output" / ".holos_runtime"
                              / "episode-frame-sequence-").exists())


if __name__ == "__main__":
    unittest.main()
