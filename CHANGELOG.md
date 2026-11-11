# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `--version` flag on the CLI: `agent-revert --version` prints `agent-revert X.Y.Z` and exits (was: no version info without `pip show`).

### Fixed

- Revert now restores file permission bits (e.g. executable `0755`) recorded at snapshot time; old snapshots stay compatible.
- `export-patch` is binary-safe: binary/large files emit `Binary files a/... and b/... differ` instead of mojibake.
- `__version__` synchronised to `0.2.0` with `pyproject.toml`.

## [0.2.0] - 2026-11-11

### Added

- Out-of-tree default store (no `.agent-revert` directory inside the working
  tree by default) with bounded retention (5 snapshots, evict oldest).
- End-to-end CLI tests: `tests/test_cli.py`, `tests/test_cli_default.py`
  (installed entry point, default store snapshot/revert without `--store`).

### Fixed

- `export-patch` now emits a real unified diff for deleted/added files
  (was truncated for additions).

## [Unreleased] — retention

### Added

- `--max-snapshots N` CLI flag: configure the retention limit without writing
  Python (`--max-snapshots 0` disables pruning). Previously hard-coded to 5.
- `pin <ID>` / `unpin <ID>` CLI commands and `Store.pin()` / `Store.unpin()`:
  pinned snapshots are never dropped by retention pruning, so a "known good"
  state survives unbounded agent runs.
- `timeline` now marks pinned snapshots.
- `snapshot` prints which snapshots (if any) were pruned by the retention
  limit — pruning is no longer silent (`Store.last_pruned` exposes the ids).

## [0.1.0] - 2026-11-11

### Added

- First public release.
- `agent-revert snapshot` / `timeline` / `status` / `revert` / `patch` CLI
  (Python stdlib only, ≥ 3.10).
- Content-addressed snapshot store (sha256 blobs + JSON manifests).
- `revert --dry-run`, `--path` / `--store` options, default ignore list.
- pytest suite (`tests/test_store.py`) and reproducible 60-second demo
  (`examples/demo.sh`).
- GitHub Actions CI, MIT license, contributing/security/code-of-conduct docs.

### Roadmap (not yet implemented)

- Git integration (commit-aware snaps), watch mode, IDE extension,
  large/binary file handling, Windows CI matrix.

### Added (Unreleased)
- Per-OS professional installers: `scripts/install.sh` (macOS/Linux/Git Bash, pipx > venv, `--venv`/`--no-pipx`/`--help`, exit codes 0/1) and `scripts/install.ps1` (Windows PowerShell, `-VenvDir`/`-Help`, exit codes 0/1), both verifying Python ≥ 3.10 with OS-specific guidance.
- Cross-platform CI matrix: Ubuntu / macOS / Windows × Python 3.10 / 3.12, including an installer-script parse/help check on each OS.
- `pyproject.toml`: OS classifiers (macOS / Windows / POSIX Linux) and project URLs.
