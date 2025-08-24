import datetime as dt
import os
import typing as t

import requests
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="UYO AI", layout="wide")

st.title("UYO AI — Microstructure & Execution")
st.caption(
    "Educational/experimental app: execution KPIs, slicer, liquidity heatmap, replay, post-trade briefs. No signals. Paper trading only."
)

# Load environment variables from configs/.env if present (non-fatal if missing)
_dotenv_path = os.path.join("configs", ".env")
if os.path.exists(_dotenv_path):
    try:
        load_dotenv(dotenv_path=_dotenv_path, override=False)
    except Exception:
        # Ignore any dotenv parsing errors to avoid breaking the UI
        pass


def get_api_base() -> str:
    """Return the API base URL from environment with a safe default.

    Reads `API_BASE_URL` and defaults to `http://127.0.0.1:8000`.
    Trailing slashes are removed for consistent joining.
    """

    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def fetch_kpis(symbol: str) -> t.Dict[str, float]:
    """Fetch execution KPIs for the given symbol from the FastAPI backend.

    Builds a 24h UTC window ending now with a single demo fill payload.
    Raises RuntimeError for non-2xx responses and ValueError for shape issues.
    """

    now = dt.datetime.now(dt.timezone.utc)
    start = now - dt.timedelta(days=1)

    body: t.Dict[str, t.Any] = {
        "window": {"start": start.isoformat(), "end": now.isoformat()},
        "fills": [
            {
                "order_id": "demo-1",
                "symbol": symbol.upper(),
                "ts": start.isoformat(),
                "side": "BUY",
                "qty": 100.0,
                "price": 100.0,
            }
        ],
    }

    resp = requests.post(
        f"{get_api_base()}/exec/kpis",
        params={"symbol": symbol.upper()},
        json=body,
        timeout=15,
    )

    if not (200 <= resp.status_code < 300):
        raise RuntimeError(f"API {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    for key in ("is_bps", "vwap_shortfall_bps", "twap_shortfall_bps"):
        if key not in data:
            raise ValueError(f"Missing key in response: {key}")
    return data  # type: ignore[return-value]


tab1, tab2, tab3 = st.tabs(["Yesterday", "Slippage Explorer", "Slicing Lab"])

with tab1:
    st.subheader("Yesterday KPIs")
    symbol = st.text_input("Symbol", value="AAPL").strip() or "AAPL"
    if st.button("Fetch KPIs"):
        with st.spinner("Fetching KPIs..."):
            try:
                kpis = fetch_kpis(symbol)
                st.metric("Implementation Shortfall (bps)", f"{kpis['is_bps']:.1f}")
                st.metric("VWAP Shortfall (bps)", f"{kpis['vwap_shortfall_bps']:.1f}")
                st.metric("TWAP Shortfall (bps)", f"{kpis['twap_shortfall_bps']:.1f}")
            except Exception as e:
                st.warning(str(e))

with tab2:
    st.subheader("Slippage Explorer")
    st.write("Visualize distributions and time-series when data and charts are wired.")

with tab3:
    st.subheader("Order Slicer Coach")
    st.write("Plan TWAP/VWAP/POV child orders with constraints (max bar participation, pauses).")

st.divider()
st.info(
    "Fill API keys in `.env` (optional). Respect data provider terms. This project is for educational use only."
)
