FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (separate layer — only rebuilds when deps change)
COPY pyproject.toml uv.lock ./

# Install dependencies into the system Python, not a venv
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./

# Default command runs the API — override in Container Apps for the worker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
