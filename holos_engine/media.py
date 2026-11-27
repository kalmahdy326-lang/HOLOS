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


def _stream_time_seconds(stream: dict[str, Any], field: str) -> float | None:
    value = stream.get(field)
    if value not in (None, "", "N/A"):
        try:
            return float(value)
        except (TypeError, ValueError):
            pass

    if field == "duration":
        duration_ts = stream.get("duration_ts")
        time_base = stream.get("time_base")
        try:
            if duration_ts not in (None, "", "N/A") and time_base:
                return float(int(duration_ts) * Fraction(str(time_base)))
        except (TypeError, ValueError, ZeroDivisionError):
            pass
    return None



def validate_media(
    metadata: dict[str, Any],
    *,
    width: int,
    height: int,
    fps: int | float,
    expected_duration: float,
    require_audio: bool = True,
    duration_tolerance_seconds: float = 0.08,
    sync_tolerance_seconds: float = 0.08,
) -> dict[str, Any]:
    """Validate container and stream completeness plus audio/video alignment."""
    if duration_tolerance_seconds < 0 or sync_tolerance_seconds < 0:
        raise MediaError("Media validation tolerances must be non-negative.")

    errors: list[str] = []
    if not isinstance(metadata, dict):
        return {
            "valid": False,
            "errors": ["FFprobe metadata must be a JSON object."],
            "video_stream": None,
            "video_duration_seconds": None,
            "audio_stream_count": 0,
            "duration_seconds": None,
            "expected_duration_seconds": expected_duration,
            "av_sync": {
                "checked": False,
                "tolerance_seconds": sync_tolerance_seconds,
                "streams": [],
            },
        }

    raw_streams = metadata.get("streams", [])
    if not isinstance(raw_streams, list):
        errors.append("FFprobe streams metadata is not a list.")
        raw_streams = []
    streams: list[dict[str, Any]] = []
    for index, stream in enumerate(raw_streams):
        if isinstance(stream, dict):
            streams.append(stream)
        else:
            errors.append(f"FFprobe stream entry {index} is not an object.")

    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    video = video_streams[0] if video_streams else None

    if not video_streams:
        errors.append("No video stream found.")
    elif len(video_streams) > 1:
        errors.append(f"Expected one video stream, found {len(video_streams)}.")

    if video is not None:
        for field, expected in (("width", width), ("height", height)):
            try:
                actual = int(video.get(field, -1))
            except (TypeError, ValueError):
                actual = -1
            if actual != expected:
                errors.append(f"{field.title()} mismatch: expected {expected}, got {video.get(field)}.")

        rate = video.get("avg_frame_rate") or video.get("r_frame_rate")
        try:
            actual_fps = float(Fraction(rate))
            if abs(actual_fps - float(fps)) > 0.001:
                errors.append(f"Frame-rate mismatch: expected {fps}, got {rate}.")
        except (ValueError, ZeroDivisionError, TypeError):
            errors.append(f"Could not interpret video frame rate: {rate!r}.")

    format_metadata = metadata.get("format", {})
    if not isinstance(format_metadata, dict):
        errors.append("FFprobe format metadata is not an object.")
        format_metadata = {}
    duration_value = format_metadata.get("duration")
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

    video_duration = None
    if video is not None:
        video_duration = _stream_time_seconds(video, "duration")
        if video_duration is None:
            errors.append("Video stream duration is missing; output completeness cannot be verified.")
        elif abs(video_duration - expected_duration) > duration_tolerance_seconds:
            errors.append(
                f"Video stream duration mismatch: expected {expected_duration:.3f}s, "
                f"got {video_duration:.3f}s."
            )

    if require_audio and not audio:
        errors.append("Audio stream is required but missing.")

    # If an audio stream is present, validate it even when audio is optional.
    # Optional means absence is allowed; it does not mean a present stream may
    # be truncated or misaligned without detection.
    sync_checks: list[dict[str, Any]] = []
    if video is not None and audio:
        video_start = _stream_time_seconds(video, "start_time")
        if video_start is None:
            errors.append("Video stream start time is missing; A/V sync cannot be verified.")

        for index, stream in enumerate(audio):
            audio_start = _stream_time_seconds(stream, "start_time")
            audio_duration = _stream_time_seconds(stream, "duration")
            check: dict[str, Any] = {
                "audio_stream_index": index,
                "start_delta_seconds": None,
                "duration_delta_seconds": None,
                "valid": False,
            }
            if video_start is None or audio_start is None:
                errors.append(
                    f"Audio stream {index} start time is missing; A/V sync cannot be verified."
                )
            else:
                start_delta = audio_start - video_start
                check["start_delta_seconds"] = start_delta
                if abs(start_delta) > sync_tolerance_seconds:
                    errors.append(
                        f"Audio stream {index} starts {start_delta:+.3f}s relative to video; "
                        f"tolerance is {sync_tolerance_seconds:.3f}s."
                    )

            if video_duration is None or audio_duration is None:
                errors.append(
                    f"Audio stream {index} duration is missing; A/V sync cannot be verified."
                )
            else:
                duration_delta = audio_duration - video_duration
                check["duration_delta_seconds"] = duration_delta
                if abs(duration_delta) > sync_tolerance_seconds:
                    errors.append(
                        f"Audio stream {index} duration differs from video by "
                        f"{duration_delta:+.3f}s; tolerance is {sync_tolerance_seconds:.3f}s."
                    )

            check["valid"] = (
                check["start_delta_seconds"] is not None
                and check["duration_delta_seconds"] is not None
                and abs(check["start_delta_seconds"]) <= sync_tolerance_seconds
                and abs(check["duration_delta_seconds"]) <= sync_tolerance_seconds
            )
            sync_checks.append(check)

    return {
        "valid": not errors,
        "errors": errors,
        "video_stream": video,
        "video_duration_seconds": video_duration,
        "audio_stream_count": len(audio),
        "duration_seconds": actual_duration,
        "expected_duration_seconds": expected_duration,
        "av_sync": {
            "checked": bool(audio and video is not None),
            "tolerance_seconds": sync_tolerance_seconds,
            "streams": sync_checks,
        },
    }
