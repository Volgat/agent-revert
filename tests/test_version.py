"""--version flag tests."""
import subprocess
import sys

import pytest

from agent_revert import __version__
from agent_revert.cli import build_parser


def test_version_flag_prints_package_version(capsys):
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_version_via_module_entrypoint():
    r = subprocess.run(
        [sys.executable, "-m", "agent_revert", "--version"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == f"agent-revert {__version__}"
