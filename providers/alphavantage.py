from __future__ import annotations

import os

import pandas as pd
import requests

from .base import IntradayQuery, ProviderBase


class AlphaVantageProvider(ProviderBase):
    name = "alphavantage"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY", "")

    def get_intraday(self, q: IntradayQuery) -> pd.DataFrame:
        interval_map = {
            "1min": "1min",
            "5min": "5min",
            "15min": "15min",
            "30min": "30min",
            "60min": "60min",
        }
        iv = interval_map.get(q.interval, "5min")
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": q.symbol,
            "interval": iv,
            "apikey": self.api_key,
            "outputsize": "compact",
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        # Parse minimal structure; AV returns "Time Series (5min)" object
        key = next((k for k in data.keys() if "Time Series" in k), None)
        if not key:
            return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])
        ts = data[key]
        rows = []
        for k, v in ts.items():
            rows.append(
                {
                    "ts": pd.to_datetime(k, utc=True),
                    "open": float(v.get("1. open", "nan")),
                    "high": float(v.get("2. high", "nan")),
                    "low": float(v.get("3. low", "nan")),
                    "close": float(v.get("4. close", "nan")),
                    "volume": float(v.get("5. volume", "0")),
                }
            )
        df = pd.DataFrame(rows).sort_values("ts")
        return df[["ts", "open", "high", "low", "close", "volume"]]

    def get_daily(self, symbol: str, start: str | None, end: str | None) -> pd.DataFrame:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "compact",
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        key = next((k for k in data.keys() if "Time Series" in k), None)
        if not key:
            return pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])
        ts = data[key]
        rows = []
        for k, v in ts.items():
            rows.append(
                {
                    "date": pd.to_datetime(k).date(),
                    "open": float(v.get("1. open", "nan")),
                    "high": float(v.get("2. high", "nan")),
                    "low": float(v.get("3. low", "nan")),
                    "close": float(v.get("5. adjusted close", v.get("4. close", "nan"))),
                    "volume": float(v.get("6. volume", "0")),
                }
            )
        df = pd.DataFrame(rows).sort_values("date")
        if start:
            df = df[df["date"] >= pd.to_datetime(start).date()]
        if end:
            df = df[df["date"] <= pd.to_datetime(end).date()]
        return df[["date", "open", "high", "low", "close", "volume"]]
