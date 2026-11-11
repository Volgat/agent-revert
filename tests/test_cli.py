"""CLI tests for the default path: snapshot / revert / patch.

All calls run without the store override flag, with HOME isolated,
so this suite proves what a fresh user gets out of the box:
the default store lives under HOME and never inside the project.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _env(home):
    env = dict(os.environ)
    env["HOME"] = str(home)
    old = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(REPO_ROOT) + (os.pathsep + old if old else "")
    return env


def _run(home, proj, *args):
    return subprocess.run(
        [sys.executable, "-m", "agent_revert", "--path", str(proj), *args],
        cwd=str(proj), env=_env(home), capture_output=True, text=True,
    )


def _project(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    return proj, home


def test_cli_snapshot_default_store_outside_tree(tmp_path):
    proj, home = _project(tmp_path)
    (proj / "app.py").write_text("hello\n")
    r = _run(home, proj, "snapshot")
    assert r.returncode == 0, r.stderr + r.stdout
    stored = [p for p in home.rglob("*") if p.is_file()]
    assert len(stored) >= 1
    assert not (proj / ".agent-revert").exists()
    assert (proj / "app.py").read_text() == "hello\n"


def test_cli_revert_restores_via_default_store(tmp_path):
    proj, home = _project(tmp_path)
    (proj / "app.py").write_text("v1\n")
    assert _run(home, proj, "snapshot").returncode == 0
    (proj / "app.py").write_text("v2\n")
    r = _run(home, proj, "revert")
    assert r.returncode == 0, r.stderr + r.stdout
    assert (proj / "app.py").read_text() == "v1\n"


def test_cli_patch_exports_diff_via_default_store(tmp_path):
    proj, home = _project(tmp_path)
    (proj / "app.py").write_text("line1\n")
    assert _run(home, proj, "snapshot").returncode == 0
    (proj / "app.py").write_text("line1\nline2\n")
    r = _run(home, proj, "patch")
    assert r.returncode == 0, r.stderr + r.stdout
    assert "app.py" in r.stdout
    assert "line2" in r.stdout
    assert "+" in r.stdout

