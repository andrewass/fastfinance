# FastFinance

[![](https://img.shields.io/badge/python-3.12--3.14-blue.svg?style=flat)](https://www.python.org/)

FastFinance is a FastAPI backend that exposes stock/market information from [yfinance](https://github.com/ranaroussi/yfinance), including prices, holders, profile data, and statistics.

## Tech Stack

- Python `3.12 - 3.14` (including `3.14.3`)
- FastAPI
- Uvicorn (ASGI server)
- Pydantic v2 + pydantic-settings
- yfinance + pandas
- Redis (optional cache persistence backend)
- Docker + Kubernetes manifests (Skaffold workflow included)

## Main Modules

- `price`: current and historical prices
- `holders`: institutional and mutual fund holder data
- `profile`: company profile fields (industry, location, summary, etc.)
- `statistics`: financial metrics (market cap, P/B, P/E, EPS, dividends)
- `cache`: cache decorator + persistence abstraction (memory/Redis)
- `settings`: runtime/cache settings and Redis settings

## Local Setup

### Prerequisites

- Python 3.12 to 3.14
- Docker (optional, for local Redis)

### 1) Create virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) (Optional) Start Redis

```bash
docker compose up -d redis
```

### 3) Run API

Development:

```bash
uvicorn app.main:app --reload
```

Production-like local run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API is available at `http://localhost:8000`.

## Build and Verification

Build Docker image:

```bash
docker build -t fastfinance-image .
```

Basic code sanity check:

```bash
python -m compileall app
```

Run with Skaffold:

```bash
skaffold dev
```

## Configuration

Primary settings are defined in:

- `app/settings/settings.py`
- `app/settings/redissettings.py`

Current defaults:

- `cache_enabled = true`
- cache persistence defaults to in-memory (`MemoryPersistence`)
- Redis defaults:
  - `host = redis`
  - `port = 6379`
  - `user = default`
  - `password = redisDockerTestPassword`

## API Overview

Base URL: `http://localhost:8000`

Interactive docs:

- Swagger UI: `GET /docs`
- OpenAPI: `GET /openapi.json`

### Holders

- `GET /holders/{symbol}`
  - Get holders for a symbol.

### Price

- `GET /price/current-price/{symbol}`
  - Get current price for one symbol.
- `POST /price/symbols`
  - Get current prices for a list of symbols.
  - Request body:
    ```json
    { "symbols": ["AAPL", "MSFT"] }
    ```
- `GET /price/historical-prices?symbol={symbol}&period={period}`
  - Get historical prices for one symbol.
  - Supported `period` values: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`.

### Profile

- `GET /profile/{symbol}`
  - Get company profile fields (address, industry, sector, website, summary, etc.).

### Statistics

- `GET /statistics/{symbol}`
  - Get financial statistics (market cap, price-to-book, price-to-earnings, EPS, dividends).

## Kubernetes

Key files:

- `k8s/app.yaml`
- `skaffold.yaml`

Skaffold builds `fastfinance-image` from `Dockerfile` and applies `k8s/app.yaml`.

## CI and Automation

Repository automation currently includes:

- Dependabot configuration (`.github/dependabot.yml`)
- Dependabot auto-merge workflow for patch/minor updates (`.github/workflows/dependabot-auto-merge.yml`)
- Python compatibility workflow across 3.12/3.13/3.14 (`.github/workflows/python-version-compat.yml`)

## Practical Notes

- Data quality and field availability depend on upstream Yahoo Finance responses.
- External calls are network-bound and can fail/time out; handle this in clients accordingly.
- Existing routes are public and do not currently implement auth.
- If you change route contracts, keep backward compatibility unless intentionally introducing a breaking change.
