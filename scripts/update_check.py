#!/usr/bin/env python3
"""Vérifie les nouvelles versions de kaia-cod/agent-revert et synchronise le clone local.
Usage: python3 scripts/update_check.py [--force] [--no-fetch]
- Query GitHub API releases + HEAD remote (sans token, public).
- Compare avec version locale (pyproject.toml) et commit local.
- Si nouveau: git fetch --ff-only (ou clone frais), reinstall editable, log dans suivi-agent-revert.md
- Idempotent, stdlib only.
"""
import argparse, json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]
REPO = "kaia-cod/agent-revert"
API = f"https://api.github.com/repos/{REPO}"

def _git(*args):
    return subprocess.run(["git", "-C", str(REPO_DIR), *args], capture_output=True, text=True, timeout=60)

def local_version():
    m = re.search(r'^version\s*=\s*"([^"]+)"', (REPO_DIR/"pyproject.toml").read_text(), re.M)
    return m.group(1) if m else "?"

def log(msg):
    p = REPO_DIR/"suivi-agent-revert.md"
    p.write_text(p.read_text() + f"\n## {datetime.now(timezone.utc).isoformat()}\n- {msg}\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()
    print(f"local: version={local_version()} head={_git('rev-parse','--short','HEAD').stdout.strip()}")
    req = urllib.request.Request(API+"/releases", headers={"User-Agent":"agent-revert-updater"})
    try:
        releases = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        print(f"API releases KO: {e}"); return 1
    tags = [(r["tag_name"], r.get("published_at")) for r in releases]
    print(f"remote releases: {tags[:5]}")
    if not a.no_fetch:
        r = _git("fetch", "origin", "main")
        print("fetch:", r.stderr.strip() or "ok")
        head, remote = _git("rev-parse","HEAD").stdout.strip(), _git("rev-parse","origin/main").stdout.strip()
        if head != remote:
            r = _git("merge","--ff-only","origin/main")
            print("ff-only:", r.stdout.strip() or r.stderr.strip())
            subprocess.run([sys.executable,"-m","pip","install","-e",".","--quiet"], cwd=REPO_DIR, capture_output=True)
            log(f"sync auto: {head[:7]} -> {remote[:7]}, version {local_version()}")
        else:
            print("A jour: HEAD == origin/main")
    return 0

if __name__ == "__main__":
    sys.exit(main())
