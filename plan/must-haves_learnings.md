🌟 Top-Features (Was Goldib unbedingt erben muss)
1. ProphecyEngine & Feature-Vielfalt (70+ Features)

Esoterik-Konfluenz: Die einzigartige Kombination aus Swiss Ephemeris (Astrologie Natal vs. Transit), NOAA Space Weather (Sonnenstürme/Kp-Index), Sacred Geometry, Numerologie und hermetischen Prinzipien (Kybalion).

Veto-System: Intelligente Blockaden (z. B. technisches Signal blockiert entgegengesetztes kosmisches Signal).

2. Multi-Timeframe-Analyse (MTF)

Simultane Analyse von 7 Zeitrahmen (1M bis 1W).

Konfluenz-Scoring, Macro/Micro-Trend-Separation und Erkennung von harmonischer Resonanz und Divergenzen.

3. Dynamische Trading Profiles (KI-Kontext)

Asset-spezifische Parameter (z.B. BTC verhält sich anders als Gold).

Lernendes Stop-Loss/Take-Profit-System (Trailing) und Anti-Oszillations-Mechanismen (Verhinderung von Trade-Spamming in Seitwärtsphasen).

Performance-Rollback: Die KI kehrt zu alten Parametern zurück, wenn sich die Performance verschlechtert.

4. Dreischichtige KI-Architektur

Schicht 1: Signal-Engine (Regelbasiert & Esoterik).

Schicht 2: Klassifikator (ML.NET/FastTree) für Win/Loss-Wahrscheinlichkeit.

Schicht 3: Deep Learning (LSTM) für kurzfristige Preisvorhersagen.

5. Walk-Forward & Recency Weighting

Die Modelle gewichten aktuelle Marktdaten (Recency) stärker als alte, um sich an wechselnde Marktregime anzupassen (Drift Detection).

⚠️ Key Learnings & Fallstricke (Warum Goldib in Python/Ray gebaut wird)
1. Thread-Pool Erschöpfung & Concurrency (Der wichtigste Punkt)

GoldAIG-Problem: Massive Task.Run-Aufrufe im Causal Backtesting und geteilter State (Mutable Collections) führten zu Hängern, Deadlocks und Race Conditions.

Goldib-Lösung: Das Ray Actor-Modell. Vollständige Prozess-Isolation. Ein Asset = Ein gekapselter Container. Kein Shared State mehr im RAM.

2. State Management & Immutability

GoldAIG-Problem: Eigenschaften veränderten sich zur Laufzeit unerwartet (Torn Reads).

Goldib-Lösung: Strikte Verwendung von unveränderlichen Datenstrukturen (Pydantic Models). Der Live-State liegt extern und thread-safe in Redis.

3. LSTM Direction Accuracy & Daten-Normalisierung

GoldAIG-Problem: Das Training auf absoluten Preisen führte zu schlechter Richtungsvorhersage (~40% Direction Accuracy).

Goldib-Lösung: KI-Modelle in PyTorch trainieren direkt auf Log-Returns / Z-Scores statt auf Rohpreisen. Implementierung einer Loss-Funktion, die explizit falsche Richtungen bestraft (Direction Penalty).

4. Timeframe- und Daten-Konsistenz

GoldAIG-Problem: Backtests liefen teilweise auf H1, Live-Trading auf M5. Das verfälschte die ML-Realität (Data Leakage).

Goldib-Lösung: TimescaleDB als "Single Source of Truth". Der Backtester nutzt exakt denselben Tick-Datenstrom wie die Live-Execution.

5. Performance-Bottlenecks bei Indikatoren

GoldAIG-Problem: Tausendfache Neuberechnung von Planetenständen und Geometrie bei jedem Tick.

Goldib-Lösung: Cleveres Caching (z.B. Transit-Positionen der Planeten ändern sich so langsam, dass sie nur 1x pro Stunde berechnet und in Redis zwischengespeichert werden).

6. Signal-Symmetrie

GoldAIG-Problem: Asymmetrische Gewichtung von Indikatoren (z.B. Bearish MACD wurde bei "oversold" fälschlicherweise abgewertet).

Goldib-Lösung: Klare Trennung zwischen "Trend-Following" und "Mean-Reversion" Signalen ohne Doppelgewichtungen (wie beim alten "Extreme Confluence Bonus").