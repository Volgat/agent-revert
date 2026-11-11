# agent-revert — container image published to GitHub Container Registry (GHCR).
#
# Repository: https://github.com/kaia-cod/agent-revert
#
# The org.opencontainers.image.source label below is what makes GitHub link
# this image to the repository: it shows up under "Packages" in the repo
# sidebar as a *container* package (ghcr.io/kaia-cod/agent-revert).
# Python wheels/sdists are not a GitHub Packages registry type, so the
# container is the publishable form of this project.
#
# Usage:
#   docker run --rm -v "$PWD:/work" ghcr.io/kaia-cod/agent-revert snapshot --label "before agent"
#   docker run --rm -v "$PWD:/work" ghcr.io/kaia-cod/agent-revert revert --dry-run

FROM python:3.12-slim

# OCI image labels — org.opencontainers.image.source links the image to
# https://github.com/kaia-cod/agent-revert (Packages sidebar).
LABEL org.opencontainers.image.title="agent-revert" \
      org.opencontainers.image.description="Undo any AI coding agent in one command — snapshot / revert / timeline / diff for your working tree" \
      org.opencontainers.image.url="https://github.com/kaia-cod/agent-revert" \
      org.opencontainers.image.source="https://github.com/kaia-cod/agent-revert" \
      org.opencontainers.image.documentation="https://github.com/kaia-cod/agent-revert#readme" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.vendor="kaia-cod"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Build from source (pyproject.toml), not from dist/: dist/ is gitignored,
# so only the source tree is available in CI.
COPY pyproject.toml README.md ./
COPY agent_revert ./agent_revert

RUN pip install --no-cache-dir . \
    && agent-revert --help > /dev/null \
    && useradd --create-home --uid 10001 app \
    && mkdir -p /data /work \
    && chown -R app:app /data /work

USER app

# agent-revert stores snapshots outside the target tree at
# ~/.agent-revert/<project>-<hash>; point HOME at a writable, mountable dir.
ENV HOME=/data

# The project directory to snapshot/revert. Mount your project here:
#   docker run --rm -v "$PWD:/work" ghcr.io/kaia-cod/agent-revert ...
WORKDIR /work

ENTRYPOINT ["agent-revert"]
CMD ["--help"]
