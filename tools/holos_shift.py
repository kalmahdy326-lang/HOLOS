#!/usr/bin/env python3
"""Bounded deterministic HOLOS validation runner; not an autonomous AI agent.

Each phase exits when its checks finish. The time limit is a ceiling, never
an instruction to idle. Only generated reports are written; source assets and
tracked production files are read-only.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def run_check(name, command, deadline, env=None):
    remaining = int(deadline - time.monotonic())
    if remaining <= 0:
        return {"name": name, "status": "not_run_time_budget_exhausted"}
    started = time.monotonic()
    item = {"name": name, "command": shlex.join(command),
            "started_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                                text=True, timeout=remaining, check=False)
        item.update({"status": "passed" if result.returncode == 0 else "failed",
                     "return_code": result.returncode,
                     "stdout_tail": (result.stdout or "")[-10000:],
                     "stderr_tail": (result.stderr or "")[-10000:]})
    except subprocess.TimeoutExpired:
        item.update({"status": "timed_out", "return_code": None})
    except OSError as exc:
        item.update({"status": "could_not_start", "error": str(exc)})
    item["duration_seconds"] = round(time.monotonic() - started, 3)
    item["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    return item


def asset_snapshot():
    base = ROOT / "godot"
    candidates = {"khaled": [], "kevin": []}
    if base.is_dir():
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".tscn", ".scn", ".gd", ".tres", ".res"}:
                for character in candidates:
                    if character in path.name.lower():
                        candidates[character].append(path.relative_to(ROOT).as_posix())
    return {
        "godot_project_present": (base / "project.godot").is_file(),
        "character_named_source_candidates": candidates,
        "interpretation": "Filename scan only; not proof of original rig identity, dependency loading, or animation acceptance."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("foundation", "godot"), required=True)
    parser.add_argument("--max-minutes", type=int, required=True)
    parser.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "local"))
    args = parser.parse_args()
    limit = 360 if args.phase == "foundation" else 120
    if not 1 <= args.max_minutes <= limit:
        parser.error("max-minutes exceeds the documented phase ceiling")
    if not args.run_id.replace("-", "").replace("_", "").isalnum():
        parser.error("run-id may contain only letters, digits, hyphens, and underscores")

    start = time.monotonic()
    deadline = start + args.max_minutes * 60
    py = sys.executable
    if args.phase == "foundation":
        stamp = args.run_id
        tasks = [
            ("python_regression_suite", [py, "-m", "unittest", "discover", "-s", "tests", "-v"], None),
            ("read_only_source_inventory", [py, "tools/holos.py", "inventory", "--output", "output/reports/shift-" + stamp + "-inventory.json"], None),
            ("godot_resource_audit", [py, "tools/holos.py", "audit-godot-assets", "--godot-project", "godot", "--output", "output/reports/shift-" + stamp + "-godot-assets.json"], None),
        ]
        checks = []
    else:
        godot = os.environ.get("HOLOS_GODOT")
        if not godot or not Path(godot).is_file():
            tasks = []
            checks = [{"name": "godot_executable_available", "status": "blocked",
                       "error": "HOLOS_GODOT is not an executable file."}]
        else:
            env = os.environ.copy()
            env.update({"HOLOS_GODOT": godot, "HOLOS_GODOT_HEADLESS": "0",
                        "HOLOS_GODOT_DISPLAY_WRAPPER": "xvfb-run",
                        "LIBGL_ALWAYS_SOFTWARE": "1"})
            tasks = [
                ("godot_project_import_and_parse", [godot, "--headless", "--editor", "--path", "godot", "--quit"], env),
                ("godot_offscreen_integration_suite", [py, "-m", "unittest", "discover", "-s", "tests", "-p", "test_godot_integration.py", "-v"], env),
            ]
            checks = []

    for name, command, env in tasks:
        checks.append(run_check(name, command, deadline, env))

    failed = sum(x["status"] in {"failed", "could_not_start", "timed_out", "blocked"} for x in checks)
    report = {
        "schema_version": 1, "project": "HOLOS", "phase": args.phase,
        "run_id": args.run_id, "time_ceiling_minutes": args.max_minutes,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "status": "passed" if failed == 0 and all(x["status"] == "passed" for x in checks) else "incomplete_or_failed",
        "checks": checks, "asset_snapshot": asset_snapshot(),
        "scope_boundary": "Deterministic repository checks only. This is not an AI coding agent. It does not author scenes, animate characters, recover external files, generate artwork/music, alter source assets, commit changes, or certify a finished episode."
    }
    out = ROOT / "output" / "automation-reports"
    out.mkdir(parents=True, exist_ok=True)
    target = out / ("production-shift-" + args.run_id + "-" + args.phase + ".json")
    if target.exists():
        raise FileExistsError("Refusing to overwrite " + str(target))
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        lines = ["## HOLOS production shift — " + args.phase, "",
                 "- Status: **" + report["status"] + "**",
                 "- Elapsed seconds: " + str(report["elapsed_seconds"]),
                 "- Report: " + target.relative_to(ROOT).as_posix()]
        for check in checks:
            lines.append("- " + check["name"] + ": **" + check["status"] + "**")
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write("\n".join(lines) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
