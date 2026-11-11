"""End-to-end CLI tests for agent-revert."""
from pathlib import Path

from agent_revert.cli import main


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "app.py").write_text("print('hello')\n")
    (root / "util.py").write_text("x = 1\n")
    return root


def test_cli_full_cycle(tmp_path, capsys):
    root = _project(tmp_path)
    store = str(tmp_path / "store")
    base = ["--path", str(root), "--store", store]

    assert main(base + ["snapshot", "--label", "before agent"]) == 0
    out = capsys.readouterr().out
    assert "snapshot" in out and "files=2" in out

    # agent breaks things
    (root / "app.py").write_text("BROKEN\n")
    (root / "util.py").unlink()
    (root / "junk.txt").write_text("junk\n")

    assert main(base + ["status"]) == 0
    out = capsys.readouterr().out
    assert "added:" in out and "modified:" in out and "deleted:" in out

    assert main(base + ["revert", "--dry-run"]) == 0
    assert (root / "junk.txt").exists()  # dry-run changes nothing

    assert main(base + ["revert"]) == 0
    assert (root / "app.py").read_text() == "print('hello')\n"
    assert (root / "util.py").read_text() == "x = 1\n"
    assert not (root / "junk.txt").exists()

    assert main(base + ["timeline"]) == 0
    out = capsys.readouterr().out
    assert "before agent" in out


def test_cli_no_snapshots(tmp_path):
    root = _project(tmp_path)
    store = str(tmp_path / "store")
    assert main(["--path", str(root), "--store", store, "timeline"]) == 0
    assert main(["--path", str(root), "--store", store, "status"]) == 1


def test_cli_patch(tmp_path, capsys):
    root = _project(tmp_path)
    store = str(tmp_path / "store")
    base = ["--path", str(root), "--store", store]
    assert main(base + ["snapshot"]) == 0
    (root / "app.py").write_text("changed\n")
    assert main(base + ["patch"]) == 0
    out = capsys.readouterr().out
    assert "a/app.py" in out and "changed" in out
