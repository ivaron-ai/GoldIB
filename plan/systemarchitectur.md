🏛️ Die Goldib Systemarchitektur
Bevor wir die Agenten loslegen lassen, hier der Blueprint, den die KI bauen wird:
Main Orchestrator (Konsole): Eine Python-Konsolenanwendung (z.B. basierend auf dem Framework Ray oder FastAPI), die als Command Center dient. Sie startet den integrierten Webserver und verwaltet die Container.
Web-UI: Ein modernes, responsives Dashboard (React/Vue oder Streamlit), das über die Konsole ausgeliefert wird. Es visualisiert Systemstatus, Metriken und die 8 goldenen Regeln des UI/UX-Designs.
Datenhaltung: TimescaleDB für historische Ticks/Candles und Redis für das Live-State-Management der Container.
Die Trade-Instrument-Aktoren (Docker Container): Das Herzstück. Für jedes Asset (z.B. BTC, GOLD, AAPL) wird ein isolierter Docker-Container gestartet.
Inhalt: Jeder Container enthält das TradingProfile (Kontext/State), die Modelle (LSTM, Reinforcement Learning, FinGPT) und die Ausführungslogik (Trade-Caring, Stop-Loss/Take-Profit Anpassung).
Online Learning: Da pro Asset maximal ein Container existiert, verbleibt das Modell im RAM und lernt live aus jedem abgeschlossenen Trade (Echtes inkrementelles Lernen).
Multi-Cloud: Container können über eine Abstraktionsschicht wahlweise lokal, auf Azure, AWS oder DigitalOcean ausgeführt werden.

🚀 Projektplan: Die Ralph-Loops (PRD-Spezifikationen)
Für jeden der folgenden Schritte erstellst du ein Product Requirements Document (prd.json), welches du an das Ralph-PowerShell-Skript (z.B. ralph-loop.ps1) verfütterst.
🔁 Ralph-Loop 1: Basis-Infrastruktur & Orchestrator
Ziel: Das Grundgerüst steht, die Konsolen-App läuft und die Datenbanken sind als Container verfügbar.
Tasks für den Agenten:
Initialisiere eine Python 3.11+ Umgebung mit poetry oder pip.
Erstelle ein Multi-Stage Dockerfile für die Basis-App.
Schreibe eine docker-compose.yml, die TimescaleDB (PostgreSQL) und Redis bereitstellt.
Entwickle die main.py als Konsolen-Einstiegspunkt, die einen FastAPI Server im Hintergrund hochfährt.
Implementiere ein robustes Logging-System (strukturiertes Logging für AIOps).
Stop-Hook: pytest prüft, ob die Datenbankverbindungen (Redis/Timescale) stehen und der FastAPI-Health-Endpoint HTTP 200 liefert.
🔁 Ralph-Loop 2: Das Web-UI Dashboard
Ziel: Eine Browser-Schnittstelle, die über den in Loop 1 erstellten Server erreichbar ist.
Tasks für den Agenten:
Integriere ein Frontend (z.B. HTML/JS/CSS mit Tailwind oder ein React-Build, das von FastAPI als Static Files ausgeliefert wird).
Implementiere ein Dashboard für das "System Health Monitoring" und eine Übersicht der Instrumente (vgl. Goldib_Browser_UI.png).
Beachte UI/UX-Best-Practices: Klarer Startpunkt (Dashboard), gute Kontraste (Dark Mode/Gold), Status-Indikatoren der Container.
Erstelle API-Routen in FastAPI, die den Status von Docker-Containern auf dem Host-System auslesen (läuft Container X?).
Stop-Hook: Selenium/Playwright-Test, der prüft, ob das UI unter localhost:8000 erreichbar ist und die Layout-Struktur existiert.
🔁 Ralph-Loop 3: Der Trade-Instrument-Aktor (Basis-Container)
Ziel: Die Blaupause für den autonomen Trading-Container.
Tasks für den Agenten:
Erstelle ein separates Verzeichnis/Docker-Image für den AssetActor.
Implementiere die Klasse TradingProfile als State-Container. Dieses Profil hält die normalisierten Daten, Asset-DNA und historische Performance.
Integriere die Broker-API (z.B. ib_insync für Interactive Brokers oder Capital.com API) für den Daten-Ingest in den Container.
Implementiere die ExecutionEngine (Trade-Caring): Eine Schleife, die offene Positionen überwacht, Trailing-Stops nachzieht (ATR-basiert) und bei extremer Marktumkehr (z.B. ADX/Momentum Crash) frühzeitig aussteigt.
Stop-Hook: Ein Unit-Test, der einen Mock-Tick in das TradingProfile pusht und prüft, ob die ExecutionEngine einen simulierten Stop-Loss korrekt nachzieht.
🔁 Ralph-Loop 4: Das KI-Gehirn & Online-Learning
Ziel: Die ML/DL-Modelle in den Container integrieren und lernfähig machen.
Tasks für den Agenten:
Baue die Inferenz-Logik ein: Lade ein vortrainiertes PyTorch LSTM-Modell (Deep Learning) für die kurzfristige Preisprognose.
Implementiere ein Reinforcement Learning Modul (z.B. mit Stable-Baselines3 oder Deep Q-Learning), das das "Trade-Sizing" und "Exit-Timing" dynamisch steuert.
Erstelle den Online-Learning-Loop: Sobald ein Trade abgeschlossen ist, wird der Feature-Vektor mit dem Ergebnis (Win/Loss) an einen In-Memory-Buffer gesendet. Nutze Online Gradient Boosting oder PyTorch Fine-Tuning, um das Modell im laufenden Container leicht anzupassen, ohne komplett neu zu trainieren.
(Optional) Integriere einen NLP-Call (FinGPT/BloombergGPT Konzept), um Finanznachrichten-Sentiment live abzurufen und in das TradingProfile zu schreiben.
Stop-Hook: Das System muss einen kompletten Lebenszyklus (Tick -> Prediction -> Mock Trade -> Trade Close -> Model Weights Update) ohne Exception durchlaufen.
🔁 Ralph-Loop 5: Multi-Cloud Orchestrierung
Ziel: Der Orchestrator (Konsole) kann Container nicht nur lokal, sondern auch in der Cloud starten.
Tasks für den Agenten:
Implementiere den CloudTrainingOrchestrator in der Haupt-App.
Erstelle Schnittstellen (ICloudComputeProvider Konzept in Python) für:
DigitalOcean: Über die DO API ein CPU-Droplet starten und den Container via SSH/Docker-Machine deployen.
AWS: Den Container an ECS oder SageMaker übergeben.
Azure: Den Container an Azure Container Instances oder Azure ML senden.
Füge dem UI Steuerelemente hinzu, um festzulegen: "Bitcoin auf AWS (GPU)", "EUR/USD Lokal".
Stop-Hook: Mock-Tests der Cloud-APIs (Boto3 für AWS, Azure SDK, DigitalOcean API), die prüfen, ob die Deployment-Payloads korrekt strukturiert sind.

