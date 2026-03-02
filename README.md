# Ralph

Trading Infrastructure with FastAPI, TimescaleDB, and Redis.

## Quick Start

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Install dependencies
poetry install

# Start infrastructure
docker-compose up -d

# Run application
python -m src.main
```

## Testing

```bash
pytest tests/
```

## Architecture

- **FastAPI** - REST API server
- **TimescaleDB** - Time-series database (PostgreSQL)
- **Redis** - Caching and pub/sub
