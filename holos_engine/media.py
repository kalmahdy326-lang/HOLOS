"""FFmpeg assembly and FFprobe validation for HOLOS episode renders.

Source frames and audio are treated as read-only inputs. Assembly refuses to
overwrite an existing output file.
"""

from __future__ import annotations

from fractions import Fraction
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


class MediaError(RuntimeError):
    """Raised when media assembly or validation fails."""


def _executable(name: str, explicit: str | None = None) -> str:
    path = explicit or shutil.which(name)
    if not path:
        raise MediaError(f"Required executable not found: {name}")
    return str(path)


def _frame_files(frames_dir: Path, frame_count: int) -> list[Path]:
    if frame_count <= 0:
        raise MediaError("frame_count must be positive.")
    expected = [frames_dir / f"frame_{i:06d}.png" for i in range(frame_count)]
    missing = [str(path) for path in expected if not path.is_file()]
    if missing:
        raise MediaError(
            f"Frame sequence is incomplete: {len(missing)} of {frame_count} frames missing. "
            f"First missing: {missing[0]}"
        )
    return expected


def build_assembly_command(
    *,
    ffmpeg: str,
    frames_dir: Path,
    fps: int | float,
    frame_count: int,
    output: Path,
    dialogue: Path | None = None,
    music: Path | None = None,
) -> list[str]:
    """Build an explicit constant-frame-rate H.264/AAC assembly command."""
    if fps <= 0:
        raise MediaError("fps must be positive.")
    if frame_count <= 0:
        raise MediaError("frame_count must be positive.")

    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-n",
        "-framerate", str(fps), "-start_number", "0",
        "-i", str((frames_dir / "frame_%06d.png").resolve()),
    ]

    audio_inputs: list[Path] = []
    for audio_path in (dialogue, music):
        if audio_path is not None:
            if not audio_path.is_file():
                raise MediaError(f"Audio source does not exist: {audio_path}")
            audio_inputs.append(audio_path.resolve())
            command.extend(["-i", str(audio_path.resolve())])

    if len(audio_inputs) == 2:
        command.extend([
            "-filter_complex",
            "[1:a:0][2:a:0]amix=inputs=2:duration=longest:dropout_transition=0,apad[aout]",
            "-map", "0:v:0", "-map", "[aout]",
            "-c:a", "aac", "-b:a", "192k",
        ])
    elif len(audio_inputs) == 1:
        command.extend([
            "-map", "0:v:0", "-map", "1:a:0?",
            "-af", "apad",
            "-c:a", "aac", "-b:a", "192k",
        ])
    else:
        command.extend(["-map", "0:v:0", "-an"])

    duration = frame_count / float(fps)
    command.extend([
        "-frames:v", str(frame_count),
        "-t", f"{duration:.9f}",
        "-r", str(fps),
        "-fps_mode", "cfr",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output.resolve()),
    ])
    return command


def assemble_video(
    *,
    frames_dir: Path,
    fps: int | float,
    frame_count: int,
    output: Path,
    dialogue: Path | None = None,
    music: Path | None = None,
    ffmpeg_executable: str | None = None,
    timeout_seconds: int = 7200,
) -> dict[str, Any]:
    """Assemble validated numbered frames and optional audio into a new MP4."""
    frames_dir = frames_dir.resolve()
    output = output.resolve()
    if not frames_dir.is_dir():
        raise MediaError(f"Frames directory does not exist: {frames_dir}")
    _frame_files(frames_dir, frame_count)
    if output.exists():
        raise MediaError(f"Refusing to overwrite existing output: {output}")
    if timeout_seconds <= 0:
        raise MediaError("timeout_seconds must be positive.")

    output.parent.mkdir(parents=True, exist_ok=True)
    command = build_assembly_command(
        ffmpeg=_executable("ffmpeg", ffmpeg_executable),
        frames_dir=frames_dir,
        fps=fps,
        frame_count=frame_count,
        output=output,
        dialogue=dialogue,
        music=music,
    )
    try:
        result = subprocess.run(
            command, capture_output=True, text=True,
            timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise MediaError(f"FFmpeg timed out after {timeout_seconds} seconds.") from exc
    except OSError as exc:
        raise MediaError(f"Could not start FFmpeg: {exc}") from exc

    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise MediaError(f"FFmpeg exited with code {result.returncode}: {details[-4000:]}")
    if not output.is_file() or output.stat().st_size == 0:
        raise MediaError("FFmpeg reported success but no non-empty output file exists.")

    return {
        "output": str(output),
        "frame_count": frame_count,
        "fps": fps,
        "expected_duration_seconds": frame_count / float(fps),
        "audio_inputs": [str(p) for p in (dialogue, music) if p is not None],
        "command": command,
        "return_code": result.returncode,
    }


def probe_media(
    path: Path,
    *,
    ffprobe_executable: str | None = None,
    timeout_seconds: int = 30,
) -> dict[str, Any]:
    """Return FFprobe JSON metadata for a media file."""
    path = path.resolve()
    if not path.is_file():
        raise MediaError(f"Media file does not exist: {path}")
    command = [
        _executable("ffprobe", ffprobe_executable),
        "-v", "error", "-show_streams", "-show_format", "-of", "json",
        str(path),
    ]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True,
            timeout=timeout_seconds, check=False,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise MediaError(f"FFprobe could not inspect {path}: {exc}") from exc
    if result.returncode != 0:
        raise MediaError(f"FFprobe failed: {(result.stderr or result.stdout)[-4000:]}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise MediaError("FFprobe returned invalid JSON.") from exc


def validate_media(
    metadata: dict[str, Any],
    *,
    width: int,
    height: int,
    fps: int | float,
    expected_duration: float,
    require_audio: bool = True,
    duration_tolerance_seconds: float = 0.08,
) -> dict[str, Any]:
    """Validate video dimensions, frame rate, duration, and audio presence."""
    streams = metadata.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    errors: list[str] = []

    if video is None:
        errors.append("No video stream found.")
    else:
        if int(video.get("width", -1)) != width:
            errors.append(f"Width mismatch: expected {width}, got {video.get('width')}.")
        if int(video.get("height", -1)) != height:
            errors.append(f"Height mismatch: expected {height}, got {video.get('height')}.")
        rate = video.get("avg_frame_rate") or video.get("r_frame_rate")
        try:
            actual_fps = float(Fraction(rate))
            if abs(actual_fps - float(fps)) > 0.001:
                errors.append(f"Frame-rate mismatch: expected {fps}, got {rate}.")
        except (ValueError, ZeroDivisionError, TypeError):
            errors.append(f"Could not interpret video frame rate: {rate!r}.")

    duration_value = metadata.get("format", {}).get("duration")
    try:
        actual_duration = float(duration_value)
        if abs(actual_duration - expected_duration) > duration_tolerance_seconds:
            errors.append(
                f"Duration mismatch: expected {expected_duration:.3f}s, "
                f"got {actual_duration:.3f}s."
            )
    except (ValueError, TypeError):
        actual_duration = None
        errors.append("Could not read media duration.")

    if require_audio and not audio:
        errors.append("Audio stream is required but missing.")

    return {
        "valid": not errors,
        "errors": errors,
        "video_stream": video,
        "audio_stream_count": len(audio),
        "duration_seconds": actual_duration,
        "expected_duration_seconds": expected_duration,
    }
