# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered output for logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv from official ghcr image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency configuration and lockfile
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync (frozen ensures exact lockfile versions)
RUN uv sync --frozen --no-install-project

# Copy application source code
COPY . .

# Install the application itself
RUN uv sync --frozen

# Expose FastAPI / Uvicorn default port
EXPOSE 8000

# Run FastAPI using uv run uvicorn inside the container bound to 0.0.0.0
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

