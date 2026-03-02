# GoldIB Agent Instructions & Context

## Project: GoldIB
High-frequency trading system using Python (Ray/FastAPI), Docker, and AI (LSTM/RL).
Target: Multi-Cloud, Autonomous "Asset Actors".

## Ralph Loop Protocol
We use `scripts/ralph-loop.ps1` to drive development.
**Usage:** `.\scripts\ralph-loop.ps1 <job-name>`

**Job Structure (`ralph-jobs/<job-name>/`):**
1.  `prompt.md`: The task description.
2.  `stop-hook.ps1`: The definition of "Done". Must return exit code 0 on success.
3.  `checklist.json`: Optional step tracking.

**Best Practices:**
-   **Atomic Loops:** Keep loops small (e.g., "Setup Base Infra", "Create UI Skeleton").
-   **Test-Driven:** The `stop-hook` should ideally run `pytest` or a similar verification script.
-   **State:** Use `sessions/` to track progress.

## Tech Stack & Standards
-   **Language:** Python 3.11+
-   **Package Manager:** Poetry (preferred) or pip.
-   **Concurrency:** AsyncIO (FastAPI), Ray (Actor Model).
-   **Containerization:** Docker, Docker Compose.
-   **Database:** TimescaleDB (Time-Series), Redis (State/Cache).
-   **Frontend:** React/Vue/Streamlit (served via FastAPI).

## Copilot Skills (You)
-   **Plan First:** Always check `plan/plan.md` before starting a loop.
-   **Context:** Read `plan/systemarchitectur.md` for architectural decisions.
-   **Search:** Use `grep` to find existing implementations before writing new code.
-   **Safety:** Do not overwrite existing code without verifying backups/git status (though currently not a git repo, be careful).
