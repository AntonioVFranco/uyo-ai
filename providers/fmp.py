from __future__ import annotations

import os

import pandas as pd
import requests

from .base import IntradayQuery, ProviderBase


class FmpProvider(ProviderBase):
    name = "fmp"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("FMP_API_KEY", "")

    def get_intraday(self, q: IntradayQuery) -> pd.DataFrame:
        # FMP intraday requires paid tier for some endpoints; keep daily for free tier
        return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])

    def get_daily(self, symbol: str, start: str | None, end: str | None) -> pd.DataFrame:
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol.upper()}"
        params = {"apikey": self.api_key, "serietype": "line"}
        r = requests.get(url, params=params, timeout=30)
        if r.status_code != 200:
            return pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])
        data = r.json()
        hist = data.get("historical", [])
        rows = [
            {
                "date": pd.to_datetime(x["date"]).date(),
                "open": float(x.get("open", "nan")),
                "high": float(x.get("high", "nan")),
                "low": float(x.get("low", "nan")),
                "close": float(x.get("close", "nan")),
                "volume": float(x.get("volume", 0)),
            }
            for x in hist
        ]
        df = pd.DataFrame(rows).sort_values("date")
        if start:
            df = df[df["date"] >= pd.to_datetime(start).date()]
        if end:
            df = df[df["date"] <= pd.to_datetime(end).date()]
        return df[["date", "open", "high", "low", "close", "volume"]]
