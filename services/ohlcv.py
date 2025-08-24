from __future__ import annotations

import datetime as dt
from typing import Tuple

import pandas as pd

from providers.yahoo import fetch_daily_yahoo
from providers.stooq import fetch_daily_stooq
from data.warehouse import read_daily, upsert_daily


def _datepair(start: str | dt.date, end: str | dt.date) -> Tuple[dt.date, dt.date]:
    s = start if isinstance(start, dt.date) else dt.date.fromisoformat(str(start)[:10])
    e = end if isinstance(end, dt.date) else dt.date.fromisoformat(str(end)[:10])
    return (s, e)


def ensure_daily(symbol: str, start, end) -> pd.DataFrame:
    s, e = _datepair(start, end)
    existing = read_daily(symbol, s, e)
    if not existing.empty and len(existing) >= (e - s).days * 0.6:
        return existing
    # fetch missing via Yahoo, fallback to Stooq
    try:
        fetched = fetch_daily_yahoo(symbol, s, e)
    except Exception:
        fetched = fetch_daily_stooq(symbol, s, e)
    if not fetched.empty:
        upsert_daily(symbol, fetched)
        return read_daily(symbol, s, e)
    return existing

