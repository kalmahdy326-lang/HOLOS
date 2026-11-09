"""Environment and asset preflight checks for local HOLOS production."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any


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


def run_preflight(project_root: Path, episode: dict[str, Any]) -> dict[str, Any]:
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

    return {
        "project_root": str(root),
        "tools": tools,
        "assets": assets,
        "missing_assets": [item["path"] for item in assets if not item["exists"]],
        "godot_available": tools["godot"] is not None,
        "ffmpeg_available": tools["ffmpeg"] is not None,
        "ffprobe_available": tools["ffprobe"] is not None,
    }
