"""Environment and episode-resource preflight checks for local HOLOS production."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


class ScenePreflightError(RuntimeError):
    """Raised when configured episode scenes cannot be resolved safely."""


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def _assert_no_symlink_components(root: Path, path: Path, label: str) -> None:
    root = root.resolve()
    candidate = Path(os.path.abspath(path))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ScenePreflightError(
            f"{label} must remain inside the project root: {candidate}"
        ) from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ScenePreflightError(
                f"{label} must not traverse symbolic links: {current}"
            )


def _resource_parts(value: Any) -> tuple[str, ...]:
    if not isinstance(value, str) or not value.startswith("res://"):
        raise ValueError("scene must be a Godot res:// path")
    relative = value[len("res://"):]
    parts = relative.split("/")
    parsed = PurePosixPath(relative)
    if (
        not relative
        or "\\" in relative
        or "\x00" in relative
        or parsed.is_absolute()
        or any(part in {"", ".", ".."} for part in parts)
        or (parts and ":" in parts[0])
    ):
        raise ValueError("scene path is not a safe project-relative resource path")
    return tuple(parts)


def inspect_episode_scenes(
    project_root: Path,
    episode: dict[str, Any],
    godot_project: Path = Path("godot"),
) -> dict[str, Any]:
    """Check every configured scene file without following symlinks or writing files."""
    root = project_root.resolve()
    candidate = godot_project if godot_project.is_absolute() else root / godot_project
    _assert_no_symlink_components(root, candidate, "Godot project path")
    project = Path(os.path.abspath(candidate))
    if not _inside(root, project) or not project.is_dir():
        raise ScenePreflightError(
            f"Godot project must be an existing directory inside project root: {project}"
        )

    project_file = project / "project.godot"
    _assert_no_symlink_components(root, project_file, "Godot project configuration")
    if not project_file.is_file():
        raise ScenePreflightError(f"project.godot not found: {project_file}")

    checked: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    unsafe: list[dict[str, str]] = []
    for scene_group in episode["scenes"]:
        for shot in scene_group["shots"]:
            shot_id = shot["shot_id"]
            scene_path = shot.get("scene")
            try:
                parts = _resource_parts(scene_path)
                target = project.joinpath(*parts)
                _assert_no_symlink_components(project, target, f"Scene for shot {shot_id}")
                resolved = target.resolve()
                if not _inside(project, resolved):
                    raise ValueError("scene path resolves outside the Godot project")
                if not resolved.is_file():
                    missing.append({
                        "shot_id": shot_id,
                        "scene": scene_path,
                        "reason": "scene_file_not_found",
                    })
                    checked.append({
                        "shot_id": shot_id,
                        "scene": scene_path,
                        "exists": False,
                    })
                else:
                    checked.append({
                        "shot_id": shot_id,
                        "scene": scene_path,
                        "exists": True,
                    })
            except (ValueError, ScenePreflightError) as exc:
                unsafe.append({
                    "shot_id": shot_id,
                    "scene": scene_path if isinstance(scene_path, str) else repr(scene_path),
                    "reason": str(exc),
                })
                checked.append({
                    "shot_id": shot_id,
                    "scene": scene_path if isinstance(scene_path, str) else repr(scene_path),
                    "exists": False,
                })

    return {
        "godot_project": str(project),
        "project_file": str(project_file),
        "valid": not missing and not unsafe,
        "checked": checked,
        "missing": missing,
        "unsafe": unsafe,
    }


def require_episode_scenes(
    project_root: Path,
    episode: dict[str, Any],
    godot_project: Path = Path("godot"),
) -> dict[str, Any]:
    """Fail before rendering if any configured scene is absent or unsafe."""
    result = inspect_episode_scenes(project_root, episode, godot_project)
    if not result["valid"]:
        details = [
            f"{item['shot_id']}: {item['scene']} ({item['reason']})"
            for item in result["missing"] + result["unsafe"]
        ]
        raise ScenePreflightError(
            "Episode scene preflight failed; no shots were rendered: "
            + "; ".join(details)
        )
    return result


def tool_version(executable: str, version_args: tuple[str, ...] = ("--version",)) -> str | None:
    path = shutil.which(executable)
    if path is None:
        return None
    try:
        result = subprocess.run(
            [path, *version_args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "installed; version check failed"
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else "installed; no version text"


def run_preflight(
    project_root: Path,
    episode: dict[str, Any],
    godot_project: Path = Path("godot"),
) -> dict[str, Any]:
    root = project_root.resolve()
    tools = {
        "python": tool_version("python"),
        "godot": tool_version("godot", ("--version",)),
        "ffmpeg": tool_version("ffmpeg"),
        "ffprobe": tool_version("ffprobe"),
        "git": tool_version("git"),
    }

    assets: list[dict[str, str | bool]] = []
    for scene in episode["scenes"]:
        for shot in scene["shots"]:
            for asset in shot.get("assets", []):
                candidate = (root / asset).resolve()
                exists = candidate == root or root in candidate.parents
                exists = exists and candidate.exists()
                assets.append({"path": asset, "exists": exists})

    for key in ("dialogue", "music"):
        audio_path = episode.get("audio", {}).get(key)
        if audio_path:
            candidate = (root / audio_path).resolve()
            safe = candidate == root or root in candidate.parents
            assets.append({
                "path": audio_path,
                "exists": bool(safe and candidate.is_file()),
            })

    scene_resources = inspect_episode_scenes(root, episode, godot_project)
    return {
        "project_root": str(root),
        "tools": tools,
        "assets": assets,
        "missing_assets": [item["path"] for item in assets if not item["exists"]],
        "scene_resources": scene_resources,
        "godot_available": tools["godot"] is not None,
        "ffmpeg_available": tools["ffmpeg"] is not None,
        "ffprobe_available": tools["ffprobe"] is not None,
    }
