# RAMS: Forex Risk Analytics Microservice

RAMS is a high-performance microservice designed for real-time risk analytics in Forex trading. It ingests 1-second OHLC bars and calculates key risk metrics for a defined set of currency pairs.

## Architecture

- **Microservice**: Built with Python (FastAPI).
- **Data Frequency**: 1-second OHLC bars.
- **Storage**: In-memory ring buffers for high-speed calculation (backed by TimescaleDB/Redis in future phases).

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd RAMS
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**:
    Copy `.env.template` to `.env` (or use the provided `.env`):
    ```bash
    cp .env.template .env
    ```
    Ensure `SYMBOLS` and `BAR_FREQUENCY` are set correctly.

## Usage

### Run Locally
```bash
uvicorn app.main:app --reload
```

### API Endpoints

-   `GET /health`: Check service health and environment.
-   `GET /ready`: Check if service is ready to accept traffic.
-   `POST /ingest`: Ingest 1s OHLC bars.
-   `GET /metrics/{symbol}`: Get risk metrics for a specific symbol.
-   `GET /metrics/portfolio`: Get aggregated portfolio risk metrics.
-   `GET /metrics`: Prometheus metrics scraper.

## Contributing

-   Follow PEP 8 style guide.
-   Ensure all tests pass before submitting PRs.