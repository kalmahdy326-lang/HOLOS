#!/usr/bin/env bash
set -euo pipefail

REPO="${HOLOS_REPO:-kalmahdy326-lang/HOLOS}"
PR="${HOLOS_PR:-6}"
RUN_ID="${HOLOS_RUN_ID:-43695472809}"
HEAD_BRANCH="${HOLOS_HEAD_BRANCH:-docs/milestone-5-1-four-turn-acceptance}"
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: check_run_status.sh [--dry-run]

Read-only GitHub CLI diagnostics for a HOLOS PR and Actions run.
--dry-run  Validate configuration and print the planned checks without calling GitHub.
USAGE
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
elif [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
elif [[ -n "${1:-}" ]]; then
  usage >&2
  exit 2
fi

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

[[ -n "$REPO" && -n "$PR" && -n "$RUN_ID" && -n "$HEAD_BRANCH" ]] || fail 'Repository, PR, run and branch configuration must be non-empty.'

if (( DRY_RUN )); then
  cat <<PLAN
DRY RUN — no GitHub commands will be executed.
Repository: $REPO
PR:         $PR
Run ID:     $RUN_ID
Branch:     $HEAD_BRANCH
Planned read-only checks:
  1. gh auth status
  2. gh repo view $REPO
  3. gh pr view $PR --repo $REPO
  4. gh run view $RUN_ID --repo $REPO
  5. gh api repos/$REPO/actions/runs/$RUN_ID/jobs
  6. gh run view $RUN_ID --repo $REPO --log-failed
  7. gh run list --repo $REPO --branch $HEAD_BRANCH
PLAN
  exit 0
fi

command -v gh >/dev/null 2>&1 || fail 'GitHub CLI (gh) is not installed. Install it and authenticate the repository-access account.'

echo '== GitHub identity =='
gh auth status

echo
echo '== Repository visibility =='
gh repo view "$REPO" --json nameWithOwner,isPrivate,defaultBranchRef,url

echo
echo '== Pull request =='
gh pr view "$PR" --repo "$REPO" --json number,state,isDraft,baseRefName,headRefName,headRefOid,title,url

echo
echo '== Workflow run =='
gh run view "$RUN_ID" --repo "$REPO" \
  --json databaseId,number,status,conclusion,headSha,headBranch,workflowName,url,createdAt,updatedAt

echo
echo '== Jobs and steps =='
gh api "repos/$REPO/actions/runs/$RUN_ID/jobs?per_page=100" --paginate \
  --jq '.jobs[] | {
    id,
    name,
    status,
    conclusion,
    started_at,
    completed_at,
    steps: [.steps[]? | {
      name,
      status,
      conclusion,
      number
    }]
  }'

echo
echo '== Failed logs =='
# `--log-failed` can return no text when all jobs pass; do not turn that into a false diagnosis.
if ! gh run view "$RUN_ID" --repo "$REPO" --log-failed; then
  echo 'No failed-log output was returned; inspect the job conclusions above.'
fi

echo
echo '== Recent branch runs =='
gh run list --repo "$REPO" --branch "$HEAD_BRANCH" --limit 20 \
  --json databaseId,number,status,conclusion,headSha,workflowName,createdAt,url

echo
echo 'Read-only check complete. No login, push, rerun, commit or merge was performed.'
