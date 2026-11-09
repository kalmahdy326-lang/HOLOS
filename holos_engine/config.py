"""Load and validate versioned HOLOS episode configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when an episode configuration is invalid."""


def load_episode(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigError(f"Episode configuration not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"Invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc

    validate_episode(data)
    return data


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigError(message)


def validate_episode(data: Any) -> None:
    """Validate the v1 configuration contract without external dependencies."""
    _require(isinstance(data, dict), "Episode root must be a JSON object.")
    _require(data.get("schema_version") == 1, "schema_version must be integer 1.")
    _require(isinstance(data.get("episode_id"), str) and data["episode_id"].strip(),
             "episode_id must be a non-empty string.")
    _require(isinstance(data.get("title"), str) and data["title"].strip(),
             "title must be a non-empty string.")

    render = data.get("render")
    _require(isinstance(render, dict), "render must be an object.")
    _require(isinstance(render.get("width"), int) and render["width"] > 0,
             "render.width must be a positive integer.")
    _require(isinstance(render.get("height"), int) and render["height"] > 0,
             "render.height must be a positive integer.")
    fps = render.get("fps")
    _require(isinstance(fps, (int, float)) and not isinstance(fps, bool) and fps > 0,
             "render.fps must be a positive number.")
    debug_overlay = render.get("debug_overlay", False)
    _require(isinstance(debug_overlay, bool),
             "render.debug_overlay must be a boolean.")

    scenes = data.get("scenes")
    _require(isinstance(scenes, list) and scenes, "scenes must be a non-empty array.")
    seen_scenes: set[str] = set()
    seen_shots: set[str] = set()

    for scene_index, scene in enumerate(scenes):
        prefix = f"scenes[{scene_index}]"
        _require(isinstance(scene, dict), f"{prefix} must be an object.")
        scene_id = scene.get("scene_id")
        _require(isinstance(scene_id, str) and scene_id.strip(),
                 f"{prefix}.scene_id must be a non-empty string.")
        _require(scene_id not in seen_scenes, f"Duplicate scene_id: {scene_id}")
        seen_scenes.add(scene_id)

        shots = scene.get("shots")
        _require(isinstance(shots, list) and shots, f"{prefix}.shots must be non-empty.")
        for shot_index, shot in enumerate(shots):
            shot_prefix = f"{prefix}.shots[{shot_index}]"
            _require(isinstance(shot, dict), f"{shot_prefix} must be an object.")
            shot_id = shot.get("shot_id")
            _require(isinstance(shot_id, str) and shot_id.strip(),
                     f"{shot_prefix}.shot_id must be a non-empty string.")
            _require(shot_id not in seen_shots, f"Duplicate shot_id: {shot_id}")
            seen_shots.add(shot_id)

            start = shot.get("start_frame")
            end = shot.get("end_frame")
            _require(isinstance(start, int) and start >= 0,
                     f"{shot_prefix}.start_frame must be an integer >= 0.")
            _require(isinstance(end, int) and end > start,
                     f"{shot_prefix}.end_frame must be greater than start_frame.")

            characters = shot.get("characters", [])
            _require(isinstance(characters, list)
                     and all(isinstance(item, str) and item for item in characters),
                     f"{shot_prefix}.characters must be an array of non-empty strings.")

    audio = data.get("audio", {})
    _require(isinstance(audio, dict), "audio must be an object.")
    for key in ("dialogue", "music"):
        value = audio.get(key)
        _require(value is None or isinstance(value, str),
                 f"audio.{key} must be a path string or null.")
    sync_tolerance_ms = audio.get("sync_tolerance_ms", 80)
    _require(
        isinstance(sync_tolerance_ms, (int, float))
        and not isinstance(sync_tolerance_ms, bool)
        and sync_tolerance_ms >= 0,
        "audio.sync_tolerance_ms must be a non-negative number.",
    )
