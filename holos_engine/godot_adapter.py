"""Subprocess adapter for the HOLOS Godot shot runner.

The adapter does not own animation logic. It passes a validated shot contract
to a Godot project, then verifies that the expected frame files were produced.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any


class GodotAdapterError(RuntimeError):
    """Raised when Godot cannot render a configured shot."""


def find_godot(executable: str | None = None) -> str:
    candidate = executable or shutil.which("godot") or shutil.which("godot4")
    if not candidate:
        raise GodotAdapterError(
            "Godot executable not found. Install Godot 4.x or pass its executable path."
        )
    return str(candidate)


def build_render_command(
    godot_executable: str,
    project_dir: Path,
    runner_script: str,
    shot_config: Path,
    output_dir: Path,
) -> list[str]:
    """Build a deterministic headless Godot invocation."""
    return [
        godot_executable,
        "--headless",
        "--path", str(project_dir.resolve()),
        "--script", runner_script,
        "--",
        "--config", str(shot_config.resolve()),
        "--output", str(output_dir.resolve()),
    ]


def render_shot(
    *,
    project_root: Path,
    godot_project: Path,
    runner_script: str,
    shot_config: Path,
    output_dir: Path,
    expected_frame_count: int,
    executable: str | None = None,
    timeout_seconds: int = 3600,
) -> dict[str, Any]:
    """Render one shot and require every expected PNG frame.

    The caller is responsible for writing the shot JSON and for ensuring that
    output_dir is a new or explicitly approved destination.
    """
    root = project_root.resolve()
    project = (root / godot_project).resolve()
    config = (root / shot_config).resolve()
    output = (root / output_dir).resolve()

    for label, path in (("Godot project", project), ("shot config", config)):
        if root not in path.parents and path != root:
            raise GodotAdapterError(f"{label} must remain inside project root: {path}")
        if not path.exists():
            raise GodotAdapterError(f"{label} does not exist: {path}")

    if expected_frame_count <= 0:
        raise GodotAdapterError("expected_frame_count must be positive.")

    output.mkdir(parents=True, exist_ok=True)
    godot = find_godot(executable)
    command = build_render_command(
        godot, project, runner_script, config, output
    )

    try:
        result = subprocess.run(
            command,
            cwd=project,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise GodotAdapterError(
            f"Godot render timed out after {timeout_seconds} seconds."
        ) from exc
    except OSError as exc:
        raise GodotAdapterError(f"Could not start Godot: {exc}") from exc

    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise GodotAdapterError(
            f"Godot exited with code {result.returncode}. {details[-4000:]}"
        )

    frames = sorted(output.glob("frame_*.png"))
    if len(frames) != expected_frame_count:
        raise GodotAdapterError(
            f"Expected {expected_frame_count} frames, found {len(frames)} in {output}."
        )

    return {
        "command": command,
        "return_code": result.returncode,
        "frame_count": len(frames),
        "first_frame": str(frames[0]),
        "last_frame": str(frames[-1]),
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
