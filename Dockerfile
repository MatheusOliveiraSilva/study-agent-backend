# Stage 1: Base image with Python and uv
FROM python:3.11-slim as base
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # uv
    UV_EXTRA_INDEX_URL=""

# Install uv
RUN pip install uv

WORKDIR /app

# Stage 2: Builder image - Install dependencies
FROM base as builder
COPY pyproject.toml uv.lock* ./
# Install dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Stage 3: Final image - Copy application code and run
FROM base as final
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./app /app/app

# Expose the port the app runs on
EXPOSE 8000

# Run the application using uvicorn with hot-reloading for development
# For production, you might use a different command (e.g., without --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 