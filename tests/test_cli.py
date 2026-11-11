"""CLI tests for the default path: snapshot / revert / patch.

All calls run without the store override flag, with HOME isolated,
so this suite proves what a fresh user gets out of the box:
the default store lives under HOME and never inside the project.
"""
import os
import subprocess
import sys
from pathlib import Path

from agent_revert.cli import main

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





def test_cli_max_snapshots_flag(tmp_path, capsys):
    root, _home = _project(tmp_path)
    store = str(tmp_path / "store")
    base = ["--path", str(root), "--store", store, "--max-snapshots", "2"]

    for i in range(3):
        (root / "app.py").write_text(f"v{i}\n")
        assert main(base + ["snapshot", "--label", f"s{i}"]) == 0
    out = capsys.readouterr().out
    assert "pruned:" in out, out  # oldest snapshot was dropped, and we say so

    assert main(["--path", str(root), "--store", store, "timeline"]) == 0
    out = capsys.readouterr().out
    assert "s2" in out and "s0" not in out


def test_cli_pin_unpin(tmp_path, capsys):
    root, _home = _project(tmp_path)
    store = str(tmp_path / "store")
    base = ["--path", str(root), "--store", store]

    assert main(base + ["snapshot", "--label", "known good"]) == 0
    out = capsys.readouterr().out
    snap_id = out.split()[1]

    assert main(base + ["pin", snap_id]) == 0
    out = capsys.readouterr().out
    assert "pinned" in out

    assert main(base + ["timeline"]) == 0
    assert "[pinned]" in capsys.readouterr().out

    # retention of 1 would drop anything unpinned; pinned survives
    (root / "app.py").write_text("v1\n")
    assert main(base + ["--max-snapshots", "1", "snapshot", "--label", "b"]) == 0
    assert main(["--path", str(root), "--store", store, "timeline"]) == 0
    out = capsys.readouterr().out
    assert "known good" in out and "[pinned]" in out

    assert main(base + ["unpin", snap_id]) == 0
    assert "unpinned" in capsys.readouterr().out


def test_cli_pin_unknown_snapshot(tmp_path, capsys):
    root, _home = _project(tmp_path)
    store = str(tmp_path / "store")
    base = ["--path", str(root), "--store", store]
    assert main(base + ["snapshot"]) == 0
    capsys.readouterr()
    assert main(base + ["pin", "deadbeef"]) == 1  # KeyError -> clean error, exit 1
