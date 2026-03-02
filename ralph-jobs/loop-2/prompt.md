# Ralph-Loop 2: Full GoldIB Architecture

**Goal:** Build the complete GoldIB system on top of the Loop 1 foundation: Web-UI Dashboard, Dynamic Portfolio Engine (with esoteric screener), AssetActor container blueprint, AI Brain (LSTM + RL + Online Learning), and Multi-Cloud Orchestration stubs.

**Working Directory:** All project files MUST be created at the GoldIB repository root (`../../` relative to this job directory). Use absolute paths when creating files.

**Repo root:** Resolve via `$PSScriptRoot\..\..\` or use the path shown when the loop started.

---

## Phase A: Web-UI Dashboard

Create a minimal but functional dashboard served by FastAPI as static files.

**A1. Static UI files at `ui/` in the repo root:**
- `ui/index.html` — Dark-mode dashboard with gold accent (#FFD700 on #1a1a2e background).
  - Header: "GoldIB Trading System"
  - Section: "System Status" — shows health status fetched from `/health`
  - Section: "Active Actors" — shows running asset containers fetched from `/api/actors`
  - Section: "Portfolio Overview" — shows portfolio data fetched from `/api/portfolio/status`
  - Auto-refreshes every 5 seconds via JavaScript fetch. No external CDN dependencies (inline CSS + vanilla JS only).
- `ui/style.css` — Additional styles (dark mode, gold accents, status badges).

**A2. Extend `src/api.py`:**
- Mount `ui/` as StaticFiles at `/ui` using FastAPI's `StaticFiles`.
- Serve `ui/index.html` at the root `/` (replacing the current JSON response).
- Add `GET /api/actors` — returns list of running Docker containers whose names start with `goldib-` (use `docker ps` via subprocess or the Docker SDK if available, fall back to mock data if Docker SDK not installed).
- Add `GET /api/portfolio/status` — returns mock portfolio data: `{total_capital: 100000, allocated: 0, free: 100000, actors: []}`.

**A3. Add `StaticFiles` dependency:** Add `python-multipart` and ensure `aiofiles` is in `pyproject.toml` dependencies.

---

## Phase B: Dynamic Portfolio Engine (DPE)

Create `src/orchestrator/portfolio/` with the full discovery and allocation architecture.

**B1. `src/orchestrator/__init__.py`** — empty init file.

**B2. `src/orchestrator/portfolio/__init__.py`** — empty init file.

**B3. `src/orchestrator/portfolio/discovery_agent.py`**
- Class `DiscoveryAgent` with method `async scan_top_movers(limit: int = 10) -> list[dict]`.
- Uses `ccxt` (if installed) to fetch top volume/volatility assets from Binance. Falls back to a hardcoded mock list of top movers if ccxt is not installed or raises an exception.
- Returns list of dicts: `{symbol, price_change_pct, volume, source: "binance"|"mock"}`.
- Method `async scan_esoteric_candidates(date: datetime = None) -> list[dict]` — checks for assets whose "genesis date" (hardcoded dict mapping symbol -> IPO/ICO date) has a strong Jupiter or Venus transit today (use swisseph if installed, else return mock data). Returns list of `{symbol, transit_type, confidence}`.

**B4. `src/orchestrator/portfolio/risk_allocator.py`**
- Class `RiskAllocator` with:
  - `__init__(self, total_capital: float, max_actors: int = 10)`.
  - `calculate_kelly_fraction(win_prob: float, win_loss_ratio: float) -> float` — implements fractional Kelly criterion (half-Kelly): `f = 0.5 * ((win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio)`. Clamps result between 0.0 and 0.25.
  - `allocate(self, candidates: list[dict]) -> list[dict]` — assigns a `budget` to each candidate using Kelly fraction (use `win_prob=0.55, win_loss_ratio=1.5` as defaults). Returns candidates with `budget` field added.

**B5. `src/orchestrator/portfolio/esoteric_screener.py`**
- Class `EsotericScreener` with method `screen(candidates: list[dict]) -> list[dict]`.
- Attempts to import `swisseph` and use it to compute current planetary positions. If not available, uses a simple deterministic mock based on the current day of week (Mon/Wed/Fri = bullish, Tue/Thu = bearish, weekend = neutral).
- Adds `esoteric_signal: "bullish"|"bearish"|"neutral"` and `esoteric_confidence: float` (0.0–1.0) to each candidate dict.
- Returns the filtered/annotated list.

**B6. Add `GET /api/portfolio/scan` endpoint in `src/api.py`** — runs DiscoveryAgent.scan_top_movers(), passes through EsotericScreener, then RiskAllocator.allocate(), returns the result as JSON.

---

## Phase C: AssetActor — Autonomous Trading Container Blueprint

Create `src/actors/` with the full actor architecture.

**C1. `src/actors/__init__.py`** — empty.

**C2. `src/shared/__init__.py`** and `src/shared/models/__init__.py`** — empty init files.

**C3. `src/shared/models/trading_profile.py`**
- Pydantic model `TradingProfile`:
  - `symbol: str`
  - `strategy: Literal["trend_following", "mean_reversion"]` (default "trend_following")
  - `risk_per_trade: float = 0.02` (2% per trade)
  - `max_position_size: float = 0.1` (10% of capital)
  - `trailing_stop_atr_multiplier: float = 2.0`
  - `win_prob_estimate: float = 0.55`
  - `total_trades: int = 0`
  - `winning_trades: int = 0`
  - `current_position: Optional[dict] = None`
  - `feature_vector: Optional[list[float]] = None`
  - Property `win_rate -> float` — returns winning_trades/total_trades or 0.55 if no trades yet.

**C4. `src/shared/models/prophecy_data.py`**
- Pydantic model `ProphecyData`:
  - `symbol: str`
  - `timestamp: datetime`
  - `close: float`
  - `atr: float = 0.0`
  - `rsi: float = 50.0`
  - `macd_signal: float = 0.0`
  - `volume_ratio: float = 1.0` (current vol / avg vol)
  - `esoteric_signal: str = "neutral"`
  - `confluence_score: float = 0.0` (0.0–1.0, aggregated signal strength)
  - `prediction_direction: Optional[float] = None` (LSTM output: -1.0 to 1.0)

**C5. `src/actors/asset_actor.py`**
- Class `AssetActor`:
  - `__init__(self, symbol: str, profile: TradingProfile = None)`.
  - `async process_tick(self, prophecy: ProphecyData) -> dict | None` — core loop:
    1. Update ATR-based trailing stop if position is open.
    2. Check exit conditions: stop hit, or `abs(prophecy.confluence_score) < 0.2` (weak signal).
    3. Check entry: if no position and `abs(prophecy.confluence_score) > 0.6`, open a mock position.
    4. Returns dict `{action: "buy"|"sell"|"hold"|"close", price, reason}` or None.
  - `_calculate_trailing_stop(self, current_price: float, atr: float) -> float` — returns `current_price - (profile.trailing_stop_atr_multiplier * atr)` for long positions.
  - `update_profile_from_trade(self, won: bool)` — increments `total_trades`, conditionally `winning_trades`; recalculates `risk_per_trade` using Kelly fraction via `RiskAllocator`.

**C6. `src/actors/execution_engine.py`**
- Class `ExecutionEngine`:
  - `__init__(self, actor: AssetActor, redis_client=None)`.
  - `async run_tick(self, market_data: dict) -> dict` — converts raw market_data dict to ProphecyData, calls `actor.process_tick()`, publishes result to Redis channel `f"goldib:{actor.profile.symbol}:signals"` if redis_client is set.
  - `async close_position(self, reason: str)` — closes current position, calls `actor.update_profile_from_trade(won=...)`.

---

## Phase D: AI Brain — LSTM, RL, Online Learning

Create `src/actors/ai/` with the ML model stubs.

**D1. `src/actors/ai/__init__.py`** — empty.

**D2. `src/actors/ai/lstm_predictor.py`**
- Class `LSTMPredictor`:
  - `__init__(self, input_size: int = 10, hidden_size: int = 64, sequence_length: int = 30)`.
  - Tries to import `torch` and define a small `nn.LSTM` + `nn.Linear` model internally. If torch not available, sets `self.model = None`.
  - `predict(self, feature_sequence: list[list[float]]) -> float` — if torch available, runs forward pass on the sequence and returns a direction scalar (-1.0 to 1.0). If not available, returns a simple heuristic: mean of last 3 close log-returns (from feature_sequence), clipped to [-1, 1].
  - `train_step(self, sequence: list[list[float]], target: float) -> float` — one gradient step if torch available, returns loss. Returns 0.0 if not available.

**D3. `src/actors/ai/rl_trade_manager.py`**
- Class `RLTradeManager`:
  - Uses a simple Q-table (dict) if `stable_baselines3` not available, or a DQN policy if it is.
  - States: `(trend: int, rsi_zone: int, position_open: bool)` where trend is -1/0/1 and rsi_zone is 0 (oversold)/1 (neutral)/2 (overbought).
  - Actions: 0=hold, 1=increase_size, 2=reduce_size, 3=close.
  - `select_action(self, state: tuple) -> int` — epsilon-greedy (epsilon=0.1) selection from Q-table.
  - `update_q(self, state, action, reward, next_state)` — Q-learning update: `Q[s,a] += 0.1 * (reward + 0.95 * max(Q[s']) - Q[s,a])`.

**D4. `src/actors/ai/online_learner.py`**
- Class `OnlineLearner`:
  - Tries to import `river`. If available, uses `river.linear_model.LogisticRegression` with SGD. If not, uses a simple exponential moving average classifier.
  - `learn_one(self, features: dict, won: bool)` — incremental update with one trade result.
  - `predict_one(self, features: dict) -> float` — returns win probability estimate (0.0–1.0).

---

## Phase E: Multi-Cloud Orchestration Stubs

Create `src/orchestrator/cloud_deploy/` with provider interfaces.

**E1. `src/orchestrator/cloud_deploy/__init__.py`** — empty.

**E2. `src/orchestrator/cloud_deploy/base_provider.py`**
- Abstract base class `CloudProvider` (using `abc.ABC`):
  - `@abstractmethod async def deploy_container(self, symbol: str, image: str, config: dict) -> str` — returns container/instance ID.
  - `@abstractmethod async def stop_container(self, instance_id: str) -> bool`.
  - `@abstractmethod async def get_status(self, instance_id: str) -> dict`.

**E3. `src/orchestrator/cloud_deploy/local_provider.py`**
- Class `LocalProvider(CloudProvider)` — deploys containers via `docker run` subprocess calls. Full implementation using Python subprocess + docker CLI.

**E4. `src/orchestrator/cloud_deploy/do_provider.py`**
- Class `DigitalOceanProvider(CloudProvider)` — stub that raises `NotImplementedError("DigitalOcean provider not yet configured. Set DO_API_TOKEN env var.")` unless `DO_API_TOKEN` is set, in which case logs a warning that it's a stub.

**E5. `src/orchestrator/cloud_deploy/aws_provider.py`**
- Class `AWSProvider(CloudProvider)` — stub, raises `NotImplementedError("AWS provider not configured. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")`.

**E6. `src/orchestrator/cloud_deploy/azure_provider.py`**
- Class `AzureProvider(CloudProvider)` — stub, raises `NotImplementedError("Azure provider not configured. Set AZURE_SUBSCRIPTION_ID env var.")`.

**E7. `src/orchestrator/cluster_manager.py`**
- Class `ClusterManager`:
  - `__init__(self, provider: CloudProvider = None)` — defaults to `LocalProvider()`.
  - `async spawn_actor(self, symbol: str, profile: TradingProfile = None) -> str` — deploys a container, stores instance_id in Redis (key: `goldib:actors:{symbol}`), returns instance_id.
  - `async reap_actor(self, symbol: str)` — stops container, removes Redis key.
  - `async list_active_actors(self) -> list[str]` — returns list of active symbols from Redis keys matching `goldib:actors:*`.
- Update `GET /api/actors` in `src/api.py` to use ClusterManager if possible.

---

## Phase F: Tests

Create `tests/test_loop2.py` with unit tests covering:

1. `TestTradingProfile` — instantiation, win_rate property, default values.
2. `TestProphecyData` — instantiation with defaults.
3. `TestRiskAllocator` — Kelly fraction calculation (known inputs/outputs), allocate() returns budgets summing <= total_capital.
4. `TestAssetActor` — process_tick() with high confluence score opens position; with low score stays neutral.
5. `TestLSTMPredictor` — predict() returns value in [-1, 1]; works without torch installed (heuristic path).
6. `TestRLTradeManager` — select_action() returns valid action 0-3; update_q() changes Q-table.
7. `TestOnlineLearner` — learn_one() + predict_one() works (with or without river).
8. `TestEsotericScreener` — screen() adds esoteric_signal to all candidates.
9. `TestDiscoveryAgent` — scan_top_movers() returns list of dicts with required fields (mock path).
10. `TestCloudProviderStubs` — DigitalOceanProvider, AWSProvider, AzureProvider all raise NotImplementedError when env vars not set.

---

## Phase G: Update dependencies

Update `pyproject.toml` to add:
```
aiofiles = "^23.0.0"
ccxt = "^4.0.0"  # for market scanning
river = "^0.21.0"  # for online learning
torch = {version = "^2.0.0", optional = true}  # optional heavy dep
stable-baselines3 = {version = "^2.0.0", optional = true}
swisseph = {version = "*", optional = true}
```
Mark torch, stable-baselines3, swisseph as optional extras in `[tool.poetry.extras]`. Install non-optional new deps via pip into `.venv`.

---

## Summary of files to create

```
src/
  orchestrator/
    __init__.py
    cluster_manager.py
    portfolio/
      __init__.py
      discovery_agent.py
      risk_allocator.py
      esoteric_screener.py
    cloud_deploy/
      __init__.py
      base_provider.py
      local_provider.py
      do_provider.py
      aws_provider.py
      azure_provider.py
  actors/
    __init__.py
    asset_actor.py
    execution_engine.py
    ai/
      __init__.py
      lstm_predictor.py
      rl_trade_manager.py
      online_learner.py
  shared/
    __init__.py
    models/
      __init__.py
      trading_profile.py
      prophecy_data.py
ui/
  index.html
  style.css
tests/
  test_loop2.py
```

Also update: `src/api.py`, `pyproject.toml`.
