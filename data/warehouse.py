from __future__ import annotations

import os
import pathlib
import datetime as dt

import duckdb
import pandas as pd

DEFAULT_PATH = os.getenv("WAREHOUSE_PATH", "data/market.duckdb")


def _connect(path: str | None = None) -> duckdb.DuckDBPyConnection:
    db = pathlib.Path(path or DEFAULT_PATH)
    db.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db))
    con.execute(
        """
    CREATE TABLE IF NOT EXISTS ohlcv_daily (
      symbol TEXT,
      ts DATE,
      open DOUBLE, high DOUBLE, low DOUBLE, close DOUBLE, volume DOUBLE,
      PRIMARY KEY (symbol, ts)
    );
    """
    )
    return con


def upsert_daily(symbol: str, df: pd.DataFrame, path: str | None = None) -> None:
    if df.empty:
        return
    df = df.copy()
    df["symbol"] = symbol.upper()
    df["ts"] = pd.to_datetime(df["ts"]).dt.date
    with _connect(path) as con:
        con.execute("BEGIN")
        con.register("df", df[["symbol", "ts", "open", "high", "low", "close", "volume"]])
        con.execute(
            """
          INSERT OR REPLACE INTO ohlcv_daily
          SELECT symbol, ts, open, high, low, close, volume FROM df
          """
        )
        con.execute("COMMIT")


def read_daily(symbol: str, start: dt.date, end: dt.date, path: str | None = None) -> pd.DataFrame:
    with _connect(path) as con:
        q = (
            "SELECT ts, open, high, low, close, volume FROM ohlcv_daily "
            "WHERE symbol = ? AND ts BETWEEN ? AND ? ORDER BY ts"
        )
        out = con.execute(q, [symbol.upper(), start, end]).fetch_df()
    return out

