#!/usr/bin/env bash
# agent-revert installer — macOS & Linux (bash/zsh) and Git Bash on Windows.
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/kaia-cod/agent-revert/main/scripts/install.sh | bash
#   # or local:
#   bash scripts/install.sh [--venv DIR] [--no-pipx] [--help]
# Options:
#   --venv DIR    Install into a Python venv at DIR (default: ~/.local/share/agent-revert/venv)
#   --no-pipx     Skip pipx even if present, use the venv fallback
#   --help, -h    Show this help and exit 0
# Exit codes: 0 = success, 1 = usage/python-not-found/install failure.
set -euo pipefail

usage() { sed -n '2,11p' "$0"; }

VENV_DIR=""
USE_PIPX=1
while [ $# -gt 0 ]; do
  case "$1" in
    --venv)
      [ $# -ge 2 ] || { echo "ERROR: --venv requires a DIR argument" >&2; usage >&2; exit 1; }
      VENV_DIR="$2"; shift 2 ;;
    --no-pipx) USE_PIPX=0; shift ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

echo "== agent-revert installer =="
echo "OS: $(uname -s 2>/dev/null || echo Windows/Git-Bash)"

# --- 1. Find Python 3.10+ (python3 on Unix, python or py on Windows) ---
PY=""
for cand in python3 python py; do
  if command -v "$cand" >/dev/null 2>&1; then
    ver="$("$cand" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo 0)"
    major="${ver%%.*}"; minor="${ver#*.}"
    if [ "${major:-0}" -ge 3 ] && [ "${minor:-0}" -ge 10 ]; then PY="$cand"; break; fi
  fi
done
if [ -z "$PY" ]; then
  echo "ERROR: Python >= 3.10 not found. Install it first:" >&2
  case "$(uname -s 2>/dev/null)" in
    Darwin) echo '  brew install python3' >&2 ;;
    Linux)  echo '  sudo apt install python3 python3-pip   # Debian/Ubuntu' >&2; echo '  sudo dnf install python3 pip             # Fedora/RHEL' >&2 ;;
    *)      echo '  Download from https://www.python.org/downloads/  (check "Add python to PATH")' >&2 ;;
  esac
  exit 1
fi
echo "Python: $("$PY" --version)  -> $("$PY" -c 'import sys; print(sys.executable)')"

# --- 2. Install method: pipx > venv ---
if [ "$USE_PIPX" = 1 ] && [ -z "$VENV_DIR" ] && command -v pipx >/dev/null 2>&1; then
  echo "Installing with pipx (isolated, recommended)..."
  pipx install --force agent-revert || pipx install --force 'agent-revert @ git+https://github.com/kaia-cod/agent-revert'
  echo "OK: installed via pipx"
  if command -v agent-revert >/dev/null 2>&1; then
    agent-revert --help >/dev/null && echo "Check OK: $(agent-revert --help 2>&1 | head -n1)"
  else
    echo "Note: agent-revert not on PATH yet — ensure ~/.local/bin is on PATH."
  fi
  exit 0
fi

# Fallback: Python venv (works on macOS, Linux, Windows Git Bash)
VENV_DIR="${VENV_DIR:-$HOME/.local/share/agent-revert/venv}"
echo "Installing into venv: $VENV_DIR"
"$PY" -m venv "$VENV_DIR" || { echo "ERROR: failed to create venv at $VENV_DIR" >&2; exit 1; }
if [ -f "$VENV_DIR/Scripts/activate" ]; then  # Windows venv layout
  VENV_PY="$VENV_DIR/Scripts/python.exe"; BIN="$VENV_DIR/Scripts"
else
  VENV_PY="$VENV_DIR/bin/python"; BIN="$VENV_DIR/bin"
fi
"$VENV_PY" -m pip install --quiet --upgrade pip || { echo "ERROR: pip upgrade failed" >&2; exit 1; }
# Prefer the published package; fall back to the git checkout for unreleased versions.
"$VENV_PY" -m pip install --quiet 'agent-revert @ git+https://github.com/kaia-cod/agent-revert' \
  || { echo "ERROR: pip install of agent-revert failed" >&2; exit 1; }
echo "OK: installed in venv. Launcher: $BIN/agent-revert"
"$BIN/agent-revert" --help >/dev/null 2>&1 && echo "Check OK: agent-revert --help works" || echo "Warning: launcher check failed — try: $BIN/agent-revert --help"
echo ""
echo "To use it everywhere, add to PATH (one-time):"
echo "  export PATH=\"$BIN:\$PATH\"    # bash/zsh (~/.bashrc or ~/.zshrc)"
echo "Or run full path: \"$BIN/agent-revert\" snapshot"
