"""Subprocess adapter for the HOLOS Godot shot runner."""

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
    *,
    headless: bool = True,
) -> list[str]:
    """Build a deterministic Godot invocation.

    True headless mode is useful for non-rendering tasks. Actual viewport
    capture requires a rendering-capable display; use headless=False with a
    virtual display such as Xvfb on display-less Linux machines.
    """
    command = [godot_executable]
    if headless:
        command.append("--headless")
    command.extend([
        "--path", str(project_dir.resolve()),
        "--script", runner_script,
        "--",
        "--config", str(shot_config.resolve()),
        "--output", str(output_dir.resolve()),
    ])
    return command


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


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
    headless: bool = True,
    command_prefix: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Render one shot into a fresh, project-contained output directory."""
    root = project_root.resolve()
    project = (root / godot_project).resolve()
    config = (root / shot_config).resolve()
    output = (root / output_dir).resolve()

    for label, path in (("Godot project", project), ("shot config", config)):
        if not _inside(root, path):
            raise GodotAdapterError(f"{label} must remain inside project root: {path}")
        if not path.exists():
            raise GodotAdapterError(f"{label} does not exist: {path}")

    if not project.is_dir():
        raise GodotAdapterError(f"Godot project must be a directory: {project}")
    if not (project / "project.godot").is_file():
        raise GodotAdapterError(f"project.godot not found in Godot project: {project}")
    if runner_script.startswith("res://"):
        runner_file = project / runner_script.removeprefix("res://")
        if not runner_file.is_file():
            raise GodotAdapterError(f"Godot runner script not found: {runner_file}")
    if not _inside(root, output):
        raise GodotAdapterError(f"Output directory must remain inside project root: {output}")
    if expected_frame_count <= 0:
        raise GodotAdapterError("expected_frame_count must be positive.")
    if timeout_seconds <= 0:
        raise GodotAdapterError("timeout_seconds must be positive.")

    if output.exists() and any(output.iterdir()):
        raise GodotAdapterError(
            f"Refusing to render into a non-empty directory; use a fresh output path: {output}"
        )
    output.mkdir(parents=True, exist_ok=True)

    godot = find_godot(executable)
    command = [
        *command_prefix,
        *build_render_command(
            godot, project, runner_script, config, output, headless=headless
        ),
    ]

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
    expected_names = [f"frame_{index:06d}.png" for index in range(expected_frame_count)]
    actual_names = [frame.name for frame in frames]
    if actual_names != expected_names:
        raise GodotAdapterError(
            "Frame sequence mismatch. "
            f"Expected {expected_names[0]}..{expected_names[-1]} "
            f"({expected_frame_count} frames), found {len(frames)} frame files."
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
