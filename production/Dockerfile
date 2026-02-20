### Builder ###
FROM python:3.13-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY /src /app/src
COPY ./pyproject.toml .

RUN uv sync

### Production ###
FROM python:3.13-slim-bookworm AS production

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY /src /app/src
COPY ./worker.py /app
COPY ./client.py /app

ENV PATH="/app/.venv/bin:$PATH"