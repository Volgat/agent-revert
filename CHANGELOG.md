# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
