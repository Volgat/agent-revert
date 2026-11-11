"""S21: permission bits and binary-safe patch export."""
from pathlib import Path
from agent_revert.store import Store


def test_revert_restores_executable_bit(tmp_path):
    proj = tmp_path / "p"
    proj.mkdir()
    f = proj / "run.sh"
    f.write_text("echo ok\n")
    f.chmod(0o755)
    st = Store(tmp_path / "store")
    snap = st.snapshot(proj, label="t")
    assert snap["modes"]["run.sh"] == 0o755
    f.write_text("echo broken\n")
    f.chmod(0o644)
    st.revert(snap, proj)
    assert (proj / "run.sh").read_text() == "echo ok\n"
    assert int((proj / "run.sh").stat().st_mode & 0o777) == 0o755


def test_patch_binary_safe(tmp_path):
    proj = tmp_path / "p"
    proj.mkdir()
    (proj / "data.bin").write_bytes(b"\x00\x01\x02hello")
    st = Store(tmp_path / "store")
    snap = st.snapshot(proj)
    (proj / "data.bin").write_bytes(b"\x00\xff\xfechanged")
    patch = st.export_patch(snap, proj)
    assert "Binary files a/data.bin and b/data.bin differ" in patch
    assert "\x00" not in patch
