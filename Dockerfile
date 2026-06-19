FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy
WORKDIR /workspace
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.12-slim AS runtime
WORKDIR /workspace
COPY --from=builder /workspace/.venv ./.venv
COPY app ./app
COPY migrations ./migrations
COPY frontend ./frontend
ENV PATH="/workspace/.venv/bin:$PATH"
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --create-home --shell /bin/bash appuser && \
    chown -R appuser:appgroup /workspace
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]