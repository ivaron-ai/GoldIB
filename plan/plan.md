# GoldIB - Project Plan

## Overview
GoldIB is an advanced high-frequency trading system using Python (Ray/FastAPI), Docker, and AI (LSTM/RL). The system uses an actor model where each asset (BTC, AAPL) runs in an isolated container.

## Project Phases (Ralph Loops)

### Loop 1: Basis-Infrastruktur & Orchestrator (Current Focus)
**Goal:** Base framework, Console App, DB Containers.
- [ ] Initialize Python 3.11+ environment (poetry/pip).
- [ ] Create Multi-Stage Dockerfile for Base-App.
- [ ] Create `docker-compose.yml` (TimescaleDB, Redis).
- [ ] Develop `main.py` (Console + FastAPI background).
- [ ] Implement structured logging (AIOps).
- [ ] **Stop-Hook:** `pytest` checks DB connections and FastAPI health (200 OK).

### Loop 2: Web-UI Dashboard
**Goal:** Browser interface for monitoring.
- [ ] Integrate Frontend (React/Static Files via FastAPI).
- [ ] Implement System Health Monitoring Dashboard.
- [ ] Create API routes for Container status.
- [ ] **Stop-Hook:** Selenium/Playwright test for UI reachability.

### Loop 2.5: Dynamic Portfolio Engine (DPE)
**Goal:** Auto-Portfolio Maker / Discovery Agent.
- [ ] Create `orchestrator/portfolio/` structure.
- [ ] Implement `discovery_agent.py` (Market Scanner).
- [ ] Implement `risk_allocator.py` (Kelly Criterion).
- [ ] **Stop-Hook:** Unit tests for allocation logic.

### Loop 3: Trade-Instrument-Aktor (Basis-Container)
**Goal:** Autonomous Trading Container blueprint.
- [ ] Create `AssetActor` Docker image/dir.
- [ ] Implement `TradingProfile` (State Container).
- [ ] Integrate Broker API (ib_insync/ccxt).
- [ ] Implement `ExecutionEngine` (Trade-Caring, Trailing-Stops).
- [ ] **Stop-Hook:** Unit test for Trailing Stop logic.

### Loop 4: AI Brain & Online Learning
**Goal:** Integrate ML/DL models.
- [ ] In inference logic (PyTorch LSTM).
- [ ] RL Module (Trade-Sizing/Exit-Timing).
- [ ] Online Learning Loop (River/LightGBM).
- [ ] **Stop-Hook:** Full lifecycle test (Tick -> Prediction -> Trade -> Update).

### Loop 5: Multi-Cloud Orchestration
**Goal:** Cloud deployment capabilities.
- [ ] Implement `CloudTrainingOrchestrator`.
- [ ] Interfaces for DigitalOcean, AWS, Azure.
- [ ] **Stop-Hook:** Mock tests for Cloud APIs.

## Current Tasks
- Prepare "Ralph Loop 1" job structure.
- Create `prompt.md` and `stop-hook.ps1` for Loop 1.
