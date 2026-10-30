# Dockerfile
FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
COPY prompts ./prompts
RUN uv sync --frozen --no-dev
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "aikit.api:app", "--host", "0.0.0.0", "--port", "8000"]
