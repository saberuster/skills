FROM node:24-bookworm-slim AS core

ENV DEBIAN_FRONTEND=noninteractive \
    FERN_VALIDATION_CONTAINER=1 \
    PATH=/opt/validation-python/bin:/opt/powershell:$PATH \
    PWSH=/opt/powershell/pwsh \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Official release assets; fixed digests verified against the publishers.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 python3-venv git ripgrep ca-certificates curl xz-utils \
       libicu72 libssl3 libgssapi-krb5-2 zlib1g \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /opt/powershell \
    && curl --fail --location --retry 3 \
       https://github.com/PowerShell/PowerShell/releases/download/v7.4.13/powershell-7.4.13-linux-x64.tar.gz \
       --output /tmp/powershell.tar.gz \
    && echo '59e5df675dacbfe45374c32c1bf2480168a33243423c9b19252d0476fd1b748c  /tmp/powershell.tar.gz' | sha256sum --check - \
    && tar -xzf /tmp/powershell.tar.gz -C /opt/powershell \
    && chmod +x /opt/powershell/pwsh \
    && rm /tmp/powershell.tar.gz \
    && python3 -m venv /opt/validation-python \
    && npm install --global @openai/codex@0.161.0 skills@1.7.0 \
    && groupadd --gid 1001 fern-worker \
    && useradd --uid 1001 --gid 1001 --create-home fern-worker \
    && groupadd --gid 1002 fern-evaluator \
    && useradd --uid 1002 --gid 1002 --create-home fern-evaluator

WORKDIR /source
COPY . /source/
RUN python -m pip install --no-cache-dir -r requirements-agent-ci.txt tomlkit==0.13.3 \
    && npm ci \
    && git init --quiet \
    && git add . \
    && chmod -R go-rwx /source \
    && mkdir /evidence

CMD ["python", "scripts/validation_ci.py", "--check", "checks", "--output", "/evidence"]

FROM core AS engines

ENV BLENDER=/opt/blender/blender

# https://download.blender.org/release/Blender4.5/blender-4.5.3.sha256
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgl1 libegl1 libxi6 libxrender1 libxfixes3 libxkbcommon0 \
       libsm6 libice6 libx11-6 libxxf86vm1 libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/* \
    && curl --fail --location --retry 3 \
       https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz \
       --output /tmp/blender.tar.xz \
    && echo '975c58fcb244273838534bba771e64ad87739216b0f9b39a888531a49a72d845  /tmp/blender.tar.xz' | sha256sum --check - \
    && mkdir /opt/blender \
    && tar -xJf /tmp/blender.tar.xz --strip-components=1 -C /opt/blender \
    && rm /tmp/blender.tar.xz

CMD ["python", "scripts/validation_ci.py", "--check", "blender", "--output", "/evidence"]

# A direct build defaults to the lightweight core image.
FROM core AS default
