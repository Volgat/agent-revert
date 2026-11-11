# Contributing to agent-revert

Thanks for your interest! `agent-revert` is a small, stdlib-only Python CLI.
The bar for a change: it must keep the tool dependency-free and work on
Python ≥ 3.10.

## Workflow

1. Open an issue first for anything non-trivial (bug, feature, design question).
2. Fork the repo, create a branch: `feat/<short-name>` or `fix/<short-name>`.
3. Make your change, add or update tests in `tests/`.
4. Run the checks locally:

   ```bash
   python3 -m pytest -q
   bash examples/demo.sh
   ```

5. Open a pull request against `main`, describing what and why. Link the issue
   with `Closes #<n>`.

## Code style

- Python ≥ 3.10, type hints where they help readability.
- Standard library first — new dependencies need a strong justification
  (default answer: no).
- Small, focused PRs. One issue per PR when possible.
- Docstrings for public functions; keep README in sync for user-facing changes.

## Testing

- `tests/test_store.py` covers snapshot / diff / revert / dedup / patch.
- New behavior needs a test. Tests must be hermetic (use `tmp_path`).
- CI runs on `main` and on every PR (`.github/workflows/ci.yml`).

## Releases

Maintainer-only. Bump `agent_revert/__init__.py` + `pyproject.toml`, add a
`CHANGELOG.md` entry, tag `vX.Y.Z`.
