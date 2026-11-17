"""Initial orchestration layer for the HOLOS Local Production Engine."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .preflight import run_preflight


def write_preflight_report(
    project_root: Path,
    episode: dict[str, Any],
    godot_project: Path = Path("godot"),
) -> Path:
    report_dir = project_root / "output" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{episode['episode_id']}-preflight.json"
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "engine_version": "0.1.0",
        "episode_id": episode["episode_id"],
        "status": "preflight_only",
        "checks": run_preflight(project_root, episode, godot_project),
        "notes": [
            "This report does not indicate that any shots were rendered.",
            "Scene checks verify file paths only; they do not load scenes in Godot or prove runtime compatibility.",
        ],
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report_path
