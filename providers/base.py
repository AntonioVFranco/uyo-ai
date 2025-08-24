
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import pandas as pd
from abc import ABC, abstractmethod

@dataclass
class IntradayQuery:
    symbol: str
    interval: str  # e.g., "1min", "5min"
    start: Optional[str] = None
    end: Optional[str] = None

class ProviderBase(ABC):
    name: str

    @abstractmethod
    def get_intraday(self, q: IntradayQuery) -> pd.DataFrame:
        """Return DataFrame with columns: ts, open, high, low, close, volume."""
        raise NotImplementedError

    @abstractmethod
    def get_daily(self, symbol: str, start: Optional[str], end: Optional[str]) -> pd.DataFrame:
        """Return DataFrame with columns: date, open, high, low, close, volume."""
        raise NotImplementedError
