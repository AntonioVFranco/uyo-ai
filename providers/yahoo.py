
from __future__ import annotations
import pandas as pd
import yfinance as yf
from .base import ProviderBase, IntradayQuery

class YahooProvider(ProviderBase):
    name = "yahoo"

    def get_intraday(self, q: IntradayQuery) -> pd.DataFrame:
        # yfinance has limited intraday history on free tier; use for demos
        interval_map = {"1min": "1m", "2min": "2m", "5min": "5m", "15min": "15m", "30min": "30m", "60min": "60m"}
        iv = interval_map.get(q.interval, "5m")
        df = yf.download(q.symbol, period="5d", interval=iv, progress=False)
        if df.empty:
            return pd.DataFrame(columns=["ts","open","high","low","close","volume"])
        df = df.rename(columns=str.lower).reset_index().rename(columns={"datetime":"ts"})
        if "index" in df.columns:
            df = df.rename(columns={"index":"ts"})
        if "date" in df.columns and "ts" not in df.columns:
            df = df.rename(columns={"date":"ts"})
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        return df[["ts","open","high","low","close","volume"]]

    def get_daily(self, symbol: str, start: str | None, end: str | None) -> pd.DataFrame:
        df = yf.download(symbol, start=start, end=end, progress=False)
        if df.empty:
            return pd.DataFrame(columns=["date","open","high","low","close","volume"])
        df = df.rename(columns=str.lower).reset_index().rename(columns={"date":"date"})
        df["date"] = pd.to_datetime(df["date"]).dt.date
        return df[["date","open","high","low","close","volume"]]
