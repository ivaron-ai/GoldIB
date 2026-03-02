# Ralph-Loop 1: Basis-Infrastruktur & Orchestrator

**Goal:** Build the foundation. Console App running, Databases active via Docker.

**Tasks:**
1. **Python Env:** Initialize a Python 3.11+ project with `pyproject.toml` (poetry format) and also create a `.venv` virtual environment at the repo root using `python -m venv .venv`, then install all required packages into it.
2. **Dockerfile:** Create a Multi-Stage Dockerfile for the main application.
3. **Docker Compose:** Create docker-compose.yml starting:
    - TimescaleDB (PostgreSQL)
    - Redis
4. **Main App:** Create src/main.py:
    - Entry point for console.
    - Starts a FastAPI server in a background thread/process.
5. **Logging:** Implement basic structured logging.
6. **Tests:** Create tests/test_infra.py to verify:
    - Redis connection is reachable.
    - TimescaleDB connection is reachable.
    - FastAPI endpoint /health returns 200.

**Working Directory:** All project files MUST be created at the GoldIB repository root (two levels up from this job directory: `../../`). Do NOT create project files inside this job directory.

**Constraint:** ensure the directory structure is clean at the repo root (e.g., `../../src/`, `../../tests/`, `../../docker/`).
