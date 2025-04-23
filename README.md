# Study Agent Backend

This repository contains the backend for the Study Agent project, built with FastAPI and containerized with Docker, and observability using Grafana.

App demo:

https://github.com/user-attachments/assets/1cc81bf0-8fd2-4d1e-ab11-1aed678db136

Front-End: https://github.com/MatheusOliveiraSilva/study-agent-frontend

## Prerequisites

- Docker and Docker Compose
- Make (optional, for local development)
- Python 3.12+ (for local development without Docker)
- uv package manager (for local development)

## Environment Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/study-agent-backend.git
   cd study-agent-backend
   ```

2. Create a `.env` file (using stuff like .env_example varibles) in the root directory with your environment variables or use the existing one.

## Running with Docker Compose

The easiest way to run the application is using Docker Compose:

```bash
# Build and start all services
docker compose up --build

# Run in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

The API will be available at `http://localhost:8000`.

## Using the Makefile

The Makefile provides several commands to simplify local development:

```bash
# Install dependencies (including dev dependencies)
make install

# Run linters to check code quality
make lint

# Format code automatically
make format

# Run tests
make test

# Run lint and tests
make check
```

## Local Development Without Docker

1. Install dependencies:
   ```bash
   make install
   ```

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

- `app/`: Application source code
- `tests/`: Test files
- `Dockerfile`: Container definition
- `docker-compose.yml`: Multi-container Docker configuration
- `Makefile`: Development workflow commands
- `pyproject.toml`: Project dependencies and metadata

## Environment Variables

The application uses environment variables defined in the `.env` file for configuration, including:

- OpenTelemetry endpoints
- API keys
- Other configuration options

Make sure to properly configure these variables before running the application.

