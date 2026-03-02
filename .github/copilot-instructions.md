# Copilot Instructions for GoldIB

This repository contains a high-frequency trading system built with Python (FastAPI, Ray), Docker, and AI (PyTorch, RL). The development process is driven by an agent loop script.

## Development Workflow

We use `ralph-loop.ps1` to drive development through defined "jobs" or "loops".

- **Run a Job:** `.\ralph-loop.ps1 <job-name>`
- **Job Location:** `ralph-jobs/<job-name>/`
- **Job Structure:**
  - `prompt.md`: The task description and instructions.
  - `stop-hook.ps1`: A PowerShell script that verifies completion (must return exit code 0 on success).
  - `checklist.json`: Optional step tracking.
  - `sessions/`: Directory where the agent loop stores its progress state.

**Before starting work:**
1. Check `plan/plan.md` for the current project status.
2. Read `plan/systemarchitectur.md` to understand architectural decisions.
3. Verify if a relevant job already exists in `ralph-jobs/`.

## Build, Test, and Lint

Since this is a multi-container environment, testing and verification are handled per-job via the `stop-hook.ps1`.

- **Run Verification:** Execute the job's stop hook:
  ```powershell
  .\ralph-jobs\<job-name>\stop-hook.ps1
  ```
- **Standard Tests:**
  - Python tests should be in `tests/` and runnable via `pytest`.
  - Docker services are defined in `docker-compose.yml`.

## High-Level Architecture

- **Orchestrator:** Python 3.11+ console app using Ray for actor model and FastAPI for the web UI backend.
- **Frontend:** Next.js (React) with TailwindCSS and TradingView Lightweight Charts.
- **Data Storage:**
  - **TimescaleDB:** Historical candles, ticks, signal logs.
  - **Redis:** Live state management, Pub/Sub broadcasting.
- **AI/ML:**
  - **PyTorch:** LSTM for price prediction, RL for trade management.
  - **River/LightGBM:** Online learning (incremental updates).
- **Infrastructure:** One Docker container per asset (e.g., `goldib-btc`, `goldib-aapl`).

## Key Conventions

- **Atomic Loops:** Keep jobs small and focused (e.g., "Setup Base Infra", "Create UI Skeleton").
- **Test-Driven:** The `stop-hook` should ideally run automated tests (pytest, curl, etc.) to verify success.
- **Path Handling:** Use Windows-style paths (backslashes) as the environment is Windows-based.
- **State Persistence:** Do not rely on memory between sessions; verify state from files or the database.
- **Existing Code:** Always `grep` or search for existing implementations before writing new code to avoid duplication.
