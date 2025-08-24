
# UYO AI — Microstructure & Execution

Open‑source educational stack to analyze execution costs (VWAP/TWAP/arrival, implementation shortfall),
slice orders (TWAP/VWAP/POV), visualize liquidity heatmaps, replay sessions, and generate post‑trade executive briefs.
No trading signals. Paper trading by default. Apache‑2.0.

## Quickstart (WSL)
```bash
# 1) Create and activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3) Pre-commit hooks (optional but recommended)
pre-commit install

# 4) Run API and UI
make run-api
make run-ui
# API: http://127.0.0.1:8000/docs
# UI : streamlit prints the URL (usually http://localhost:8501)
```

## Environment
Copy `.env.example` to `.env` and fill free API keys if you have them:
- `ALPHAVANTAGE_API_KEY`
- `FINNHUB_API_KEY`
- `TWELVEDATA_API_KEY`
- `FMP_API_KEY`

## Docker (optional)
```bash
docker compose up --build
```

## Monorepo layout
```text
apps/
  uyo_ai_api/        # FastAPI service (REST)
  uyo_ai_ui/         # Streamlit UI

engines/
  execution/         # KPIs (VWAP/TWAP/IS), slicer, simulator (stubs)

providers/
  base.py            # ProviderBase interface
  alphavantage.py    # Alpha Vantage adapter (basic)
  yahoo.py           # yfinance adapter (basic)
  stooq.py           # Stooq adapter (basic)
  fmp.py             # Financial Modeling Prep (basic)

infra/docker/        # Dockerfiles
reports/             # templates (future)
configs/             # .env.example and policies placeholders
tests/               # pytest stubs
```

## Run commands
The Makefile targets use the updated module paths:
- API: `make run-api` (uvicorn `apps.uyo_ai_api.app:app`)
- UI: `make run-ui` (Streamlit `apps/uyo_ai_ui/app.py`)

## Security & Compliance
- No PII, paper trading only, educational use.
- No recommendations or trading signals.
- Headers, dependency pinning, and CI stubs included.

## License
Apache-2.0
