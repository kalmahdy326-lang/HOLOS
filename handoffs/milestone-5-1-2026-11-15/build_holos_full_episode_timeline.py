#!/usr/bin/env python3
"""Compatibility entry point for the repository-relative timeline builder."""
from __future__ import annotations

import runpy
from pathlib import Path
import sys


def find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "tools" / "build_holos_full_episode_timeline.py").is_file():
            return candidate
    raise RuntimeError("Cannot locate repository root containing tools/build_holos_full_episode_timeline.py")


def main() -> None:
    repo_root = find_repo_root()
    builder = repo_root / "tools" / "build_holos_full_episode_timeline.py"
    runpy.run_path(str(builder), run_name="__main__")


if __name__ == "__main__":
    main()
