#!/usr/bin/env bash
# Informational repository snapshot only. This script never establishes production readiness.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)"; then
  printf '%s\n' 'repository_state_audit: unable to locate Git repository root' >&2
  exit 2
fi
REPO_ROOT="$(cd -- "$REPO_ROOT" && pwd -P)"
REPORT_PATH="$REPO_ROOT/production/quality/repository_state_audit_report.json"
export REPO_ROOT REPORT_PATH

python3 - <<'PY'
import hashlib
import json
import os
import subprocess
from pathlib import Path

root = Path(os.environ["REPO_ROOT"])
report = Path(os.environ["REPORT_PATH"])
report_rel = report.relative_to(root).as_posix()

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL).decode("utf-8", "replace").strip()

branch = git("branch", "--show-current")
commit = git("rev-parse", "HEAD")
# Parse NUL-delimited porcelain output so unusual filenames remain safe. Exclude this
# report from both tracked-change and untracked counts, regardless of whether it exists.
raw = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain=v1", "-z", "--untracked-files=all"])
entries = raw.split(b"\0")
working_tree_count = 0
untracked_count = 0
i = 0
while i < len(entries) and entries[i]:
    record = entries[i]
    i += 1
    if len(record) < 4:
        continue
    status = record[:2].decode("ascii", "replace")
    name = record[3:].decode("utf-8", "surrogateescape")
    # For rename/copy records, porcelain -z has a second NUL record containing the source.
    if "R" in status or "C" in status:
        i += 1
    if name == report_rel:
        continue
    if status == "??":
        untracked_count += 1
    else:
        working_tree_count += 1

# Paths are repository-relative and intentionally include both governance records and
# source-evidence examples from the repository evidence criteria/intake. This is an
# inventory, not a claim that these paths exhaust all production requirements.
governance_docs = [
    "production/quality/production_readiness_matrix.md",
    "production/quality/repository_evidence_criteria.md",
    "production/quality/asset_acceptance_criteria.md",
    "production/quality/asset_acceptance_specification.md",
    "production/quality/change_request_process.md",
    "production/quality/final_render_verification_rules.md",
    "production/quality/final_verification_checklist.md",
    "production/quality/script_approval_record.json",
    "production/quality/asset_acceptance_checks.json",
    "production/quality/change_request_log.json",
    "production/quality/final_acceptance_record.json",
    "production/quality/shot_review_record.json",
    "production/quality/render_acceptance_record.json",
    "production/quality/audio_acceptance_record.json",
    "production/quality/licensing_audit.json",
    "production/quality/archive_manifest.json",
    "production/quality/release_readiness_report.json",
    "production/quality/repository_state_audit.sh",
    "production/quality/change_request.template.json",
    "production/quality/governance_artifact_roadmap.md",
    "production/quality/cross_document_consistency_review.md",
    "production/quality/final_render_verification.md",
    "config/schemas/holos-script-approval-record-v1.schema.json",
    "config/schemas/holos-change-request-v1.schema.json",
    "config/schemas/holos-asset-acceptance-checks-v1.schema.json",
    "docs/episode1-production-asset-intake.md",
    "docs/episode1-shared-audio-clock-integration.md",
]
source_evidence = [
    "production/screenplay/episode_01_screenplay_v1.md",
    "production/audio/episode_01_approved_script.json",
    "production/audio/episode_01_four_turn_v1.wav",
    "production/audio/episode_01_wav_format_validation.json",
    "production/audio/episode_01_whisperx_validation.json",
    "production/audio/episode_01_acoustic_word_timeline.json",
    "production/audio/episode_01_acoustic_phoneme_timeline.json",
    "production/audio/episode_01_audio_acceptance_report.json",
    "production/animation/episode_01_acoustic_viseme_timeline.json",
    "production/render/final/holos_episode_01_complete.mp4",
    "handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json",
    "handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json",
    "handoffs/milestone-5-1-2026-11-15/HOLOS_Episode1_four_turn_review_manifest.json",
]

def inspect(rel):
    p = root / rel
    try:
        st = p.lstat()
    except FileNotFoundError:
        return {"path": rel, "status": "MISSING", "sha256": None, "size_bytes": None}
    if p.is_symlink():
        return {"path": rel, "status": "SYMLINK", "sha256": None, "size_bytes": None}
    if not p.is_file():
        return {"path": rel, "status": "MISSING", "sha256": None, "size_bytes": None}
    # Inspect actual worktree bytes. Git LFS pointer text is metadata, not media bytes.
    with p.open("rb") as f:
        head = f.read(4096)
    if head.startswith(b"version https://git-lfs.github.com/spec/v1\n"):
        return {"path": rel, "status": "LFS_POINTER_ONLY", "sha256": None, "size_bytes": None,
                "note": "Git LFS pointer text only; payload not verified or labeled as downloaded media."}
    h = hashlib.sha256()
    size = 0
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return {"path": rel, "status": "PRESENT", "sha256": h.hexdigest(), "size_bytes": size}

payload = {
    "record_type": "REPOSITORY_STATE_AUDIT",
    "audit_classification": "INFORMATIONAL",
    "completion_claim_authorized": False,
    "repository": {
        "root": str(root),
        "branch": branch or "DETACHED_HEAD",
        "commit": commit,
        "working_tree_changed_path_count_excluding_report": working_tree_count,
        "untracked_path_count_excluding_report": untracked_count,
        "excluded_from_counts_and_hashing": [report_rel],
    },
    "governance_document_inventory": [inspect(p) for p in governance_docs],
    "expected_source_evidence_inventory": [inspect(p) for p in source_evidence],
    "evidence_boundary": (
        "This audit reports repository metadata and inspected working-tree bytes only. "
        "PRESENT means bytes exist at this path, not that they are authoritative, valid, approved, "
        "integrated, reviewed, or production-ready. LFS_POINTER_ONLY identifies pointer text only; "
        "it is never treated as downloaded media. A missing path means absent from this checkout, "
        "not necessarily absent elsewhere. This audit does not authorize or establish completion."
    ),
}
# Encode all data through Python's JSON serializer; write atomically to avoid partial reports.
report.parent.mkdir(parents=True, exist_ok=True)
tmp = report.with_name(report.name + ".tmp")
with tmp.open("w", encoding="utf-8", newline="\n") as f:
    json.dump(payload, f, ensure_ascii=True, indent=2, sort_keys=True)
    f.write("\n")
os.replace(tmp, report)
PY
