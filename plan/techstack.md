Backend & Orchestrierung: Python 3.12+ mit FastAPI (für das Web-UI) und Ray (für das Actor-Modell/verteiltes Rechnen).
Containerisierung: Docker (ein isolierter Container pro Asset, z. B. goldib-btc, goldib-aapl).
Datenhaltung: * TimescaleDB (PostgreSQL) für historische Kerzen, Ticks und Signal-Logs.
Redis für schnelles Live-State-Management, Pub/Sub-Broadcasting (z.B. für den GlobalAnalyst) und In-Memory Feature-Buffer.
KI & Machine Learning:
PyTorch für LSTM (Preise) und RL (Deep Q-Learning für Trade-Management).
River oder LightGBM für schnelles inkrementelles Online-Learning (Trade-by-Trade Updates im RAM).
Externe Daten & Esoterik:
swisseph (Swiss Ephemeris) für hochpräzise Astrologie.
NOAA SWPC API für Space Weather (Kp-Index, Solar Flares X-Ray Flux).
Frontend (Web-UI): Next.js (React) mit TailwindCSS und TradingView Lightweight Charts.