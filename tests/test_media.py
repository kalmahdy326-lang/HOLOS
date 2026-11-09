"""Unit tests for FFmpeg command construction and media validation."""

import tempfile
import unittest
from pathlib import Path

from holos_engine.media import (
    MediaError,
    build_assembly_command,
    validate_media,
)


class MediaTests(unittest.TestCase):
    def test_command_maps_dialogue_audio_and_sets_exact_frame_count(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            dialogue = root / "dialogue.wav"
            dialogue.write_bytes(b"placeholder")
            command = build_assembly_command(
                ffmpeg="ffmpeg",
                frames_dir=root / "frames",
                fps=24,
                frame_count=240,
                output=root / "episode.mp4",
                dialogue=dialogue,
            )
            self.assertIn("-frames:v", command)
            self.assertEqual(command[command.index("-frames:v") + 1], "240")
            self.assertIn("1:a:0?", command)
            self.assertIn("apad", command)
            self.assertIn("yuv420p", command)

    def test_command_mixes_two_audio_sources_without_modifying_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            dialogue = root / "dialogue.wav"
            music = root / "music.wav"
            dialogue.write_bytes(b"dialogue")
            music.write_bytes(b"music")
            command = build_assembly_command(
                ffmpeg="ffmpeg",
                frames_dir=root / "frames",
                fps=24,
                frame_count=24,
                output=root / "out.mp4",
                dialogue=dialogue,
                music=music,
            )
            self.assertIn("-filter_complex", command)
            self.assertTrue(any("amix=inputs=2" in arg for arg in command))

    def test_rejects_missing_audio(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(MediaError, "does not exist"):
                build_assembly_command(
                    ffmpeg="ffmpeg",
                    frames_dir=root,
                    fps=24,
                    frame_count=24,
                    output=root / "out.mp4",
                    dialogue=root / "missing.wav",
                )

    def test_validates_expected_video_and_audio_metadata(self):
        metadata = {
            "streams": [
                {
                    "codec_type": "video",
                    "width": 1280,
                    "height": 720,
                    "avg_frame_rate": "24/1",
                    "start_time": "0.000000",
                    "duration": "10.000000",
                },
                {
                    "codec_type": "audio", "codec_name": "aac",
                    "start_time": "0.000000", "duration": "10.000000",
                },
            ],
            "format": {"duration": "10.000"},
        }
        result = validate_media(
            metadata, width=1280, height=720, fps=24,
            expected_duration=10.0, require_audio=True,
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["audio_stream_count"], 1)

    def test_detects_metadata_mismatch(self):
        metadata = {
            "streams": [
                {"codec_type": "video", "width": 640, "height": 360,
                 "avg_frame_rate": "30/1"}
            ],
            "format": {"duration": "8.0"},
        }
        result = validate_media(
            metadata, width=1280, height=720, fps=24,
            expected_duration=10.0, require_audio=True,
        )
        self.assertFalse(result["valid"])
        self.assertGreaterEqual(len(result["errors"]), 4)


    def test_detects_audio_video_start_offset_outside_tolerance(self):
        metadata = {
            "streams": [
                {"codec_type": "video", "width": 1280, "height": 720,
                 "avg_frame_rate": "24/1", "start_time": "0.000",
                 "duration": "10.000"},
                {"codec_type": "audio", "start_time": "0.150",
                 "duration": "10.000"},
            ],
            "format": {"duration": "10.000"},
        }
        result = validate_media(
            metadata, width=1280, height=720, fps=24,
            expected_duration=10.0, require_audio=True,
            sync_tolerance_seconds=0.08,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(any("starts +0.150s" in item for item in result["errors"]))
        self.assertTrue(result["av_sync"]["checked"])

    def test_detects_audio_video_duration_mismatch(self):
        metadata = {
            "streams": [
                {"codec_type": "video", "width": 1280, "height": 720,
                 "avg_frame_rate": "24/1", "start_time": "0.000",
                 "duration": "10.000"},
                {"codec_type": "audio", "start_time": "0.000",
                 "duration": "9.500"},
            ],
            "format": {"duration": "10.000"},
        }
        result = validate_media(
            metadata, width=1280, height=720, fps=24,
            expected_duration=10.0, require_audio=True,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(any("duration differs from video" in item
                            for item in result["errors"]))

    def test_uses_duration_timestamp_when_direct_stream_duration_is_absent(self):
        metadata = {
            "streams": [
                {"codec_type": "video", "width": 1280, "height": 720,
                 "avg_frame_rate": "24/1", "start_time": "0",
                 "duration_ts": "240000", "time_base": "1/24000"},
                {"codec_type": "audio", "start_time": "0",
                 "duration_ts": "480000", "time_base": "1/48000"},
            ],
            "format": {"duration": "10.0"},
        }
        result = validate_media(
            metadata, width=1280, height=720, fps=24,
            expected_duration=10.0, require_audio=True,
        )
        self.assertTrue(result["valid"], result["errors"])


if __name__ == "__main__":
    unittest.main()
