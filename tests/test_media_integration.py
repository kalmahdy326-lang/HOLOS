"""End-to-end FFmpeg/FFprobe test using generated temporary media.

This test runs only when both executables are available. It never touches
repository source assets.
"""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

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
                "-frames:v", "24", str(frames / "frame_%06d.png"),
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


if __name__ == "__main__":
    unittest.main()
