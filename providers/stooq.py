from __future__ import annotations

import io

import pandas as pd
import requests

from .base import IntradayQuery, ProviderBase


class StooqProvider(ProviderBase):
    name = "stooq"

    def get_intraday(self, q: IntradayQuery) -> pd.DataFrame:
        # Stooq intraday availability is limited; primary use is daily
        return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])

    def get_daily(self, symbol: str, start: str | None, end: str | None) -> pd.DataFrame:
        # CSV endpoint for daily data
        url = f"https://stooq.com/q/d/l/?s={symbol.lower()}&i=d"
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])
        df = pd.read_csv(io.StringIO(r.text))
        if df.empty:
            return pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df = df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )
        if start:
            df = df[df["date"] >= pd.to_datetime(start).date()]
        if end:
            df = df[df["date"] <= pd.to_datetime(end).date()]
        return df[["date", "open", "high", "low", "close", "volume"]]
