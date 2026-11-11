#!/usr/bin/env bash
# agent-revert 60-second demo — reproducible, no API key needed.
# Usage: bash examples/demo.sh
set -euo pipefail

# Resolve the package from this repo (works from a source checkout,
# with or without `pip install .`). Capture the repo path BEFORE any
# `cd` so the relative script path still resolves.
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

DEMO_DIR="$(mktemp -d)"
STORE_DIR="$(mktemp -d)"
trap 'rm -rf "$DEMO_DIR" "$STORE_DIR"' EXIT

# 1. A healthy project
mkdir -p "$DEMO_DIR/src"
printf "print('hello')\n" > "$DEMO_DIR/app.py"
printf "# demo\n" > "$DEMO_DIR/README.md"
printf "x = 1\n" > "$DEMO_DIR/src/util.py"
cd "$DEMO_DIR"

# python3 on macOS/Linux; plain `python` on Windows (Git Bash) and venvs.
# Override with PYTHON_BIN=/path/to/python bash examples/demo.sh
PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN=python
  else
    echo "error: no python3/python in PATH (agent-revert needs Python >= 3.10)" >&2
    exit 1
  fi
fi

RUN="$PYTHON_BIN -m agent_revert --path $DEMO_DIR --store $STORE_DIR"

echo "== 1. snapshot (before the agent runs) =="
$RUN snapshot --label "before agent"

echo "== 2. the AI coding agent breaks 3 files =="
printf "print('BROKEN')\n" > app.py
rm src/util.py
printf "junk\n" > junk.txt
$RUN status

echo "== 3. dry-run revert (nothing changes yet) =="
$RUN revert --dry-run
test -f junk.txt && echo "junk.txt still there (dry-run OK)"

echo "== 4. revert for real =="
$RUN revert
echo "--- restored files ---"
cat app.py
cat src/util.py
test ! -f junk.txt && echo "junk.txt removed — undo complete"
echo "DEMO OK"
