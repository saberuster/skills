FROM node:24-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    FERN_VALIDATION_CONTAINER=1 \
    PATH=/opt/fern-python/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 python3-venv git ripgrep ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/fern-python \
    && npm install --global @openai/codex@0.161.0 skills@1.7.0 \
    && groupadd --gid 1001 fern-worker \
    && useradd --uid 1001 --gid 1001 --create-home fern-worker \
    && groupadd --gid 1002 fern-evaluator \
    && useradd --uid 1002 --gid 1002 --create-home fern-evaluator

WORKDIR /source
COPY . /source/
RUN python -m pip install --no-cache-dir -r requirements-dev.txt tomlkit==0.13.3 \
    && npm ci \
    && git init --quiet \
    && git add . \
    && chmod -R go-rwx /source \
    && mkdir /evidence

CMD ["python", "scripts/fern_ci.py", "--suite", "checks", "--output", "/evidence"]
