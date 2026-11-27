"""Tests for the duration-exact intro/outro music-bed composer."""

from array import array
from pathlib import Path
import tempfile
import unittest
import wave

from tools.compose_episode_music_bed import MusicBedError, compose_music_bed


def write_test_wav(path: Path, value: int, seconds: int = 1) -> None:
    frames = 48_000 * seconds
    samples = array("h", [value, value]) * frames
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(2)
        stream.setsampwidth(2)
        stream.setframerate(48_000)
        stream.writeframes(samples.tobytes())


class MusicBedTests(unittest.TestCase):
    def test_places_intro_and_outro_at_exact_ends_with_silent_middle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intro = root / "intro.wav"
            outro = root / "outro.wav"
            output = root / "bed.wav"
            write_test_wav(intro, 1000)
            write_test_wav(outro, 2000)

            report = compose_music_bed(intro, outro, output, 3.0)

            with wave.open(str(output), "rb") as stream:
                self.assertEqual(stream.getnframes(), 3 * 48_000)
                samples = array("h")
                samples.frombytes(stream.readframes(stream.getnframes()))
            self.assertEqual(samples[0:2], array("h", [1000, 1000]))
            middle = (48_000 * 1 + 24_000) * 2
            self.assertEqual(samples[middle:middle + 2], array("h", [0, 0]))
            self.assertEqual(samples[-2:], array("h", [2000, 2000]))
            self.assertEqual(report["credits_outro"]["start_seconds"], 2.0)
            self.assertEqual(report["duration_seconds"], 3.0)
            self.assertTrue(report["source_modified"] is False)

    def test_rejects_too_short_duration_and_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intro = root / "intro.wav"
            outro = root / "outro.wav"
            output = root / "bed.wav"
            write_test_wav(intro, 1000)
            write_test_wav(outro, 2000)
            with self.assertRaisesRegex(MusicBedError, "exceed the final duration"):
                compose_music_bed(intro, outro, output, 1.5)
            self.assertFalse(output.exists())

    def test_refuses_to_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intro = root / "intro.wav"
            outro = root / "outro.wav"
            output = root / "bed.wav"
            write_test_wav(intro, 1000)
            write_test_wav(outro, 2000)
            output.write_bytes(b"preserve me")
            with self.assertRaisesRegex(MusicBedError, "Refusing to overwrite"):
                compose_music_bed(intro, outro, output, 3.0)
            self.assertEqual(output.read_bytes(), b"preserve me")


if __name__ == "__main__":
    unittest.main()
