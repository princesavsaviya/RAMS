What RAMS is: Forex Risk Analytics Microservice

Symbols (asset list): EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, USDINR, EURINR

Data format: 1-second OHLC bars (recommended)

Endpoints:

POST /ingest

GET /metrics/{symbol}

GET /metrics/portfolio

GET /health, GET /ready

GET /metrics (Prometheus)

Example payload for /ingest

Example response keys for /metrics/{symbol}

How to run locally + Docker + compose (Add in Future)