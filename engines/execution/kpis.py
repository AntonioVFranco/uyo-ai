
from __future__ import annotations
import numpy as np
import pandas as pd

def vwap(df: pd.DataFrame) -> float:
    """
    Compute VWAP from a DataFrame containing columns: "close" and "volume".
    Returns a float. Assumes non-empty input with positive volume.
    """
    num = (df["close"] * df["volume"]).sum()
    den = df["volume"].sum()
    return float(num / den) if den else float("nan")

def twap(df: pd.DataFrame) -> float:
    """Simple TWAP over the "close" column."""
    return float(df["close"].mean()) if not df.empty else float("nan")
