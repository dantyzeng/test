#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HABITAT_MAGS_ROOT:-}" ]]; then
  echo "Set HABITAT_MAGS_ROOT to the complete local habitat_MAGs project directory" >&2
  exit 2
fi
python3 "$SCRIPT_DIR/build_project_summary.py"
