goldib/
├── orchestrator/                 # 🧠 Main Command Center (Ray/FastAPI)
│   ├── main.py                   # Startet Ray Cluster & FastAPI Webserver
│   ├── api/                      # REST/WebSocket Endpunkte für UI
│   ├── cluster_manager.py        # Spawnt und überwacht Asset-Container
│   └── cloud_deploy/             # Multi-Cloud Orchestrierung
│       ├── do_provider.py        # DigitalOcean Droplet Deployment
│       ├── aws_provider.py       # AWS ECS Deployment
│       └── azure_provider.py     # Azure ML Deployment
│
├── actors/                       # 🚀 Die isolierten Asset-Container
│   ├── asset_actor.py            # Basis-Klasse (Ray Actor) / Einstiegspunkt
│   ├── data_feed/                # ib_insync oder ccxt Live-Feeds
│   ├── engine/
│   │   ├── prophecy.py           # Signal-Generierung & Konfluenz
│   │   ├── esoteric/
│   │   │   ├── astrology.py      # SwissEph Natal vs. Transit
│   │   │   ├── hermetics.py      # Numerologie & Kybalion
│   │   │   └── space_weather.py  # NOAA API (Solar Flares, Geomagnetic)
│   │   └── technical/            # Pandas-TA Indikatoren
│   ├── ai/
│   │   ├── lstm_predictor.py     # Deep Learning Preisvorhersage
│   │   ├── rl_trade_manager.py   # Stable-Baselines3 Trade-Caring (SL/TP)
│   │   └── online_learner.py     # Live Model-Weight Updates
│   └── execution/                # Paper-Trading & Mock Broker
│
├── shared/                       # 📦 Gemeinsame Modelle & Configs
│   ├── models/
│   │   ├── trading_profile.py    # Pydantic: Der KI-Kontext (Risk, Weights)
│   │   └── prophecy_data.py      # Pydantic: 70+ Feature Vektor
│   ├── db/
│   │   ├── timescale_repo.py     # Historische Daten
│   │   └── redis_pubsub.py       # Inter-Actor Kommunikation & State
│   └── constants.py
│
├── ui/                           # 💻 React/Next.js Dashboard
│   ├── src/components/           # Charts, Actor-Status-Cards
│   └── package.json
│
├── docker/
│   ├── Dockerfile.orchestrator   # Image für Command Center
│   └── Dockerfile.asset_actor    # Image für die einzelnen Assets
│
├── scripts/                      # 🔁 Die Ralph-Loops
│   ├── loop_1_infra.ps1          # Setzt Redis & Timescale auf
│   ├── loop_2_actor.ps1          # Baut den ersten Hello-World Container
│   └── ...
└── requirements.txt              # ray, fastapi, torch, swisseph, etc.

