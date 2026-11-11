from pathlib import Path
from agent_revert.store import default_store_path, Store

def test_default_store_is_outside_tree(tmp_path):
    proj = tmp_path / "proj"; proj.mkdir()
    store_path = default_store_path(proj)
    assert store_path == Path.home() / ".agent-revert" / store_path.name, store_path
    assert store_path.name.startswith("proj-"), store_path.name
    assert not str(store_path.resolve()).startswith(str(proj.resolve()))
    # stable per project, different across projects
    assert default_store_path(proj) == store_path
    other = tmp_path / "other"; other.mkdir()
    assert default_store_path(other) != store_path

def test_snapshot_does_not_pollute_tree(tmp_path):
    proj = tmp_path / "proj"; proj.mkdir()
    (proj / "app.py").write_text("x=1\n")
    store = Store(default_store_path(proj), max_snapshots=5)
    store.snapshot(proj)
    left = sorted(p.name for p in proj.iterdir())
    assert left == ["app.py"], left
    assert (proj / ".agent-revert").exists() is False
