"""CLI default-path test via the INSTALLED entry point.

Gap covered here (test_cli.py uses ``python -m agent_revert`` instead):
a fresh user types ``agent-revert snapshot`` / ``agent-revert revert``
with NO ``--store`` flag. This test proves that exact path end to end:

  * the console script ``agent-revert`` exists (``pip install .``),
  * the store is created under ``$HOME/.agent-revert/<project>-<hash8>``,
  * the project tree stays clean (no ``.agent-revert`` inside it),
  * ``revert`` restores the file byte-for-byte.

The entry point is resolved from ``$AGENT_REVERT_BIN`` or PATH, falling
back to a ``pip install --target`` into an isolated dir (works inside
PEP 668 externally-managed environments where ``pip install -e .``
refuses the system site-packages). HOME is isolated to ``tmp_path`` so
the real ``~/.agent-revert`` is untouched.
"""
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _entry_point() -> str:
    exe = os.environ.get("AGENT_REVERT_BIN") or shutil.which("agent-revert")
    if exe:
        return exe
    # Fallback for PEP 668 hosts: build an isolated install on the fly.
    target = Path(os.environ.get("TMPDIR", "/tmp")) / "agent-revert-target"
    if not (target / "bin" / "agent-revert").exists():
        subprocess.run(
            [sys.executable, "-m", "pip", "install", ".", "--target", str(target),
             "--quiet", "--disable-pip-version-check"],
            check=True, capture_output=True, text=True,
        )
    exe = target / "bin" / "agent-revert"
    assert exe.exists(), (
        f"entry point 'agent-revert' not found (PATH, $AGENT_REVERT_BIN, "
        f"or isolated install at {exe}) — run: pip install -e ."
    )
    return str(exe)


def _expected_store(home: Path, proj: Path) -> Path:
    digest = hashlib.sha256(str(proj.resolve()).encode("utf-8")).hexdigest()[:8]
    return home / ".agent-revert" / f"{proj.name}-{digest}"


def test_installed_entrypoint_default_store_snapshot_revert(tmp_path):
    exe = _entry_point()
    proj = tmp_path / "myproj"
    proj.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    original = "v1\n"
    (proj / "app.py").write_text(original)

    env = dict(os.environ)
    env["HOME"] = str(home)
    # pip --target installs are not on sys.path by default; the console
    # script needs its install root to import the package.
    old_pp = env.get("PYTHONPATH", "")
    if str(Path(exe).parent.parent) not in old_pp:
        env["PYTHONPATH"] = str(Path(exe).parent.parent) + (
            os.pathsep + old_pp if old_pp else ""
        )

    # 1. snapshot WITHOUT --store, run from inside the project.
    r = subprocess.run(
        [exe, "--path", str(proj), "snapshot"],
        cwd=str(proj), env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout

    # 2. store created at the documented default location; tree untouched.
    store = _expected_store(home, proj)
    assert store.is_dir(), f"default store missing: {store}"
    assert (store / "snapshots").is_dir()
    assert (store / "blobs").is_dir()
    assert list((store / "snapshots").glob("*.json")), (
        "no snapshot manifest in default store"
    )
    assert not (proj / ".agent-revert").exists(), "store polluted the project tree"
    assert sorted(p.name for p in proj.iterdir()) == ["app.py"]

    # 3. the agent breaks the file, then revert WITHOUT --store restores it.
    (proj / "app.py").write_text("v2 broken by agent\n")
    r = subprocess.run(
        [exe, "--path", str(proj), "revert"],
        cwd=str(proj), env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert (proj / "app.py").read_text() == original
    assert not (proj / ".agent-revert").exists()
