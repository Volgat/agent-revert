# agent-revert

**Undo any AI coding agent in one command.**

[![CI](https://github.com/kaia-cod/agent-revert/actions/workflows/ci.yml/badge.svg)](https://github.com/kaia-cod/agent-revert/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![OS macOS | Linux | Windows](https://img.shields.io/badge/OS-macOS%20%7C%20Linux%20%7C%20Windows-informational)](scripts/install.sh)
[![Stars](https://img.shields.io/github/stars/kaia-cod/agent-revert?style=social)](https://github.com/kaia-cod/agent-revert/stargazers)

> Your AI coding agent just rewrote your codebase. Git can't help you — those
> files were never committed. `agent-revert` snapshots your working tree
> before the agent runs and restores it in one command.


## 🚀 Launch status — 30-day open-source project

Bounded 30-day autonomous open-source sprint under **@kaia-cod** — no third-party
accounts, no user solicitation. What was provable with owned accounts is shipped here.

- **Repository:** https://github.com/kaia-cod/agent-revert
- **Releases:** https://github.com/kaia-cod/agent-revert/releases
- **Project board (issues):** https://github.com/kaia-cod/agent-revert/issues
  Board columns are tracked as labelled issues: `[BACKLOG]`, `[IN PROGRESS]`,
  `[REVIEW]`, `[DONE]`, `[ROADMAP]` (equivalent of a Projects board via API).
- **Audit:** [`AUDIT.md`](AUDIT.md) — bounded audit of the local repo and the
  @kaia-cod account, including what was honestly abandoned (Show HN, Product Hunt,
  10 000 stars, HF Space) and why.

Status: `snapshot` / `revert` / `timeline` / `status` / `patch` implemented and
tested (stdlib only, Python ≥ 3.10). See [CHANGELOG.md](CHANGELOG.md) for details.

## Why this exists

Claude Code, Codex, Cursor and friends edit files directly, often without any
commit. When the result is broken, you have no clean way back:

- `git checkout` / `git stash` only cover **committed** (or fully untracked) work
- Most agents run in the same directory you work in, so damage is immediate
- There is no single "undo everything the agent just did" button

`agent-revert` fills exactly that gap: a content-addressed snapshot of your
tree, taken in milliseconds, with `revert`, `timeline`, `status` and `patch`
on top. Zero dependencies, works with or without git, no API key.

## Installation (macOS · Linux · Windows)

**Prerequisite — every OS:** Python **≥ 3.10** (`python3 --version` / `py --version` / `python --version`).
Stdlib only — no other runtime dependency.

### 🍎 macOS / 🐧 Linux

```bash
# Recommended: isolated CLI app with pipx (keeps your system Python clean)
pipx install 'agent-revert @ git+https://github.com/kaia-cod/agent-revert'   # latest from git (PyPI lags: 0.1.5 vs 0.2.0)

# Alternative: one-command installer script (pipx if present, else a venv in ~/.local)
curl -fsSL https://raw.githubusercontent.com/kaia-cod/agent-revert/main/scripts/install.sh | bash
# or, from a local checkout:
bash scripts/install.sh           # options: --help, --venv DIR, --no-pipx

# Manual / any environment:
pip install 'agent-revert @ git+https://github.com/kaia-cod/agent-revert'   # or: pip install -e .  from a checkout
```

### 🪟 Windows (PowerShell)

```powershell
# Recommended: isolated CLI app with pipx
pipx install 'agent-revert @ git+https://github.com/kaia-cod/agent-revert'

# Alternative: one-command installer script (creates %LOCALAPPDATA%\agent-revert\venv)
powershell -ExecutionPolicy Bypass -File scripts/install.ps1      # -VenvDir <dir> to customise
# or one-liner:
irm https://raw.githubusercontent.com/kaia-cod/agent-revert/main/scripts/install.ps1 | iex

# Manual / any environment:
py -m pip install 'agent-revert @ git+https://github.com/kaia-cod/agent-revert'   # or: python -m pip install -e .  from a checkout
```

> **Installer exit codes (both scripts):** `0` = success, `1` = Python ≥ 3.10 missing / install failure. Run `bash scripts/install.sh --help` (or `install.ps1 -Help`) for options.

> **Verify:** `agent-revert --help` prints the usage. If the command is not found,
> restart your terminal (PATH) or run `python -m agent_revert --help` /
> `py -m agent_revert --help`. The default snapshot store lives outside your
> tree at `~/.agent-revert/<project>-<hash>` (macOS/Linux) or
> `%USERPROFILE%\.agent-revert\<project>-<hash>` (Windows).

## Quick start

```bash
cd your-project

# 1. snapshot BEFORE the agent runs
agent-revert snapshot --label "before refactor"

# 2. let the agent do its thing... it breaks 3 files

# 3. preview the undo (changes nothing)
agent-revert revert --dry-run

# 4. undo it, for real
agent-revert revert
```

See the full reproducible demo: [`examples/demo.sh`](examples/demo.sh)
(`bash examples/demo.sh` — under 60 seconds, no network, no API key).

## Usage

```
agent-revert [--path DIR] [--store DIR] <command>

snapshot [--label TEXT]        take a snapshot of DIR
timeline                       list all snapshots
status [--json]                what changed since the latest snapshot?
revert [--snapshot ID] [--dry-run]
                               restore DIR to a snapshot (default: latest)
patch [--snapshot ID]          export a unified diff vs a snapshot
```

- `--path` defaults to the current directory.
- `--store` defaults to `~/.agent-revert/<project>-<hash8>` (outside the
  tracked tree, on every OS; `%USERPROFILE%\.agent-revert\...` on Windows).
  Pass `--store DIR` to override, e.g. `--store ~/.agent-revert/myproject`.
  The store is content-addressed (`blobs/<sha256>` + `snapshots/<id>.json`),
  so unchanged files cost nothing across snapshots.
- Ignored by default: `.git`, `__pycache__`, `.venv`, `venv`, `.mypy_cache`,
  `.pytest_cache`, `node_modules`.

### Example

```text
$ agent-revert snapshot --label "before agent"
snapshot 3f9a1c2b4d5e  files=128  label='before agent'

$ agent-revert status
snapshot: 3f9a1c2b4d5e (before agent)
added:    2
  + junk.txt
  + src/generated.py
modified: 3
  ~ app.py
  ~ config.yaml
  ~ src/util.py
deleted:  1
  - src/legacy.py

$ agent-revert revert --dry-run
would revert to snapshot 3f9a1c2b4d5e: 2 to remove, 3 to restore, 1 to recreate

$ agent-revert revert
reverted to snapshot 3f9a1c2b4d5e: 2 to remove, 3 to restore, 1 to recreate
```

## Architecture

```
agent_revert/
  __init__.py     version
  store.py        Store: snapshot / list / get / latest / diff / revert / export_patch
  cli.py          argparse CLI (snapshot, timeline, status, revert, patch)
  __main__.py     python -m agent_revert entry point
tests/
  test_store.py   pytest: snapshot→break→dry-run→revert, dedup, empty tree, patch
examples/
  demo.sh         60-second reproducible demo
```

Design principles:

1. **Stdlib only** — runs anywhere Python ≥ 3.10 runs. No install friction.
2. **Content-addressed** — one blob per unique file content (`sha256`), so
   repeated snapshots are cheap and deduplicated.
3. **Git-agnostic** — works on any directory; git integration is a roadmap
   item, never a requirement.
4. **Safe by default** — `revert --dry-run` previews exactly what will change;
   symlinks/devices/sockets are never followed or tracked.

## Why not ... ?

| Alternative | What it does | Gap vs agent-revert |
|---|---|---|
| `git checkout` / `git stash` | restores committed work | misses uncommitted files — exactly what agents produce |
| LangGraph / Langfuse / Phoenix | agent tracing & time-travel | replays *conversations*, doesn't restore your *filesystem* |
| OrcaReplay | record/replay/fork agent runs | re-executes the agent; slower, model-dependent |
| vibe-revert | TS-based agent undo | different stack, tiny community |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: Python ≥ 3.10, stdlib-first,
`python3 -m pytest`, open an issue or a PR.

## Code of conduct / security

- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md) — please do **not** open public issues for vulnerabilities.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Roadmap

Tracked as GitHub issues (see the `Roadmap` column of the project board):
git integration, binary/large-file handling, watch mode, IDE extension.
Cross-platform CI (Ubuntu / macOS / Windows × Python 3.10 / 3.12) and
per-OS installers (`scripts/install.sh`, `scripts/install.ps1`) are shipped.


## Discoverability

Forgettable? No: `agent-revert` is deliberately boring — stdlib only,
zero config, one command. It works precisely because AI coding agents
keep getting better at *changing* files while undo stays manual.
That gap — undo for any agent, with or without git — is the whole
point of this project.

## License

[MIT](LICENSE) © 2026 kaia-cod contributors.
